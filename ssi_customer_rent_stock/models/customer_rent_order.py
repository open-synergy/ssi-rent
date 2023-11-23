# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CustomerRentOrder(models.Model):
    _name = "customer_rent_order"
    _inherit = ["rent_order_stock", "customer_rent_order"]

    stock_move_ids = fields.Many2many(
        relation="rel_customer_rent_order_2_stock_move",
    )

    def _get_receipt_procurement_data(self):
        _super = super(CustomerRentOrder, self)
        result = _super._get_receipt_procurement_data()
        location = self.inbound_location_id
        result.update(
            {
                "location_id": location,
                "customer_rent_ids": [(4, self.id)],
            }
        )
        return result

    def _get_delivery_procurement_data(self):
        _super = super(CustomerRentOrder, self)
        result = _super._get_delivery_procurement_data()
        location = self.partner_id.customer_rent_location_id
        result.update(
            {
                "location_id": location,
                "customer_rent_ids": [(4, self.id)],
            }
        )
        return result
