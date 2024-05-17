from odoo import models, fields, api, _
from num2words import num2words


class AccountMove(models.Model):
    _inherit = "account.move"

    row_check = fields.Integer(compute="compute_row_check")
    amount_in_words = fields.Char(compute="compute_amount_in_words")

    def compute_row_check(self):
        for rec in self:
            if rec.invoice_line_ids:
                rec.row_check = 9 - len(rec.invoice_line_ids)

    def compute_amount_in_words(self):
        for rec in self:
            rec.amount_in_words = num2words(rec.amount_residual)

    @api.depends('posted_before', 'state', 'journal_id', 'date', 'payment_state')
    def _compute_name(self):
        """ OVERRIDE """
        self = self.sorted(lambda m: (m.date, m.ref or '', m.id))
        print('\n\n\nSELF', self)

        for move in self:
            print('\n\n\nmove.name', move.name)
            if move.payment_state == "partial" and (move.name.startswith("INV") or move.name.startswith("PINV")) and not move.ref:
                partial_seq = move.env['ir.sequence'].sudo().next_by_code('invoice.partial.payment')
                move.name = partial_seq
                continue
            if move.state == 'cancel':
                continue

            move_has_name = move.name and move.name != '/'
            if move_has_name and move.name.startswith("PINV"):
                move.name = False
            if move_has_name or move.state != 'posted':
                if not move.posted_before and not move._sequence_matches_date():
                    if move._get_last_sequence(lock=False):
                        # The name does not match the date and the move is not the first in the period:
                        # Reset to draft
                        move.name = False
                        continue
                else:
                    if move_has_name and move.posted_before or not move_has_name and move._get_last_sequence(lock=False):
                        # The move either
                        # - has a name and was posted before, or
                        # - doesn't have a name, but is not the first in the period
                        # so we don't recompute the name
                        continue
            if move.date and (not move_has_name or not move._sequence_matches_date()) and not move.name.startswith("PINV"):
                move._set_next_sequence()

        self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = '/'
        self._inverse_name()

