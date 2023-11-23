# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Rent Management",
    "version": "14.0.2.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "configuration_helper",
        "ssi_master_data_mixin",
        "ssi_company_currency_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_ready_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_date_duration_mixin",
        "ssi_transaction_terminate_mixin",
        "ssi_transaction_partner_mixin",
        "ssi_transaction_pricelist_mixin",
        "ssi_product_line_account_mixin",
        "ssi_m2o_configurator_mixin",
        "base_duration",
        "ssi_financial_accounting",
        "ssi_localdict_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "menu.xml",
        "views/rent_type_views.xml",
        "views/rent_order_views.xml",
    ],
    "demo": [],
}
