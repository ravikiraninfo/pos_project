from odoo import fields, models, api
import random
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mrp_price = fields.Float(string="MRP Price")
    whole_sale_price = fields.Float(string="Wholesale Price")
    price_selection = fields.Selection(
        [('sale_price', 'Sale Price'), ('mrp_price', 'MRP Price'), ('wh_price', 'WholesalePrice')])
    product_code = fields.Char(string="Product Code")

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
        str_val = ""
        if res.pos_categ_id:
            str_val = str(res.pos_categ_id.sequence) + " "
        if res.product_template_attribute_value_ids:
            str_val = str_val + "("
            for att in res.product_template_attribute_value_ids:
                str_val = str_val + att.product_attribute_value_id.attribute_id.name + "-" + att.product_attribute_value_id.name + ","
            str_val = str_val + ")"
        barcode_str = self.env['barcode.nomenclature'].sanitize_ean(
            "%s%s" % (res.id, datetime.now().strftime("%d%m%y%H%M")))
        res.barcode = barcode_str
        res.default_code = str_val
        res.product_code = str(res.pos_categ_id.sequence) + "-" + res.seller_ids[
            0].partner_id.vendor_code if res.seller_ids else " " + "-" + str(res.create_date.date()) + "-" + str(
            res.standard_price) + "-" + barcode_str

        return res
