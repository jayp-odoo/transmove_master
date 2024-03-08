from odoo import api, fields, models


class TransmovePickupRequests(models.Model):
    _name = "transmove.pickup.requests"

    bookings_id = fields.Many2one(
        "transmove.bookings", required=True, ondelete="cascade"
    )
    vehicle_id = fields.Many2one("fleet.vehicle")
    pickup_date = fields.Date(related="bookings_id.cargo_pickup_date")
    state = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
        ],
        default="pending",
        group_expand="_expand_groups",
    )

    # @api.onchange("state")
    # def _onchange_state(self):
    #     if self.state == "completed":
    #         self.bookings_id.state = "received_at_origin"
    #         print(" reached ".center(100, "="))

    def write(self, vals):
        if "state" in vals:
            if vals["state"] == "completed":
                self.bookings_id.state = "received_at_origin"
            return super(TransmovePickupRequests, self).write(vals)

    @api.model
    def _expand_groups(self, states, domain, order):
        return ["pending", "scheduled", "completed"]
