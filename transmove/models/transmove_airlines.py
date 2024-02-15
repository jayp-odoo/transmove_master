from odoo import fields, models


class AirLines(models.Model):
    """this model is used to represent multiple types of airline companies"""

    _name = "transmove.airlines"
    _description = "this table is used to store airlines information"

    name = fields.Char(string="Airline name", required=True)
    contact_no = fields.Char(string="Contact Number", required=True)
    email = fields.Char(string="Email", required=True)
    estimated_price_kg = fields.float(string="Estimated Price per kg")
