from odoo import models, fields, api, _


class AccountPaymentDue(models.Model):
    _name = 'account.payment.due'

    partner_id = fields.Many2one('res.partner', string="Customer")
    invoice_ids = fields.Many2many('account.move')
    state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid')], default="draft", string="State",
                             compute="_compute_state")

    def _compute_state(self):
        for rec in self:
            invoice_ids = rec.invoice_ids
            result = 0
            for line in invoice_ids:
                if line.payment_state == "paid":
                    result = 1
                else:
                    result = 0
                    break
            if result == 1:
                rec.state = "paid"
            else:
                rec.state = "draft"

    @api.onchange('partner_id')
    def _onachneg_partner_id(self):
        if self.partner_id:
            due_invoices = self.env['account.move'].search(
                [('partner_id', '=', self.partner_id.id), ('payment_state', '!=', 'paid'),
                 ('move_type', '=', 'in_invoice')])
            if due_invoices:
                self.invoice_ids = due_invoices.ids

    def action_view_due_statements(self):
        due_invoices = self.env['account.move'].search(
            [('partner_id', '=', self.partner_id.id), ('payment_state', '!=', 'paid'),
             ('move_type', '=', 'out_invoice')]).invoice_line_ids.mapped('id')
        return {
            'res_model': 'account.move.line',
            'type': 'ir.actions.act_window',
            'name': 'Due Statements',
            'view_mode': 'tree,form',
            'views':
                [(self.env.ref('multiple_payment_for_outstanding_dues'
                               '.account_move_line_view_tree').id,
                  'list'),
                 (self.env.ref('account.view_move_line_form').id, 'form')],
            'context': {'create': False,
                        'search_default_group_by_invoices': True},
            'domain': [('id', 'in', due_invoices)],
        }

    def action_register_payment(self):
        """ Open the account.payment.register wizard to pay the selected
        journal entries.
        :return: An action opening the account.payment.register wizard.
        """
        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.invoice_ids.filtered(lambda r: r.select).ids
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }


class AccountMove(models.Model):
    _inherit = "account.move"

    select = fields.Boolean(string="Select")
