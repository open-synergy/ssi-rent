# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class RentTypeStock(models.AbstractModel):
    _name = "rent_type_stock"
    _inherit = [
        "rent_type",
        "mixin.inbound_stock_warehouse_m2o_configurator",
        "mixin.outbound_stock_warehouse_m2o_configurator",
        "mixin.inbound_stock_route_m2o_configurator",
        "mixin.outbound_stock_route_m2o_configurator",
        "mixin.inbound_stock_location_m2o_configurator",
        "mixin.outbound_stock_location_m2o_configurator",
    ]
    _description = "Customer Rent Type"

    _inbound_stock_warehouse_m2o_configurator_insert_form_element_ok = True
    _inbound_stock_warehouse_m2o_configurator_form_xpath = "//page[@name='inventory']"
    _outbound_stock_warehouse_m2o_configurator_insert_form_element_ok = True
    _outbound_stock_warehouse_m2o_configurator_form_xpath = "//page[@name='inventory']"
    _inbound_stock_route_m2o_configurator_insert_form_element_ok = True
    _inbound_stock_route_m2o_configurator_form_xpath = "//page[@name='inventory']"
    _outbound_stock_route_m2o_configurator_insert_form_element_ok = True
    _outbound_stock_route_m2o_configurator_form_xpath = "//page[@name='inventory']"
    _inbound_stock_location_m2o_configurator_insert_form_element_ok = True
    _inbound_stock_location_m2o_configurator_form_xpath = "//page[@name='inventory']"
    _outbound_stock_location_m2o_configurator_insert_form_element_ok = True
    _outbound_stock_location_m2o_configurator_form_xpath = "//page[@name='inventory']"
