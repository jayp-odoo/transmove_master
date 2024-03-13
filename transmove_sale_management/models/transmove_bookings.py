from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class TransmoveBookings(models.Model):
    """
    this model is responsible to handle bookings, which
    considered as most important model because it is connected with major models
    """

    _name = "transmove.bookings"
    _description = "Booking for shipment"
    _order = "priority desc"
    _inherit = ["mail.thread"]

    order_id = fields.Many2one(
        "sale.order", string="Order", required=True, ondelete="cascade"
    )
    invoice_id = fields.Many2one("account.move")
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
        """
        this method will compute the cargo pickup date with the use of order date + transit time - 3 days
        buffer time
        """
        for record in self:
            record.cargo_pickup_date = fields.Date.add(
                record.order_id.date_order, days=int(record.order_id.transit_time) - 3
            )

    @api.depends("order_id")
    def _compute_display_name(self):
        """
        this method will assign display name to it uniquely created serial number
        """
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
        """
        this button action is used to cancel the booking also we need to cancel pickup requests
        as well as custom clearance requests
        """
        for record in self:
            record.state = "cancelled"
            pickup_obj = self.env["transmove.pickup.requests"].search(
                [("bookings_id", "=", record.id)]
            )
            custom_obj = self.env["transmove.customs.clearance"].search(
                [("booking_id", "=", record.id)]
            )
            if pickup_obj and custom_obj:
                pickup_obj.state = "cancelled"
                custom_obj.state = "cancelled"

    def action_backtodraft(self):
        """
        to transfer the back to draft state we also need to change state of pickup requests and customs requests
        """
        for record in self:
            record.state = "draft"
            pickup_obj = self.env["transmove.pickup.requests"].search(
                [("bookings_id", "=", record.id)]
            )
            custom_obj = self.env["transmove.customs.clearance"].search(
                [("booking_id", "=", record.id)]
            )
            if pickup_obj and custom_obj:
                pickup_obj.state = "pending"
                custom_obj.state = "draft"

    def action_load_to_container(self):
        self.state = "load_to_container"

    def action_on_the_sky(self):
        self.state = "on_the_sky"

    def action_won(self):
        """
        once the state in won then invoice should be created with this method
        also we need invoice id to be stored for state button.
        """
        self.state = "won"
        vals = {
            "partner_id": self.customer.id,
            "move_type": "out_invoice",
            "invoice_date": (fields.Date.today()).strftime("%Y-%m-%d"),
            "currency_id": self.currency.id,
            "amount_total_signed": self.total_amount,
            "narration": "- In case of any discrepancy in the invoice, please bring the same to our attention within 7 days of receipt of invoice else the same would be treated as correct. ",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": f"From : {self.order_id.origin_city_id.name} \nTo: {self.order_id.destination_city_id.name} \nAirline : {self.airline}",
                        "quantity": 1,
                        "price_unit": self.total_amount,
                        "currency_id": self.currency.id,
                    }
                ),
                Command.create(
                    {
                        "name": "AMS Charges-T fees",
                        "quantity": 1,
                        "price_unit": 1600.00,
                        "currency_id": self.currency.id,
                    }
                ),
                Command.create(
                    {
                        "name": "Airways Bill",
                        "quantity": 1,
                        "price_unit": 900.00,
                        "currency_id": self.currency.id,
                    }
                ),
                Command.create(
                    {
                        "name": "Custom Clearance",
                        "quantity": 1,
                        "price_unit": 100.00,
                        "currency_id": self.currency.id,
                    }
                ),
                Command.create(
                    {
                        "name": "GSEC",
                        "quantity": 1,
                        "price_unit": 550.00,
                        "currency_id": self.currency.id,
                    }
                ),
            ],
        }

        moves = self.env["account.move"].create(vals)
        self.invoice_id = moves.id

    def open_invoice(self):
        """
        this method will open the particular invoice in form view with given invoice id
        and we return action in context.
        """
        if self.invoice_id:
            return {
                "type": "ir.actions.act_window",
                "name": "Invoice",
                "res_model": "account.move",
                "res_id": self.invoice_id.id,
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }
        else:
            raise UserError("Invoice not found")
