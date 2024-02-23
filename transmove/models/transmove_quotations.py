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


class TransmoveQuotations(models.Model):
    """this class is used to store the quotations created by administration"""

    _name = "transmove.quotations"
    _description = "this table is used to store Quotations information"
    _inherit = ["mail.thread"]

    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    origin_city_id = fields.Many2one("res.city", string="Origin City")
    destination_city_id = fields.Many2one("res.city", string="Destination City")
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
    expiration_date = fields.Date()
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
    # status = fields.Selection(
    #     selection=[
    #         ("approved", "Approved"),
    #         ("cancelled", "Cancelled"),
    #         ("pending", "Pending"),
    #     ],
    #     default="pending",
    # )
    airline_id = fields.Many2one("transmove.airlines", tracking=True)
    state = fields.Selection(
        string="Status",
        required=True,
        selection=[
            ("new", "New"),
            ("sent", "Sent"),
            ("won", "Won"),
            ("canceled", "Canceled"),
        ],
        copy=False,
        default="new",
    )

    @api.depends("airline_id", "weight")
    def _compute_estimated_cost(self):
        for record in self:
            if record.weight and record.airline_id:
                record.estimated_cost = (
                    record.airline_id.estimated_price_kg * record.weight
                )

    def action_quotation_send(self):
        """
        this is button action funciton called by clicking the send button on form view
        """
        for record in self:
            record.state = "sent"

    def action_quotation_cancel(self):
        """
        this is button action  function called by clicking the cancel button on form view
        """
        for record in self:
            record.state = "canceled"

    def action_quotation_won(self):
        """
        this is button action function called by clicking the Confirm button on form view
        """
        for record in self:
            record.state = "won"
