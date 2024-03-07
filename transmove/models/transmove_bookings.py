from odoo import api, fields, models


class TransmoveBookings(models.Model):
    _name = "transmove.bookings"
    _description = "Booking for shipment"

    order_id = fields.Many2one(
        "sale.order", string="Order", required=True, ondelete="cascade"
    )
    airway_bill_number = fields.Char(string="Airway Bill Number")
    departure_date = fields.Date(string="Departure Date")
    arrival_date = fields.Date(string="Arrival Date")
    shipment_description = fields.Text(string="Shipment Description")
    customs_clearance_date = fields.Date(string="Customs Clearance Date")
    documentation_submitted = fields.Boolean(string="Documentation Submitted")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Airline Confirmed"),
            ("custom_cleared", "Custom Cleared"),
            ("cancelled", "Cancelled"),
        ],
        string="state",
        default="draft",
    )
