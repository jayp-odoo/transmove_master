from odoo import models, fields

goods_type = [
    ("general cargo", "General Cargo"),
    ("perishable goods", "Perishable Goods"),
    ("hazardous materials", "Hazardous Materials"),
    ("temperature-controlled goods", "Temperature-Controlled Goods"),
    ("oversized or heavy Cargo", "Oversized or Heavy Cargo"),
    ("livestock and animals", "Livestock and Animals"),
    ("personal effects and household goods", "Personal Effects and Household Goods"),
]


class Quotations(models.Model):
    """this class is used to store the quotations created by administration"""

    _name = "transmove.quotations"
    _description = "this table is used to store Quotations information"

    customer_id = fields.Many2one("res.partner", string="Customer")
    origin = fields.Char(string="Origin")
    destination = fields.Char(string="Destination")
    mode_of_transport = fields.Selection(
        selection=[("air", "Air"), ("sea", "Sea")], default="air"
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
    estimated_cost = fields.Float(string="Estimated Cost", required=True)
    transit_time = fields.Char(
        string="Transit Time (in days)",
        required=True,
    )
    status = fields.Selection(
        selection=[
            ("approved", "Approved"),
            ("cancelled", "Cancelled"),
            ("pending", "Pending"),
        ],
        default="pending",
    )
    # airline_company =
