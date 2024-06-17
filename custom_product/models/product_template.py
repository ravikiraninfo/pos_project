from odoo import fields, models, api, _
import random
from datetime import datetime
from odoo.tools import format_amount


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
    # list_price = fields.Float(compute="_compute_list_price", readonly=False, store=True)

    product_tag_ids = fields.Many2many(string='Work Tags')
    taxes_id = fields.Many2many(compute="_compute_taxes_id")

    sales_price_with_tax_editable = fields.Integer("Sales Price(Incl. Tax)")

    @api.onchange("sales_price_with_tax_editable")
    def _onchange_sales_price_with_tax_editable(self):
        if self.sales_price_with_tax_editable > 0:
            total_tax_amount = self.taxes_id.mapped("amount")
            sales_price_without_tax = ((self.sales_price_with_tax_editable * 100) / (100 + sum(total_tax_amount)))
            self.list_price = sales_price_without_tax

    def _construct_tax_string(self, price):
        currency = self.currency_id
        res = self.taxes_id.compute_all(price, product=self, partner=self.env['res.partner'])
        joined = []
        included = res['total_included']
        included = round(int(float(included)))
        if currency.compare_amounts(included, price):
            joined.append(_('%s Incl. Taxes', format_amount(self.env, included, currency)))
        excluded = res['total_excluded']
        if currency.compare_amounts(excluded, price):
            joined.append(_('%s Excl. Taxes', format_amount(self.env, excluded, currency)))
        if joined:
            tax_string = f"(= {', '.join(joined)})"
        else:
            tax_string = " "
        return tax_string


    @api.depends("hsn_code", "standard_price")
    def _compute_taxes_id(self):
        for tmpl in self:
            tmpl.taxes_id = tmpl.taxes_id
            if not tmpl.hsn_code:
                continue 
            if tmpl.hsn_code.name.startswith('6'):
                if tmpl.standard_price < 1000:
                    tmpl.taxes_id = tmpl.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5)
                else:
                    tmpl.taxes_id = tmpl.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5)
            else:
                tmpl.taxes_id = tmpl.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst'))



    @api.onchange('hsn_code', "standard_price")
    def _onhange_hsncode(self):
        if self.hsn_code:
            if self.hsn_code.name.startswith('6'):
                if self.standard_price < 1000:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids
                else:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5).ids
            else:
                self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst')).ids
        # self.standard_price = self.mrp_price

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
        attribute_ids = self.env["product.attribute"].search([])
        for aid in attribute_ids:
            val = {
                'attribute_id': aid.id
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
    
    @api.depends_context('company')
    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_standard_price(self):
        # Depends on force_company context because standard_price is company_dependent
        # on the product_product
        # unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in self:
            template.standard_price = sum(template.product_variant_ids.mapped("standard_price")) / len(template.product_variant_ids)
        


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_code = fields.Char(string="Product Code", compute="compute_product_code")
    sales_price_with_tax_editable = fields.Integer("Sales Price(Incl. Tax)")
    # taxes_id = fields.Many2many("account.tax", compute="_compute_taxes_id", store=True)

    # @api.depends("hsn_code", "standard_price")
    # def _compute_taxes_id(self):
    #     for var in self:
    #         var.taxes_id = var.taxes_id
    #         if not var.hsn_code:
    #             continue 
    #         if var.hsn_code.name.startswith('6'):
    #             if var.standard_price < 1000:
    #                 var.taxes_id = var.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids
    #             else:
    #                 var.taxes_id = var.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5).ids
    #         else:
    #             var.taxes_id = var.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst')).ids
    #         print('\n\n\nvar.taxes_id', var.taxes_id)
    

    # @api.onchange("sales_price_with_tax_editable")
    # def _onchange_sales_price_with_tax_editable(self):
    #     if self.sales_price_with_tax_editable > 0:
    #         total_tax_amount = self.taxes_id.mapped("amount")
    #         sales_price_without_tax = ((self.sales_price_with_tax_editable * 100) / (100 + sum(total_tax_amount)))
    #         self.price_extra += (sales_price_without_tax + (self.pos_multi_uom_ids and (self.pos_multi_uom_ids[0].price - self.standard_price) or 0))
            # self.lst_price = sales_price_without_tax   
    
    # @api.depends("product_template_attribute_value_ids.price_extra")
    # def _compute_product_price_extra(self):
    #     for product in self:
    #         if product.sales_price_with_tax_editable > 0:
    #             total_tax_amount = product.taxes_id.mapped("amount")
    #             sales_price_without_tax = ((product.sales_price_with_tax_editable * 100) / (100 + sum(total_tax_amount)))
    #             tax = product.sales_price_with_tax_editable - sales_price_without_tax
    #             print('\n\n\ntax', tax)
    #             print('\n\n\nproduct.list_price', product.list_price)
    #             product.price_extra = (product.sales_price_with_tax_editable - tax - product.list_price) + sum(product.product_template_attribute_value_ids.mapped('price_extra'))
    #         else:
    #             product.price_extra = sum(product.product_template_attribute_value_ids.mapped('price_extra'))

    #         print('\n\n\nproduct.price_extra111', product.price_extra)

    def _update_sales_price(self):
        for record in self:
            record.sales_price_with_tax_editable = 0
            
    def print_product_label(self):
        plist = [(5, 0, 0)]
        val = {
            'selected': True,
            'product_id': self.id,
            'barcode': self.barcode,
            'vendor_product_code': self.product_code,
            'price_unit': round(self.lst_price, 2)
        }
        plist.append((0, 0, val))
    
        return {
            'name': _('Print Label'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'print.product.label',
            'view_id': self.env.ref(
                'garazd_product_label.print_product_label_view_form').id,
            'context': {
                'default_label_ids': plist,
            },
            'target': 'current'
        }

    # @api.onchange('hsn_code', 'standard_price')
    # def _onhange_hsncode(self):
    #     if self.hsn_code:
    #         if self.hsn_code.name.startswith('6'):
    #             if self.standard_price < 1000:
    #                 self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids
    #             else:
    #                 self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5).ids
    #         else:
    #             self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids

    def compute_product_code(self):
        for rec in self:
            latest_seller = rec.seller_ids
            if latest_seller:
                latest_seller = latest_seller[0]
            value_after_dec = str(rec.standard_price).split(".")[1]
            string_value = str(rec.standard_price).replace('.', '')

            if int(value_after_dec) == 0:
                string_value = str(int(rec.standard_price))
            mapping = self.env['purchase.price.code'].search_read(domain=[],
                                                                  fields=['name', 'code'])
            mapping_dict = {item['name']: item['code'] for item in mapping}
            result = ''.join(mapping_dict.get(digit, digit) for digit in string_value)
            rec.product_code = str(rec.pos_categ_id.sequence) + "-" + str(
                latest_seller.partner_id.supplier_code) + "-" + str(
                rec.create_date.date().strftime("%d%m%y")) + "-" + result + "-" + str(
                latest_seller.product_code)

    # @api.onchange('price_selection')
    # def _onchane_price_selection(self):
    #     for rec in self:
    #         if rec.price_selection == "mrp_price":
    #             rec.list_price = rec.mrp_price
    #         if rec.price_selection == "wh_price":
    #             rec.list_price = rec.whole_sale_price

    @api.onchange("standard_price")
    def _onchange_standard_price_new(self):
        self.product_tmpl_id.standard_price = self.standard_price

        
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
    
    @api.depends('list_price', 'price_extra', 'standard_price')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        # to_uom = None
        # if 'uom' in self._context:
        #     to_uom = self.env['uom.uom'].browse(self._context['uom'])

        for product in self:
            # if to_uom:
            #     list_price = product.uom_id._compute_price(product.list_price, to_uom)
            # else:
            #     list_price = product.list_price
            if product.sales_price_with_tax_editable > 0:
                total_tax_amount = product.taxes_id.mapped("amount")
                sales_price_without_tax = ((product.sales_price_with_tax_editable * 100) / (100 + sum(total_tax_amount)))
                product.lst_price = sales_price_without_tax
                continue


            list_price = product.pos_multi_uom_ids and product.pos_multi_uom_ids[0].price or 0
            product.lst_price = list_price + product.price_extra
    