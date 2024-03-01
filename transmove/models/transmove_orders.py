from odoo import api, fields, models
from datetime import date


class TransmoveOrders(models.Model):
    _name = "transmove.orders"
    _description = "this table is used to store Orders information"

    quotation_id = fields.Many2one("transmove.quotations", "Quotation Id")
    delivery_date = fields.Date(compute="_compute_delivery_date", readonly=False)
    special_instructions = fields.Text("Special Instructions")

    @api.depends("quotation_id.transit_time")
    def _compute_delivery_date(self):
        for record in self:
            if record.quotation_id.transit_time:
                record.delivery_date = fields.Date.add(
                    date.today(), days=int(record.quotation_id.transit_time)
                )
