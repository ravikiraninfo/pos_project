from odoo import models, fields, api, _
from num2words import num2words


class AccountMove(models.Model):
    _inherit = "account.move"

    row_check = fields.Integer(compute="compute_row_check")
    amount_in_words = fields.Char(compute="compute_amount_in_words")
    partial_sequence = fields.Char()

    def compute_row_check(self):
        for rec in self:
            if rec.invoice_line_ids:
                rec.row_check = 9 - len(rec.invoice_line_ids)

    def compute_amount_in_words(self):
        for rec in self:
            rec.amount_in_words = num2words(rec.amount_total)

    @api.depends('posted_before', 'state', 'journal_id', 'date', 'payment_state')
    def _compute_name(self):
        """ OVERRIDE """
        self = self.sorted(lambda m: (m.date, m.ref or '', m.id))

        for move in self:
            if move.state == 'cancel':
                continue

            move_has_name = move.name and move.name != '/'

            if move_has_name or move.state != 'posted':
                if move.payment_state == "partial" and move.name.startswith("INV") and not move.ref:
                    move.name = "P/" + move.name
                    continue
                if move.payment_state != "partial" and move.name and move.name.startswith("P/"):
                    move.name = move.name[2:]
                    continue
                if not move.posted_before and not move._sequence_matches_date():
                    if move._get_last_sequence(lock=False):
                        # The name does not match the date and the move is not the first in the period:
                        # Reset to draft
                        move.name = False
                        continue
                else:
                    if (move_has_name and move.posted_before or not move_has_name and move._get_last_sequence(lock=False)) and move.payment_state != "partial":
                        # The move either
                        # - has a name and was posted before, or
                        # - doesn't have a name, but is not the first in the period
                        # so we don't recompute the name
                        continue
                    elif move_has_name and move.name.startswith("INV/"):
                        move.name = "P/" + move.name
                        continue
            if move.payment_state != "partial" and move.name.startswith("P/"):
                move.name = move.name[2:]
                continue
            move_has_name = move.name and move.name != '/'
            if move.date and (not move_has_name or not move._sequence_matches_date()) and not move.name.startswith("P/"):
                move._set_next_sequence()
            if not move_has_name and move.name.startswith("P/"):
                move.name = move.name[2:]


        self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = '/'
        self._inverse_name()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_tax_amounts(self):
        self.ensure_one()
        cgst_2_5 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('cgst') and tax.amount == 2.5)
        sgst_2_5 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('sgst') and tax.amount == 2.5)
        cgst_6 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('cgst') and tax.amount == 6)
        sgst_6 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('sgst') and tax.amount == 6)
        
        print('\n\n\nself.price_subtotal * ', self.price_subtotal)
        print('\n\n\nscgst_2_5 ', cgst_2_5)
        amount_cgst_2_5 = (self.price_subtotal * (cgst_2_5 and cgst_2_5.amount or 0)) / 100
        amount_sgst_2_5 = (self.price_subtotal * (sgst_2_5 and sgst_2_5.amount or 0)) / 100
        amount_cgst_6 = (self.price_subtotal * (cgst_6 and cgst_6.amount or 0)) / 100
        amount_sgst_6 = (self.price_subtotal * (sgst_6 and sgst_6.amount or 0)) / 100
        res = {
            "total_cgst_2_5": amount_cgst_2_5,
            "total_sgst_2_5": amount_sgst_2_5,
            "total_cgst_6": amount_cgst_6,
            "total_sgst_6": amount_sgst_6,
        }
        return res
