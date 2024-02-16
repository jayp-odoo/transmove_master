from odoo import api, fields, models


class TransmoveAirLines(models.Model):
    """this model is used to represent multiple types of airline companies"""

    _name = "transmove.airlines"
    _description = "this table is used to store airlines information"

    name = fields.Char(string="Airline name", required=True)
    contact_no = fields.Char(string="Contact Number", required=True)
    email = fields.Char(string="Email", required=True)
    estimated_price_kg = fields.Float(string="Estimated Price per kg")
