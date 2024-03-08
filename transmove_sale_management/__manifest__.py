{
    "name": "transmove_sale_management",
    "depends": ["transmove", "sale_management", "website", "crm", "fleet"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/transmove_bookings_views.xml",
        "views/transmove_documents_views.xml",
        "views/transmove_pickup_requests_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
