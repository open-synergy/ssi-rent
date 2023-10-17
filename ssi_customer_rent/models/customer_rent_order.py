# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CustomerRentOrder(models.Model):
    _name = "customer_rent_order"
    _inherit = [
        "rent_order",
    ]
    _description = "Customer Rent Order"

    type_id = fields.Many2one(
        comodel_name="customer_rent_type",
    )
    payment_schedule_ids = fields.One2many(
        comodel_name="customer_rent_order.payment_schedule",
    )
