{
    "name": "transmove",
    "depends": ["base", "mail", "base_address_extended", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/transmove_bookings_views.xml",
        "views/transmove_quotations_views.xml",
        "views/transmove_airlines_views.xml",
        "views/transmove_orders_views.xml",
        "views/transmove_menus.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": True,
}
