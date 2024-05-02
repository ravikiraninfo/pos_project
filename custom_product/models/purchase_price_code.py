from odoo import models, fields, api


class PurchasePriceCode(models.Model):
    _name = "purchase.price.code"

    name = fields.Char(string="Number")
    code = fields.Char(string="Code")
