from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    extra_cost_ids = fields.One2many("extra.cost", inverse_name="purchase_order_id")

    total_extra_cost = fields.Float(compute="_compute_total_extra_cost")

    @api.depends("extra_cost_ids", "extra_cost_ids.amount", "order_line")
    def _compute_total_extra_cost(self):
        for order in self:
            order.total_extra_cost = sum(order.extra_cost_ids.mapped("amount"))


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sales_price_with_tax_editable = fields.Integer("Edit Sales Price(Incl. Tax)")
    sales_price_with_tax = fields.Integer("Sales Price(Incl. Tax)", compute="_compute_sales_price_with_tax")
    partner_rf = fields.Char(string="Bill Reference", related="order_id.partner_ref")
    vendor_product_code = fields.Char(string="Vendor Product Code")
    product_tmpl_id = fields.Many2one("product.template", related="product_id.product_tmpl_id")
    hsn_code = fields.Many2one('hsn.tax', string="HSN Code", related="product_tmpl_id.hsn_code", readonly=False)

    @api.onchange('hsn_code', 'price_unit')
    def _onhange_hsncode(self):
        if self.hsn_code:
            if self.hsn_code.name.startswith('6'):
                if self.price_unit < 1000:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids
                    self.product_id.taxes_id = self.taxes_id
                else:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5).ids
                    self.product_id.taxes_id = self.taxes_id
            else:
                self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: x.name.lower() != "igst").ids
            self.product_id.product_tmpl_id.taxes_id = self.hsn_code.tax_ids
        
    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id._get_fiscal_position(line.order_id.partner_id)
            # filter taxes by company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == line.env.company)
            line.taxes_id = fpos.map_tax(taxes)
            line.taxes_id += line.hsn_code.tax_ids
            # line.product_id.product_tmpl_id.taxes_id = line.hsn_code.tax_ids

    def _compute_sales_price_with_tax(self):
        for line in self:
            prod = line.product_id
            total_price1 = prod.standard_price + sum(prod.extra_cost_ids.mapped('amount'))
            price = ((total_price1 * (prod.pos_multi_uom_ids and prod.pos_multi_uom_ids[0].profit.value or 0)) / 100) + total_price1
            taxes_amount = sum(line.product_id.taxes_id.mapped("amount"))
            line.sales_price_with_tax = price + ((taxes_amount * price) / 100)
        # for line in self:
        #     taxes_amount = sum(line.product_id.taxes_id.mapped("amount"))
        #     line.sales_price_with_tax = line.product_id.list_price + ((taxes_amount * line.product_id.list_price) / 100)
            
    @api.onchange("sales_price_with_tax_editable")
    def _onchange_sales_price_with_tax_editable(self):
        if self.sales_price_with_tax_editable > 0:
            total_tax_amount = self.taxes_id.mapped("amount")
            sales_price_without_tax = ((self.sales_price_with_tax_editable * 100) / (100 + sum(total_tax_amount)))
            # self.product_id.list_price = sales_price_without_tax
            # self.product_id.lst_price = sales_price_without_tax
            self.product_id.sales_price_with_tax_editable = self.sales_price_with_tax_editable
    
    def _get_gross_price_unit(self):
        self.ensure_one()
        price_unit = self.price_unit
        return price_unit


    # @api.depends("order_id.total_extra_cost")
    # def _compute_price_unit_and_date_planned_and_name(self):
    #     res = super()._compute_price_unit_and_date_planned_and_name()
    #     total_qty = sum(self.mapped("product_qty"))
    #     if not total_qty:
    #         return res
    #     avg_ext_cost = self[0].order_id.total_extra_cost / total_qty
    #     if not avg_ext_cost:
    #         return res
    #     # print('\n\n\n\n2-2-2-2', self.filtered(lambda line: line.order_id.extra_cost_ids))
    #     for line in self.filtered(lambda line: line.order_id.extra_cost_ids):
    #         line.price_unit += avg_ext_cost
