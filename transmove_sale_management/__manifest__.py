{
    "name": "transmove_sale_management",
    "depends": [
        "base",
        "transmove",
        "sale_management",
        "website",
        "crm",
        "fleet",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/transmove_bookings_views.xml",
        "views/transmove_documents_views.xml",
        "views/transmove_pickup_requests_views.xml",
        "views/transmove_customs_clearances_views.xml",
        "report/sale_order_invoice_report_template.xml",
    ],
    "installable": True,
    "auto_install": True,
}
