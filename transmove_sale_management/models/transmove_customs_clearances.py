from odoo import api, fields, models


class CustomsClearance(models.Model):
    """
    this model will store information about the custom clearance requests
    """

    _name = "transmove.customs.clearance"
    _description = "Customs Clearance"

    booking_id = fields.Many2one(
        "transmove.bookings", string="Booking", required=True, ondelete="cascade"
    )
    customs_clearance_date = fields.Date(string="Customs Clearance Date")
    documentation_submitted = fields.Boolean(string="Documentation Submitted")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("rejected", "Rejected"),
            ("cancelled", "Cancelled"),
        ],
        string="Clearance Status",
        default="draft",
        group_expand="_expand_groups",
    )

    @api.model
    def _expand_groups(self, states, domain, order):
        return ["draft", "confirmed", "rejected", "cancelled"]

    def action_confirm(self):
        self.state = "confirmed"
        self.booking_id.state = "custom_cleared"

    def action_reject(self):
        self.state = "rejected"

    def action_cancel(self):
        self.state = "cancelled"

    def action_back_to_draft(self):
        self.state = "draft"
