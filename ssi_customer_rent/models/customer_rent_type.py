# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CustomerRentType(models.Model):
    _name = "customer_rent_type"
    _inherit = ["rent_type"]
    _description = "Customer Rent Type"

    product_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_product",
    )
    currency_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_currency",
    )
    usage_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_usage",
    )
    analytic_account_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_analytic_account",
    )
