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
