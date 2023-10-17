# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RentType(models.AbstractModel):
    _name = "rent_type"
    _inherit = ["mixin.master_data"]
    _description = "Rent Type"

    # Product
    product_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Product Selection Method",
        required=True,
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        column1="type_id",
        column2="product_id",
        string="Products",
    )
    product_domain = fields.Text(default="[]", string="Product Domain")
    product_python_code = fields.Text(
        default="result = []", string="Product Python Code"
    )
    # Currency
    currency_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Currency Selection Method",
        required=True,
    )
    currency_ids = fields.Many2many(
        comodel_name="res.currency",
        column1="type_id",
        column2="currency_id",
        string="Currencies",
    )
    currency_domain = fields.Text(default="[]", string="Currency Domain")
    currency_python_code = fields.Text(
        default="result = []", string="Currency Python Code"
    )
    # Pricelist
    pricelist_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Pricelist Selection Method",
        required=True,
    )
    pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        column1="type_id",
        column2="pricelist_id",
        string="Pricelists",
    )
    pricelist_domain = fields.Text(default="[]", string="Pricelist Domain")
    pricelist_python_code = fields.Text(
        default="result = []", string="Pricelist Python Code"
    )
    # Usage
    usage_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Usage Selection Method",
        required=True,
    )
    usage_ids = fields.Many2many(
        comodel_name="product.usage_type",
        column1="type_id",
        column2="usage_id",
        string="Usages",
    )
    usage_domain = fields.Text(default="[]", string="Usage Domain")
    usage_python_code = fields.Text(default="result = []", string="Usage Python Code")
    # Analytic
    analytic_account_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Analytic Account Selection Method",
        required=True,
    )
    analytic_account_ids = fields.Many2many(
        comodel_name="account.analytic.account",
        column1="type_id",
        column2="analytic_account_id",
        string="Analytic Accounts",
    )
    analytic_account_domain = fields.Text(
        default="[]", string="Analytic Account Domain"
    )
    analytic_account_python_code = fields.Text(
        default="result = []", string="Analytic Account Python Code"
    )
