from odoo import api, fields, models


class TransmoveBookings(models.Model):
    _name = "transmove.bookings"
    _description = "Booking for shipment"

    order_id = fields.Many2one(
        "sale.order", string="Order", required=True, ondelete="cascade"
    )
    consignee = fields.Many2one("res.partner", string="Receiver/Consignee")
    customer = fields.Many2one(string="Customer", related="order_id.partner_id")
    t_time = fields.Char("Transit time", related="order_id.transit_time")
    airline = fields.Char("Airline", related="order_id.airline_id.name")
    type_of_good = fields.Selection("Type Of Good", related="order_id.type_of_goods")
    currency = fields.Many2one(related="order_id.currency_id")
    user = fields.Many2one(related="order_id.user_id")
    priority = fields.Selection("Priority", related="order_id.priority")
    total_amount = fields.Monetary(
        "Total Amount",
        related="order_id.amount_total",
        currency_field="currency",
    )
    origin_city = fields.Many2one(
        string="Origin City", related="order_id.origin_city_id"
    )
    destination_city = fields.Many2one(
        string="Destination City", related="order_id.destination_city_id"
    )
    airway_bill_number = fields.Char(string="Airway Bill Number")
    document_ids = fields.One2many(
        "transmove.documents", "booking_id", string="Documents"
    )
    departure_date = fields.Date(
        string="Departure Date", help="Date of departure for Airplane"
    )
    arrival_date = fields.Date(
        string="Arrival Date", help="Date of arrival to the destination"
    )
    cargo_pickup_date = fields.Date(
        "Cargo pickup date",
        help="Date of cargo pickup from Shipper with (order date + (transit_time - 3 working days))",
        compute="_compute_cargo_pickup_date",
        readonly=False,
        store=True,
    )
    shipment_description = fields.Text(string="Shipment Description")
    customs_clearance_date = fields.Date(string="Customs Clearance Date")
    documentation_submitted = fields.Boolean(string="Documentation Submitted")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Airline Confirmed"),
            ("custom_cleared", "Custom Cleared"),
            ("cancelled", "Cancelled"),
            ("received_at_origin", "Received At Origin"),
            ("load_to_container", "Loaded into Container"),
            ("on_the_sky", "On the Sky"),
            ("won", "Unloaded & Delivered to Consignee"),
        ],
        string="Status",
        default="draft",
        group_expand="_expand_groups",
    )

    @api.depends("order_id")
    def _compute_cargo_pickup_date(self):
        for record in self:
            record.cargo_pickup_date = fields.Date.add(
                record.order_id.date_order, days=int(record.order_id.transit_time) - 3
            )

    @api.depends("order_id")
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.order_id.name

    @api.model
    def _expand_groups(self, states, domain, order):
        return [
            "draft",
            "confirmed",
            "received_at_origin",
            "load_to_container",
            "custom_cleared",
            "on_the_sky",
            "won",
            "cancelled",
        ]

    def action_airline_confirm(self):
        for record in self:
            record.state = "confirmed"

    def action_airline_custom_cleared(self):
        for record in self:
            record.state = "custom_cleared"

    def action_cancelled(self):
        for record in self:
            record.state = "cancelled"

    def action_backtodraft(self):
        for record in self:
            record.state = "draft"