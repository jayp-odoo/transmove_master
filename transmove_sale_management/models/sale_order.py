from odoo import api, fields, models

goods_type = [
    ("general cargo", "General Cargo"),
    ("perishable goods", "Perishable Goods"),
    ("hazardous materials", "Hazardous Materials"),
    ("temperature-controlled goods", "Temperature-Controlled Goods"),
    ("oversized or heavy Cargo", "Oversized or Heavy Cargo"),
    ("livestock and animals", "Livestock and Animals"),
    ("personal effects and household goods", "Personal Effects and Household Goods"),
]


class SaleOrder(models.Model):
    """
    this model is inherited from sale.order we used to create our own extended model to gain access to parent
    model assets like views and fields as well as functionality
    """

    _inherit = ["sale.order"]
    _order = "priority desc, id desc"

    origin_city_id = fields.Many2one("res.city", string="Origin City", required=True)
    destination_city_id = fields.Many2one(
        "res.city", string="Destination City", required=True
    )
    mode_of_transport = fields.Selection(
        selection=[("air", "Air"), ("sea", "Sea")], default="air"
    )
    priority = fields.Selection(
        [("0", "Normal"), ("1", "Low"), ("2", "High"), ("3", "Very High")],
        string="Priority",
    )
    # shipment details
    weight = fields.Float(string="Weight of shipment(kg)")
    Quantity = fields.Integer(string="Quantity Of items")
    description = fields.Text(string="Brief Description")
    terms_conditions = fields.Text(string="Terms & Conditions")
    type_of_goods = fields.Selection(
        selection=goods_type, string="Type of goods", default="general cargo"
    )
    estimated_cost = fields.Float(
        string="Estimated Cost", compute="_compute_estimated_cost", readonly=False
    )
    transit_time = fields.Char(
        string="Transit Time (in days)",
        required=True,
    )

    airline_id = fields.Many2one("transmove.airlines", tracking=True)
    state = fields.Selection(group_expand="_expand_groups")

    @api.depends("airline_id", "weight")
    def _compute_estimated_cost(self):
        """
        this compute method will calculate the estimated cost based on weight and airline local fair price
        it will be always exstimated not fixed
        """
        for record in self:
            if record.weight and record.airline_id:
                record.estimated_cost = (
                    record.airline_id.estimated_price_kg * record.weight
                )

    @api.depends("estimated_cost")
    def _compute_amounts(self):
        """
        this method assign estimated cost to parent class variable amount_total which will
        be used later on for invoicing and accounting
        """
        for record in self:
            record.amount_total = record.estimated_cost

    @api.model
    def _expand_groups(self, states, domain, order):
        """
        this expand groups will display states based on the list returned in it
        """
        return ["draft", "sent", "sale", "cancel"]

    def action_confirm(self):
        """
        this buttpm action will be called when state is changed to won
        it will create bookings and pickup requests and customs clearance records
        with only required field booking id
        """
        booking_object = self.env["transmove.bookings"].create({"order_id": self.id})
        self.env["transmove.pickup.requests"].create({"bookings_id": booking_object.id})
        self.env["transmove.customs.clearance"].create(
            {"booking_id": booking_object.id}
        )
        return super().action_confirm()
