# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RentOrderPaymentSchedule(models.AbstractModel):
    _name = "rent_order.payment_schedule"
    _description = "Rent Order -  Payment Schedule"

    order_id = fields.Many2one(
        string="# Subscription",
        comodel_name="rent_order",
        required=True,
        ondelete="cascade",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    date_invoice = fields.Date(
        string="Date Invoice",
        required=True,
    )
    date_due = fields.Date(
        string="Date Due",
        required=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
        related="move_line_id.move_id",
        store=True,
    )
    move_line_id = fields.Many2one(
        string="Journal Item",
        comodel_name="account.move.line",
        readony=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="move_line_id.currency_id",
        store=True,
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        related="invoice_id.amount_untaxed",
        store=True,
    )
    amount_tax = fields.Monetary(
        string="Tax",
        related="invoice_id.amount_tax",
        store=True,
    )
    amount_total = fields.Monetary(
        string="Total ",
        related="invoice_id.amount_total",
        store=True,
    )
    residual = fields.Monetary(
        string="Total ",
        related="invoice_id.amount_residual",
        store=True,
    )
    no_invoice = fields.Boolean(
        string="No Invoice",
        readonly=True,
    )
    manual = fields.Boolean(
        string="Manually Controlled",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("noinvoice", "No Invoice"),
            ("invoiced", "Invoiced"),
            ("cancelled", "Cancelled"),
            ("free", "Free"),
            ("manual", "Manually Controlled"),
        ],
        compute="_compute_state",
        store=True,
    )

    @api.depends(
        "invoice_id",
        "order_id.state",
        "no_invoice",
        "manual",
    )
    def _compute_state(self):
        for record in self:
            if record.order_id.state in ["draft", "confirm", "reject", "cancel"]:
                state = "draft"
            elif record.order_id.state in ["open", "close"]:
                if record.invoice_id:
                    state = "invoiced"
                elif record.no_invoice:
                    state = "free"
                elif record.manual:
                    state = "manual"
                elif record.order_id.state == "close" and not record.invoice_id:
                    state = "noinvoice"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    def action_create_invoice(self):
        for record in self.sudo():
            record._create_invoice()

    def action_delete_invoice(self):
        for record in self.sudo():
            record._delete_invoice()

    def action_disconnect_invoice(self):
        for record in self.sudo():
            record._disconnect_invoice()

    def action_mark_as_free(self):
        for record in self.sudo():
            record._mark_as_free()

    def action_mark_as_must_pay(self):
        for record in self.sudo():
            record._mark_as_must_pay()

    def action_manually_controlled(self):
        for record in self.sudo():
            record._manually_controlled()

    def action_no_manual(self):
        for record in self.sudo():
            record._no_manual()

    def _mark_as_free(self):
        self.ensure_one()
        self.write(
            {
                "no_invoice": True,
            }
        )

    def _mark_as_must_pay(self):
        self.ensure_one()
        self.write(
            {
                "no_invoice": False,
            }
        )

    def _manually_controlled(self):
        self.ensure_one()
        self.write(
            {
                "manual": True,
            }
        )

    def _no_manual(self):
        self.ensure_one()
        self.write(
            {
                "manual": False,
            }
        )

    def _disconnect_invoice(self):
        self.ensure_one()
        self.write(
            {
                "invoice_id": False,
            }
        )

    def _create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            error_msg = _("There is already an invoice")
            raise UserError(error_msg)
        AM = self.env["account.move"]
        invoice = AM.create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )
        return True

    def _prepare_invoice_data(self):
        self.ensure_one()
        order = self.order_id
        lines = []
        lines += self._prepare_invoice_line()
        return {
            "date": self.date_invoice,
            "ref": order.name,
            "move_type": "out_invoice",
            "journal_id": order.journal_id.id,
            "partner_id": order.contact_partner_id.id,
            "currency_id": order.currency_id.id,
            "invoice_user_id": order.user_id.id,
            "invoice_date": self.date_invoice,
            "invoice_date_due": self.date_due,
            "invoice_origin": order.name,
            "invoice_payment_term_id": False,
            "invoice_line_ids": lines,
            "payment_reference": order.name,
        }

    def _prepare_invoice_line(self):
        self.ensure_one()
        order = self.order_id
        aa = order.analytic_account_id and order.analytic_account_id.id

        return [
            (
                0,
                0,
                {
                    "product_id": order.product_id.id,
                    "name": order.product_id.name,
                    "account_id": order.account_id.id,
                    "quantity": order.uom_quantity,
                    "product_uom_id": order.uom_id.id,
                    "price_unit": order.price_unit,
                    "tax_ids": [(6, 0, order.tax_ids.ids)],
                    "analytic_account_id": aa and aa.id or False,
                },
            )
        ]

    def _get_partner(self):
        self.ensure_one()
        result = self.subscription_id.contact_invoice_id

        if not result:
            result = self.subscription_id.partner_id

        return result

    def _get_receivable_journal(self):
        self.ensure_one()
        error_msg = _("No receivable journal defined")
        if not self.subscription_id.template_id.journal_id:
            raise UserError(error_msg)

        return self.subscription_id.template_id.journal_id

    def _get_receivable_account(self):
        self.ensure_one()
        error_msg = _("No receivable account defined")
        if not self.subscription_id.partner_id.property_account_receivable_id:
            raise UserError(error_msg)
        return self.subscription_id.partner_id.property_account_receivable_id

    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        if invoice.state == "draft":
            self.write({"invoice_id": False})
            invoice.unlink()
        else:
            msg_err = _("Only invoice with draft state can be deleted")
            raise UserError(msg_err)
        return True
