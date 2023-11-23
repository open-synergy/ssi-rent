# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class RentOrderStock(models.AbstractModel):
    _name = "rent_order_stock"
    _inherit = [
        "rent_order",
    ]
    _description = "Rent Order + Stock Integration"

    need_inventory_setting = fields.Boolean(
        string="Need Inventory Setting",
        compute="_compute_need_inventory_setting",
        store=True,
    )
    need_lot = fields.Boolean(
        string="Need Lot",
        compute="_compute_need_lot",
        store=True,
    )
    lot_id = fields.Many2one(
        string="# Serial Number",
        comodel_name="stock.production.lot",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_lot_ids = fields.Many2many(
        string="Allowed Lot",
        comodel_name="stock.production.lot",
        compute="_compute_allowed_lot_ids",
        store=False,
    )
    outbound_warehouse_id = fields.Many2one(
        string="Outbound Warehouse",
        comodel_name="stock.warehouse",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    inbound_warehouse_id = fields.Many2one(
        string="Inbound Warehouse",
        comodel_name="stock.warehouse",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    outbound_route_id = fields.Many2one(
        string="Outbound Route",
        comodel_name="stock.location.route",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    outbound_location_id = fields.Many2one(
        string="Outbound Location",
        comodel_name="stock.location",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    inbound_route_id = fields.Many2one(
        string="Inbound Route",
        comodel_name="stock.location.route",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    inbound_location_id = fields.Many2one(
        string="Inbound Location",
        comodel_name="stock.location",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    procurement_group_id = fields.Many2one(
        string="Procurement Group",
        comodel_name="procurement.group",
        readonly=True,
    )
    stock_move_ids = fields.Many2many(
        string="Stock Moves",
        comodel_name="stock.move",
        column1="rent_id",
        column2="stock_move_id",
        readonly=True,
    )
    qty_to_receive = fields.Float(
        string="Qty to Receive", compute="_compute_qty_to_receive", store=True
    )
    qty_incoming = fields.Float(
        string="Qty Incoming", compute="_compute_qty_incoming", store=True
    )
    qty_received = fields.Float(
        string="Qty Received", compute="_compute_qty_received", store=True
    )
    qty_to_deliver = fields.Float(
        string="Qty to Deliver", compute="_compute_qty_to_deliver", store=True
    )
    qty_outgoing = fields.Float(
        string="Qty Outgoing", compute="_compute_qty_outgoing", store=True
    )
    qty_delivered = fields.Float(
        string="Qty Delivered", compute="_compute_qty_delivered", store=True
    )
    create_reception_ok = fields.Boolean(
        string="Create Reception",
        compute="_compute_create_picking",
        store=False,
    )
    create_delivery_ok = fields.Boolean(
        string="Create Delivery",
        compute="_compute_create_picking",
        store=False,
    )
    allowed_inbound_warehouse_ids = fields.Many2many(
        comodel_name="stock.warehouse",
        string="Allowed Inbound Warehouses",
        compute="_compute_allowed_inbound_warehouse_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_inbound_route_ids = fields.Many2many(
        comodel_name="stock.location.route",
        string="Allowed Inbound Routes",
        compute="_compute_allowed_inbound_route_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_inbound_location_ids = fields.Many2many(
        comodel_name="stock.location",
        string="Allowed Inbound Locations",
        compute="_compute_allowed_inbound_location_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_outbound_warehouse_ids = fields.Many2many(
        comodel_name="stock.warehouse",
        string="Allowed Outbound Warehouses",
        compute="_compute_allowed_outbound_warehouse_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_outbound_route_ids = fields.Many2many(
        comodel_name="stock.location.route",
        string="Allowed Outbound Routes",
        compute="_compute_allowed_outbound_route_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_outbound_location_ids = fields.Many2many(
        comodel_name="stock.location",
        string="Allowed Outbound Locations",
        compute="_compute_allowed_outbound_location_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "product_id",
    )
    def _compute_need_lot(self):
        for record in self:
            result = False
            if record.product_id and record.product_id.tracking == "serial":
                result = True
            record.need_lot = result

    @api.depends("product_id")
    def _compute_need_inventory_setting(self):
        for record in self:
            result = False

            if record.product_id.type == "product":
                result = True

            record.need_inventory_setting = result

    @api.depends("type_id")
    def _compute_allowed_inbound_warehouse_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.warehouse",
                    method_selection=record.type_id.inbound_warehouse_selection_method,
                    manual_recordset=record.type_id.inbound_warehouse_ids,
                    domain=record.type_id.inbound_warehouse_domain,
                    python_code=record.type_id.inbound_warehouse_python_code,
                )
            record.allowed_inbound_warehouse_ids = result

    @api.depends("type_id", "inbound_warehouse_id")
    def _compute_allowed_inbound_route_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.location.route",
                    method_selection=record.type_id.inbound_route_selection_method,
                    manual_recordset=record.type_id.inbound_route_ids,
                    domain=record.type_id.inbound_route_domain,
                    python_code=record.type_id.inbound_route_python_code,
                )
            record.allowed_inbound_route_ids = result

    @api.depends("type_id", "inbound_warehouse_id")
    def _compute_allowed_inbound_location_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.location",
                    method_selection=record.type_id.inbound_location_selection_method,
                    manual_recordset=record.type_id.inbound_location_ids,
                    domain=record.type_id.inbound_location_domain,
                    python_code=record.type_id.inbound_location_python_code,
                )
            record.allowed_inbound_location_ids = result

    @api.depends("type_id")
    def _compute_allowed_outbound_warehouse_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.warehouse",
                    method_selection=record.type_id.outbound_warehouse_selection_method,
                    manual_recordset=record.type_id.outbound_warehouse_ids,
                    domain=record.type_id.outbound_warehouse_domain,
                    python_code=record.type_id.outbound_warehouse_python_code,
                )
            record.allowed_outbound_warehouse_ids = result

    @api.depends("type_id", "outbound_warehouse_id")
    def _compute_allowed_outbound_route_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.location.route",
                    method_selection=record.type_id.outbound_route_selection_method,
                    manual_recordset=record.type_id.outbound_route_ids,
                    domain=record.type_id.outbound_route_domain,
                    python_code=record.type_id.outbound_route_python_code,
                )
            record.allowed_outbound_route_ids = result

    @api.depends("type_id", "outbound_warehouse_id")
    def _compute_allowed_outbound_location_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.location",
                    method_selection=record.type_id.outbound_location_selection_method,
                    manual_recordset=record.type_id.outbound_location_ids,
                    domain=record.type_id.outbound_location_domain,
                    python_code=record.type_id.outbound_location_python_code,
                )
            record.allowed_outbound_location_ids = result

    @api.depends(
        "product_id",
        "outbound_location_id",
    )
    def _compute_allowed_lot_ids(self):
        Quant = self.env["stock.quant"]
        for record in self:
            result = False
            if record.product_id and record.outbound_location_id:
                criteria = [
                    ("product_id", "=", record.product_id.id),
                    ("location_id", "=", record.outbound_location_id.id),
                ]
                result = Quant.search(criteria).mapped("lot_id")
            record.allowed_lot_ids = result

    @api.depends(
        "qty_to_receive",
        "qty_to_deliver",
        "state",
    )
    def _compute_create_picking(self):
        for record in self:
            record.create_reception_ok = record.create_delivery_ok = False
            if record.qty_to_receive > 0.0 and record.state == "open":
                record.create_reception_ok = True
            if record.qty_to_deliver > 0.0 and record.state == "open":
                record.create_delivery_ok = True

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "uom_quantity",
        "qty_incoming",
        "qty_received",
        "qty_delivered",
    )
    def _compute_qty_to_receive(self):
        for record in self:
            record.qty_to_receive = (
                record.qty_delivered - record.qty_incoming - record.qty_received
            )

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_incoming(self):
        for record in self:
            states = [
                "draft",
                "waiting",
                "confirmed",
                "partially_available",
                "assigned",
            ]
            record.qty_incoming = record._get_move_qty(states, "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_received(self):
        for record in self:
            states = [
                "done",
            ]
            record.qty_received = record._get_move_qty(states, "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "uom_quantity",
        "qty_outgoing",
        "qty_delivered",
    )
    def _compute_qty_to_deliver(self):
        for record in self:
            record.qty_to_deliver = 1.0 - record.qty_outgoing - record.qty_delivered

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_outgoing(self):
        for record in self:
            states = [
                "draft",
                "waiting",
                "confirmed",
                "partially_available",
                "assigned",
            ]
            record.qty_outgoing = record._get_move_qty(states, "out")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_delivered(self):
        for record in self:
            states = [
                "done",
            ]
            record.qty_delivered = record._get_move_qty(states, "out")

    @api.onchange(
        "type_id",
    )
    def onchange_inbound_warehouse_id(self):
        self.inbound_warehouse_id = False

    @api.onchange(
        "type_id",
        "inbound_warehouse_id",
    )
    def onchange_inbound_route_id(self):
        self.inbound_route_id = False

    @api.onchange(
        "type_id",
        "inbound_warehouse_id",
    )
    def onchange_inbound_location_id(self):
        self.inbound_location_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_outbound_warehouse_id(self):
        self.outbound_warehouse_id = False

    @api.onchange(
        "type_id",
        "outbound_warehouse_id",
    )
    def onchange_outbound_route_id(self):
        self.outbound_route_id = False

    @api.onchange(
        "product_id",
        "outbound_location_id",
    )
    def onchange_lot_id(self):
        self.lot_id = False

    def _get_move_qty(self, states, direction):
        result = 0.0
        location = self.inbound_location_id
        if direction == "in":
            for move in self.stock_move_ids.filtered(
                lambda m: m.state in states and m.location_dest_id == location
            ):
                result += move.product_qty
        else:
            for move in self.stock_move_ids.filtered(
                lambda m: m.state in states and m.location_id == location
            ):
                result += move.product_qty
        return result

    def action_create_reception(self):
        for record in self.sudo():
            record._create_reception()

    def action_create_delivery(self):
        for record in self.sudo():
            record._create_delivery()

    @ssi_decorator.post_open_action()
    def _create_procurement_group(self):
        self.ensure_one()

        if self.procurement_group_id:
            return True

        PG = self.env["procurement.group"]
        group = PG.create(self._prepare_create_procurement_group())
        self.write(
            {
                "procurement_group_id": group.id,
            }
        )

    def _prepare_create_procurement_group(self):
        self.ensure_one()
        return {
            "name": self.name,
            "partner_id": self.partner_id.id,
        }

    def _create_reception(self):
        self.ensure_one()
        group = self.procurement_group_id
        qty = 1.0
        values = self._get_receipt_procurement_data()

        procurements = []
        try:
            procurement = group.Procurement(
                self.product_id,
                qty,
                self.product_id.uom_id,
                values.get("location_id"),
                values.get("origin"),
                values.get("origin"),
                self.env.company,
                values,
            )

            procurements.append(procurement)
            self.env["procurement.group"].with_context(rma_route_check=[True]).run(
                procurements
            )
        except UserError as error:
            raise UserError(error)

    def _create_delivery(self):
        self.ensure_one()
        group = self.procurement_group_id
        qty = 1.0
        values = self._get_delivery_procurement_data()

        procurements = []
        try:
            procurement = group.Procurement(
                self.product_id,
                qty,
                self.product_id.uom_id,
                values.get("location_id"),
                values.get("origin"),
                values.get("origin"),
                self.env.company,
                values,
            )

            procurements.append(procurement)
            self.env["procurement.group"].with_context(rma_route_check=[True]).run(
                procurements
            )
        except UserError as error:
            raise UserError(error)

    def _get_receipt_procurement_data(self):
        group = self.procurement_group_id
        origin = self.name
        warehouse = self.inbound_warehouse_id
        route = self.inbound_route_id
        result = {
            "name": origin,
            "group_id": group,
            "origin": origin,
            "warehouse_id": warehouse,
            "date_planned": fields.Datetime.now(),
            "product_id": self.product_id.id,
            "product_qty": 1.0,
            "partner_id": self.partner_id.id,
            "product_uom": self.product_id.uom_id.id,
            "route_ids": route,
            "price_unit": self.price_unit,
            "forced_lot_id": self.lot_id and self.lot_id.id,
        }
        return result

    def _get_delivery_procurement_data(self):
        group = self.procurement_group_id
        origin = self.name
        warehouse = self.outbound_warehouse_id
        route = self.outbound_route_id
        result = {
            "name": self.name,
            "group_id": group,
            "origin": origin,
            "warehouse_id": warehouse,
            "date_planned": fields.Datetime.now(),
            "product_id": self.product_id.id,
            "product_qty": 1.0,
            "partner_id": self.partner_id.id,
            "product_uom": self.product_id.uom_id.id,
            "route_ids": route,
            "forced_lot_id": self.lot_id and self.lot_id.id,
        }
        return result
