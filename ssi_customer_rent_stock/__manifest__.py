# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Customer Rent + Stock Integration",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_rent_stock",
        "ssi_customer_rent",
    ],
    "data": [
        "data/policy_template_data.xml",
        "views/customer_rent_type_views.xml",
        "views/customer_rent_order_views.xml",
    ],
    "demo": [],
}
