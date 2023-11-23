# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Rent + Inventory Integration",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_rent",
        "ssi_stock_rent_operation",
        "ssi_stock_warehouse_m2o_configurator_mixin",
        "ssi_stock_route_m2o_configurator_mixin",
        "ssi_stock_location_m2o_configurator_mixin",
    ],
    "data": [],
    "demo": [],
}
