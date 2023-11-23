# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move"]

    customer_rent_ids = fields.Many2many(
        string="Customer Rent",
        comodel_name="customer_rent_order",
        relation="rel_customer_rent_order_2_stock_move",
        column1="stock_move_id",
        column2="rent_id",
    )
