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

    extra_cost_ids = fields.One2many("extra.cost", inverse_name="product_tmpl_id")

    extra_details_description = fields.Text("Extra Details")
    list_price = fields.Float(compute="_compute_list_price", readonly=False, store=True)

    product_tag_ids = fields.Many2many(string='Work Tags')

    @api.onchange('hsn_code')
    def _onhange_hsncode(self):
        if self.hsn_code:
            if self.hsn_code.name.startswith('6'):
                if self.mrp_price < 1000:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids
                else:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5).ids
            else:
                self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: x.name.lower() != "igst").ids
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


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_code = fields.Char(string="Product Code", compute="compute_product_code")
    list_price = fields.Monetary(string="Sales Price", readonly=False)

    @api.onchange('hsn_code', 'standard_price')
    def _onhange_hsncode(self):
        if self.hsn_code:
            if self.hsn_code.name.startswith('6'):
                if self.mrp_price < 1000:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids
                else:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5).ids
            else:
                self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: x.name.lower() != "igst").ids
        # self.standard_price = self.mrp_price

    def compute_product_code(self):
        for rec in self:
            latest_seller = rec.seller_ids.sorted('date_start', reverse=True)
            if latest_seller:
                latest_seller = latest_seller[0]
            string_value = str(rec.standard_price).replace('.', '')
            mapping = self.env['purchase.price.code'].search_read(domain=[],
                                                                  fields=['name', 'code'])
            mapping_dict = {item['name']: item['code'] for item in mapping}
            result = ''.join(mapping_dict.get(digit, digit) for digit in string_value)
            rec.product_code = str(rec.pos_categ_id.sequence) + "-" + str(
                latest_seller.partner_id.supplier_code) + "-" + str(
                rec.create_date.date().strftime("%d%m%y")) + "-" + result + "-" 

    @api.onchange('price_selection')
    def _onchane_price_selection(self):
        for rec in self:
            if rec.price_selection == "mrp_price":
                rec.list_price = rec.mrp_price
            if rec.price_selection == "wh_price":
                rec.list_price = rec.whole_sale_price

    @api.model_create_multi
    def create(self, vals_list):
        liset_price = []
        for vals in vals_list:
            vals["categ_id"] = self.env.ref("custom_product.product_category_default").id
            liset_price = [(5, 0, 0)]
        res = super(ProductProduct, self).create(vals_list)
        # if not res.pos_categ_id:
        #     raise ValidationError(_("Please add category and code"))
        IrSequence = self.env['ir.sequence'].sudo()

        for product in res:
            str_val = ""
            if product.pos_categ_id:
                str_val = str(product.pos_categ_id.sequence) if product.pos_categ_id.sequence else "" + " "
            if product.product_template_attribute_value_ids:
                str_val = str_val + "("
                for att in product.product_template_attribute_value_ids:
                    str_val = str_val + att.product_attribute_value_id.attribute_id.name + "-" + att.product_attribute_value_id.name + ","
                str_val = str_val + ")"
            barcode_str = self.env['barcode.nomenclature'].sanitize_ean(
                "%s%s" % (product.id, datetime.now().strftime("%d%m%y%H%M")))
            # product.barcode = barcode_str
            product.barcode = IrSequence.next_by_code("product.barcode")

            product.default_code = str_val
            price_val = {
                'uom_id': res.env['pos.multi.price'].search([('name', '=', 'List Price')]).id
            }
            liset_price.append((0, 0, price_val))
            product.update({
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
