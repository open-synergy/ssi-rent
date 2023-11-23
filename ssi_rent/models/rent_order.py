# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class RentOrder(models.AbstractModel):
    _name = "rent_order"
    _inherit = [
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.transaction_open",
        "mixin.transaction_ready",
        "mixin.transaction_confirm",
        "mixin.transaction_partner_contact_required",
        "mixin.localdict",
        "mixin.product_line_account",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
        "mixin.transaction_pricelist",
    ]
    _description = "Rent Order"

    # Multiple Approval Attribute
    _approval_from_state = "ready"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_ready"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_ready_policy_fields = False
    _automatically_insert_ready_button = False

    _statusbar_visible_label = "draft,confirm,ready,open,done"
    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "done_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_open",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_ready",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "ready"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="rent_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    product_id = fields.Many2one(
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    usage_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    analytic_account_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    price_unit = fields.Monetary(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tax_ids = fields.Many2many(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    yearly_period = fields.Integer(
        string="Yearly Period",
        compute="_compute_period",
        store=True,
    )
    monthly_period = fields.Integer(
        string="Monthly Period",
        compute="_compute_period",
        store=True,
    )
    daily_period = fields.Integer(
        string="Daily Period",
        compute="_compute_period",
        store=True,
    )
    period_type = fields.Selection(
        string="Period Type",
        selection=[
            ("yearly", "Yearly"),
            ("monthly", "Monthly"),
            ("daily", "Daily"),
        ],
        default="yearly",
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    need_payment = fields.Boolean(
        string="Need Payment",
        compute="_compute_need_payment",
        store=True,
    )
    recurring_interval = fields.Integer(
        string="Recurring Interval",
        default=1,
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    invoice_number = fields.Integer(
        string="Invoice Number",
        compute="_compute_invoice_number",
        store=True,
    )
    invoice_computation_method = fields.Selection(
        string="Invoice Computation",
        selection=[("offset", "Offset"), ("fixed", "Fixed Date")],
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default="offset",
    )
    invoice_method = fields.Selection(
        string="Invoice Method",
        selection=[
            ("advance", "Advance"),
            ("arear", "Arear"),
        ],
        default="advance",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_invoice_offset = fields.Integer(
        string="Date Invoice Offset",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payment_term_id = fields.Many2one(
        string="Invoice Payment Term",
        comodel_name="base.duration",
        required=False,
        readonly=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=False,
        readonly=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payment_schedule_ids = fields.One2many(
        string="Payment Schedules",
        comodel_name="rent_order.payment_schedule",
        inverse_name="order_id",
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_currency_ids = fields.Many2many(
        comodel_name="res.currency",
        string="Allowed Currencies",
        compute="_compute_allowed_currency_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Allowed Pricelists",
        compute="_compute_allowed_pricelist_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_usage_ids = fields.Many2many(
        comodel_name="product.usage_type",
        string="Allowed Usages",
        compute="_compute_allowed_usage_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_analytic_account_ids = fields.Many2many(
        comodel_name="account.analytic.account",
        string="Allowed Analytic Accounts",
        compute="_compute_allowed_analytic_account_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "price_subtotal",
    )
    def _compute_need_payment(self):
        for record in self:
            result = False
            if record.price_subtotal > 0.0:
                result = True
            record.need_payment = result

    @api.depends(
        "date_start",
        "date_end",
    )
    def _compute_period(self):
        for record in self:
            if record.date_start and record.date_end:
                delta_date = relativedelta(record.date_end, record.date_start)
                record.yearly_period = delta_date.years
                record.monthly_period = delta_date.months
                record.daily_period = delta_date.days

    @api.depends(
        "period_type",
        "date_start",
        "date_end",
        "recurring_interval",
    )
    def _compute_invoice_number(self):
        for record in self:
            invoice_number = 0
            if (
                record.period_type
                and record.date_start
                and record.date_end
                and record.recurring_interval
            ):
                payment_term_period_number = record.recurring_interval
                period_type = record.period_type

                dt_start = record.date_start
                dt_end = record.date_end
                subscription_days = (dt_end - dt_start).days
                if period_type == "yearly":
                    conv_days = subscription_days / 365
                elif period_type == "monthly":
                    r_months = relativedelta(dt_end, dt_start)
                    conv_days = r_months.months + (12 * r_months.years)
                elif period_type == "daily":
                    conv_days = subscription_days
                else:
                    conv_days = 0
                invoice_number = conv_days / payment_term_period_number
            record.invoice_number = invoice_number

    @api.depends("type_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.type_id.product_selection_method,
                    manual_recordset=record.type_id.product_ids,
                    domain=record.type_id.product_domain,
                    python_code=record.type_id.product_python_code,
                )
            record.allowed_product_ids = result

    @api.depends("type_id")
    def _compute_allowed_currency_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.currency",
                    method_selection=record.type_id.currency_selection_method,
                    manual_recordset=record.type_id.currency_ids,
                    domain=record.type_id.currency_domain,
                    python_code=record.type_id.currency_python_code,
                )
            record.allowed_currency_ids = result

    @api.depends("type_id")
    def _compute_allowed_pricelist_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.pricelist",
                    method_selection=record.type_id.pricelist_selection_method,
                    manual_recordset=record.type_id.pricelist_ids,
                    domain=record.type_id.pricelist_domain,
                    python_code=record.type_id.pricelist_python_code,
                )
            record.allowed_pricelist_ids = result

    @api.depends("type_id")
    def _compute_allowed_usage_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.usage_type",
                    method_selection=record.type_id.usage_selection_method,
                    manual_recordset=record.type_id.usage_ids,
                    domain=record.type_id.usage_domain,
                    python_code=record.type_id.usage_python_code,
                )
            record.allowed_usage_ids = result

    @api.depends("type_id")
    def _compute_allowed_analytic_account_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.analytic.account",
                    method_selection=record.type_id.analytic_account_selection_method,
                    manual_recordset=record.type_id.analytic_account_ids,
                    domain=record.type_id.analytic_account_domain,
                    python_code=record.type_id.analytic_account_python_code,
                )
            record.allowed_analytic_account_ids = result

    @api.model
    def _get_policy_field(self):
        res = super(RentOrder, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "ready_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "type_id",
    )
    def onchange_currency_id(self):
        self.currency_id = False

    @api.onchange(
        "currency_id",
        "type_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_usage_id(self):
        self.usage_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_analytic_account_id(self):
        self.analytic_account_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_product_id(self):
        self.product_id = False

    def onchange_name(self):
        pass

    def action_create_payment_schedule(self):
        for document in self.sudo():
            document._delete_payment_schedule()
            document._create_payment_schedule()

    def _delete_payment_schedule(self):
        self.ensure_one()
        if self.payment_schedule_ids:
            for schedule in self.payment_schedule_ids:
                invoice_id = schedule.invoice_id
                schedule.write({"invoice_id": False})
                invoice_id.unlink()
            self.payment_schedule_ids.unlink()

    def _create_payment_schedule(self):
        self.ensure_one()
        PaymentSchedule = self.env[self.payment_schedule_ids._name]
        date_start = self.date_start
        for _period_num in range(1, self.invoice_number + 1):
            date_end = self._get_payment_schedule_date_end(date_start)
            date_invoice = self._get_payment_schedule_date_invoice(date_start, date_end)
            date_due = self._get_payment_schedule_date_due(date_invoice)
            data = {
                "order_id": self.id,
                "date_start": date_start,
                "date_end": date_end,
                "date_invoice": date_invoice,
                "date_due": date_due,
            }
            PaymentSchedule.create(data)
            date_start = date_end

    def _get_payment_schedule_date_due(self, date_invoice):
        self.ensure_one()
        return self.payment_term_id.get_duration(date_invoice)

    def _get_payment_schedule_date_invoice(self, date_start, date_end):
        self.ensure_one()
        if self.invoice_computation_method == "offset":
            if self.invoice_method == "advance":
                factor = relativedelta(days=(self.date_invoice_offset * -1))
                date = date_start
            else:
                factor = relativedelta(days=self.date_invoice_offset)
                date = date_end
        else:
            if self.invoice_method == "advance":
                factor = relativedelta(months=-1, day=self.date_invoice_offset)
                date = date_start
            else:
                factor = relativedelta(months=1, day=self.date_invoice_offset)
                date = date_start

        date_invoice = date + factor
        return date_invoice

    def _get_payment_schedule_date_start(self, date_end):
        self.ensure_one()

        date_start = date_end + relativedelta(days=1)
        return date_start

    def _get_payment_schedule_date_end(self, date):
        self.ensure_one()

        if self.period_type == "daily":
            add = relativedelta(days=self.recurring_interval)
        elif self.period_type == "monthly":
            add = relativedelta(months=self.recurring_interval)
        elif self.period_type == "yearly":
            add = relativedelta(years=self.recurring_interval)
        date_end = date + add
        return date_end

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
