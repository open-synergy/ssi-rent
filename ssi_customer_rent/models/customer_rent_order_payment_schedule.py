# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CustomerRentOrderPaymentSchedule(models.Model):
    _name = "customer_rent_order.payment_schedule"
    _inherit = [
        "rent_order.payment_schedule",
    ]
    _description = "Customer Rent Order - Payment Schedule"

    order_id = fields.Many2one(
        comodel_name="customer_rent_order",
    )
