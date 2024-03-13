from odoo import fields, models, api
import random
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mrp_price = fields.Float(string="MRP Price")
    whole_sale_price = fields.Float(string="Wholesale Price")
    price_selection = fields.Selection(
        [('sale_price', 'Sale Price'), ('mrp_price', 'MRP Price'), ('wh_price', 'WholesalePrice')])

    @api.onchange('price_selection')
    def _onchane_price_selection(self):
        for rec in self:
            if rec.price_selection == "mrp_price":
                rec.list_price = rec.mrp_price
            if rec.price_selection == "wh_price":
                rec.list_price = rec.whole_sale_price


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange('price_selection')
    def _onchane_price_selection(self):
        for rec in self:
            if rec.price_selection == "mrp_price":
                rec.list_price = rec.mrp_price
            if rec.price_selection == "wh_price":
                rec.list_price = rec.whole_sale_price

    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)

        barcode_str = self.env['barcode.nomenclature'].sanitize_ean(
            "%s%s" % (res.id, datetime.now().strftime("%d%m%y%H%M")))
        res.barcode = barcode_str

        return res
