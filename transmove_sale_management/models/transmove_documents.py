from odoo import api, fields, models


class TransmoveDocuments(models.Model):
    _name = "transmove.documents"
    _description = "this table is used to store Documents related to bookings"

    name = fields.Selection(
        string="Document Name",
        selection=[
            ("bill_of_landing", "Bill of landing"),
            ("packing_list", "Packing list"),
            ("airway_bill", "Airway bill"),
        ],
    )
    file = fields.Binary("File")
    booking_id = fields.Many2one("transmove.bookings", ondelete="cascade")
