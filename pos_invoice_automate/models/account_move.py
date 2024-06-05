from odoo import models, fields, api, _
from num2words import num2words


class AccountMove(models.Model):
    _inherit = "account.move"

    row_check = fields.Integer(compute="compute_row_check")
    amount_in_words = fields.Char(compute="compute_amount_in_words")
    partial_sequence = fields.Char()
    include_igst = fields.Boolean()

    def set_include_igst(self):
        self.include_igst = True

    def compute_row_check(self):
        for rec in self:
            if rec.invoice_line_ids:
                rec.row_check = 9 - len(rec.invoice_line_ids)

    def compute_amount_in_words(self):
        for rec in self:
            rec.amount_in_words = num2words(rec.amount_total).upper()

    def _constrains_date_sequence(self):
        pass

    @api.depends('posted_before', 'state', 'journal_id', 'date', 'payment_state')
    def _compute_name(self):
        super()._compute_name()
        for move in self:
            name_splitted = move.name.split("/")
            if move.name and move.name.startswith("KSS") and name_splitted[1] == "24-24":
                current_year = fields.Date.today().year
                year_str = str(current_year)[-2:] + "-" + str(current_year + 1)[-2:]
                move.name = "KSS/" + year_str + "/" + name_splitted[2]
                
            if move.name and move.payment_state == "partial" and move.name.startswith("KSS"):
                move.name = "KSA" + move.name[3:]

            if move.name and move.payment_state != "partial" and move.name.startswith("KSA"):
                move.name = "KSS" + move.name[3:]
                

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_tax_amounts(self):
        self.ensure_one()
        cgst_2_5 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('cgst') and tax.amount == 2.5)
        sgst_2_5 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('sgst') and tax.amount == 2.5)
        cgst_6 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('cgst') and tax.amount == 6)
        sgst_6 = self.tax_ids.filtered(lambda tax: tax.name.lower().startswith('sgst') and tax.amount == 6)
        
        amount_cgst_2_5 = (self.price_subtotal * (cgst_2_5 and cgst_2_5.amount or 0)) / 100
        amount_sgst_2_5 = (self.price_subtotal * (sgst_2_5 and sgst_2_5.amount or 0)) / 100
        amount_cgst_6 = (self.price_subtotal * (cgst_6 and cgst_6.amount or 0)) / 100
        amount_sgst_6 = (self.price_subtotal * (sgst_6 and sgst_6.amount or 0)) / 100
        res = {
            "total_cgst_2_5": round(amount_cgst_2_5, 2),
            "total_sgst_2_5": round(amount_sgst_2_5, 2),
            "total_cgst_6": round(amount_cgst_6, 2),
            "total_sgst_6": round(amount_sgst_6, 2),
        }
        return res
