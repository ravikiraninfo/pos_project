from odoo import fields, models, api, _
import random
from datetime import datetime
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mrp_price = fields.Float(string="MRP Price")
    whole_sale_price = fields.Float(string="Wholesale Price")
    price_selection = fields.Selection(
        [('sale_price', 'Sale Price'), ('mrp_price', 'MRP Price'), ('wh_price', 'WholesalePrice')])
    product_code = fields.Char(string="Product Code")
    hsn_code = fields.Many2one('hsn.tax', string="HSN Code")

    @api.onchange('hsn_code')
    def _onhange_hsncode(self):
        if self.hsn_code:
            self.taxes_id = self.hsn_code.tax_ids.ids

    @api.onchange('price_selection')
    def _onchane_price_selection(self):
        for rec in self:
            if rec.price_selection == "mrp_price":
                rec.list_price = rec.mrp_price
            if rec.price_selection == "wh_price":
                rec.list_price = rec.whole_sale_price

    @api.onchange('name')
    def onchange_name(self):
        list_a = [(5, 0, 0)]
        attribute_id = [1, 2, 3, 4, 5]
        for aid in attribute_id:
            val = {
                'attribute_id': aid
            }
            list_a.append((0, 0, val))
        self.update({
            'attribute_line_ids': list_a
        })


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
            str_val = str(res.pos_categ_id.sequence) if res.pos_categ_id.sequence else False + " "
        if res.product_template_attribute_value_ids:
            str_val = str_val + "("
            for att in res.product_template_attribute_value_ids:
                str_val = str_val + att.product_attribute_value_id.attribute_id.name + "-" + att.product_attribute_value_id.name + ","
            str_val = str_val + ")"
        barcode_str = self.env['barcode.nomenclature'].sanitize_ean(
            "%s%s" % (res.id, datetime.now().strftime("%d%m%y%H%M")))
        res.barcode = barcode_str
        res.default_code = str_val
        if not res.seller_ids:
            raise ValidationError(_("Please add vendor"))
        res.product_code = str(res.pos_categ_id.sequence) if res.pos_categ_id.sequence else " " + "-" + str(res.seller_ids[0].partner_id.supplier_code) if res.seller_ids[
            0].partner_id.supplier_code else " " + "-" + str(
            res.create_date.date()) + "-" + str(str(res.standard_price).encode())

        return res
    #
    # def write(self, vals):
    #     res = super(ProductProduct, self).write(vals)
    #     str_val = ""
    #     if self.pos_categ_id:
    #         str_val = str(self.pos_categ_id.sequence) if self.pos_categ_id.sequence else False + " "
    #     if self.product_template_attribute_value_ids:
    #         str_val = str_val + "("
    #         for att in self.product_template_attribute_value_ids:
    #             str_val = str_val + att.product_attribute_value_id.attribute_id.name + "-" + att.product_attribute_value_id.name + ","
    #         str_val = str_val + ")"
    #     barcode_str = self.env['barcode.nomenclature'].sanitize_ean(
    #         "%s%s" % (self.id, datetime.now().strftime("%d%m%y%H%M")))
    #     barcode = barcode_str
    #     default_code = str_val
    #     if not self.seller_ids:
    #         raise ValidationError(_("Please add vendor"))
    #     product_code = str(self.pos_categ_id.sequence) if self.pos_categ_id.sequence else " " + "-"
    #     + self.seller_ids[0].partner_id.vendor_code if self.seller_ids[0].partner_id.vendor_code else " " + "-" + str(
    #         self.create_date.date()) + "-" + str(str(self.standard_price).encode())
    #     self.update({
    #         'barcode': barcode,
    #         'default_code': default_code,
    #         'product_code': product_code
    #     })
    #     return res
