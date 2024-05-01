from odoo import models, fields, api


class HsnTax(models.Model):
    _name = "hsn.tax"

    name = fields.Char(string="HSN Code")
    tax_ids = fields.Many2many('account.tax', string="Tax")
