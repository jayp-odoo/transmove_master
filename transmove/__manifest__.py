{
    "name": "transmove",
    "depends": ["base", "mail", "base_address_extended"],
    "data": [
        "security/ir.model.access.csv",
        "views/transmove_quotations_views.xml",
        "views/transmove_airlines_views.xml",
        "views/transmove_menus.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": True,
}
