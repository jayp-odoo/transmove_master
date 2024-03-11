from odoo import api, fields, models


class TransmovePickupRequests(models.Model):
    """
    this class represents the all pickup requests created when order has been won
    """

    _name = "transmove.pickup.requests"

    bookings_id = fields.Many2one(
        "transmove.bookings", required=True, ondelete="cascade"
    )
    vehicle_id = fields.Many2one("fleet.vehicle")
    driver_id = fields.Many2one(related="vehicle_id.driver_id")
    pickup_date = fields.Date(related="bookings_id.cargo_pickup_date")
    state = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
        group_expand="_expand_groups",
    )

    def write(self, vals):
        """
        this method is called when we are dragging the kanban card
        if state to completed then also write booking id state to received at origin
        """
        if "state" in vals:
            if vals["state"] == "completed":
                self.bookings_id.state = "received_at_origin"
        return super(TransmovePickupRequests, self).write(vals)

    @api.model
    def _expand_groups(self, states, domain, order):
        return ["pending", "scheduled", "completed", "cancelled"]

    def action_scheduled(self):
        """
        this is button action to change state to pickup scheduled
        """
        self.state = "scheduled"

    def action_complete(self):
        """
        this button action is used to change state to complete
        """
        self.state = "completed"

    def action_cancel(self):
        """
        this button action is used to change state to cancelled
        """
        self.state = "cancelled"

    def action_back_to_pending(self):
        """
        this button action is used to change state back to pending
        """
        self.state = "pending"
