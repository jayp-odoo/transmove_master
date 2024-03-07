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
    _inherit = "sale.order"

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
        for record in self:
            if record.weight and record.airline_id:
                record.estimated_cost = (
                    record.airline_id.estimated_price_kg * record.weight
                )

    @api.model
    def _expand_groups(self, states, domain, order):
        return ["draft", "sent", "sale", "cancel"]

    @api.depends("estimated_cost")
    def _compute_amounts(self):
        for record in self:
            record.amount_total = record.estimated_cost
