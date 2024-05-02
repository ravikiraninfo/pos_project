from odoo import fields, models, api, _
import random
from datetime import datetime
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mrp_price = fields.Float(string="Product Price")
    whole_sale_price = fields.Float(string="Wholesale Price")
    price_selection = fields.Selection(
        [('sale_price', 'Sale Price'), ('mrp_price', 'MRP Price'), ('wh_price', 'WholesalePrice')])
    product_code = fields.Char(string="Product Code")
    hsn_code = fields.Many2one('hsn.tax', string="HSN Code")

    @api.onchange('hsn_code', 'mrp_price')
    def _onhange_hsncode(self):
        if self.hsn_code:
            if self.hsn_code.name.startswith('6'):
                if self.mrp_price < 1000:
                    self.taxes_id = [19, 15]
                else:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: x.id not in [16, 21, 23, 24]).ids
            else:
                self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: x.id not in [16, 21, 23, 24]).ids
        self.standard_price = self.mrp_price

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
        liset_price = [(5, 0, 0)]
        attribute_id = [1, 2, 3, 4, 5]
        for aid in attribute_id:
            val = {
                'attribute_id': aid
            }
            list_a.append((0, 0, val))
        price_val = {
            'uom_id': self.env['pos.multi.price'].search([('name', '=', 'List Price')]).id
        }
        liset_price.append((0, 0, price_val))
        self.update({
            'attribute_line_ids': list_a,
            'pos_multi_uom_ids': liset_price,
            'detailed_type': 'product'
        })

    @api.onchange('pos_multi_uom_ids')
    def _onchange_pos_multi_uom_ids(self):
        price_id = self.env['pos.multi.price'].search([('name', '=', 'List Price')]).id
        price = sum(self.pos_multi_uom_ids.filtered(lambda x: x.uom_id.id == price_id).mapped('price'))
        self.write({
            'list_price': price
        })



class ProductProduct(models.Model):
    _inherit = "product.product"

    product_code = fields.Char(string="Product Code", compute="compute_product_code")

    def compute_product_code(self):
        for rec in self:
            latest_seller = rec.seller_ids.sorted('date_start', reverse=True)[0]
            string_value = str(rec.standard_price).replace('.', '')
            mapping = self.env['purchase.price.code'].search_read(domain=[],
                                                                  fields=['name', 'code'])
            mapping_dict = {item['name']: item['code'] for item in mapping}
            result = ''.join(mapping_dict.get(digit, digit) for digit in string_value)
            rec.product_code = str(rec.pos_categ_id.sequence) + "-" + str(
                latest_seller.partner_id.supplier_code) + "-" + str(
                rec.create_date.date().strftime("%d%m%y")) + "-" + result + "-" + str(
                latest_seller.product_code)

    @api.onchange('price_selection')
    def _onchane_price_selection(self):
        for rec in self:
            if rec.price_selection == "mrp_price":
                rec.list_price = rec.mrp_price
            if rec.price_selection == "wh_price":
                rec.list_price = rec.whole_sale_price

    @api.model
    def create(self, vals):
        liset_price = [(5, 0, 0)]
        res = super(ProductProduct, self).create(vals)
        if not res.pos_categ_id:
            raise ValidationError(_("Please add category and code"))
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
        price_val = {
            'uom_id': self.env['pos.multi.price'].search([('name', '=', 'List Price')]).id
        }
        liset_price.append((0, 0, price_val))
        res.update({
            'pos_multi_uom_ids': liset_price,
        })
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
