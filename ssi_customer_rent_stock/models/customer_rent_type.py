# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CustomerRentType(models.Model):
    _name = "customer_rent_type"
    _inherit = [
        "rent_type_stock",
        "customer_rent_type",
    ]
    _description = "Customer Rent Type"

    inbound_warehouse_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_inbound_warehouse",
    )
    outbound_warehouse_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_outbound_warehouse",
    )
    inbound_route_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_inbound_route",
    )
    outbound_route_ids = fields.Many2many(
        relation="rel_customer_rent_type_2_outbound_route",
    )
