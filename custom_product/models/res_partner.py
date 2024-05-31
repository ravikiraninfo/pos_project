from odoo import models, fields, api, _


class Partner(models.Model):
    _inherit = "res.partner"

    vendor_code = fields.Char(string="Customer ID")
    supplier_code = fields.Char(string="Supplier Code")
    purchase_order_history = fields.Many2many('purchase.order.line', compute="compute_purchase_order_history")
    communication_history = fields.Text(string="Communication", tracking=True)
    vendor_rating = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], string="Rating")
    tin_no = fields.Char(string="Tin No")
    legder_name = fields.Char(string="Ledger Name")
    pan_card = fields.Char(string="Pan Card")
    gst_type = fields.Char(string="GST Type")
    gst_no = fields.Char(string="GST No")

    @api.model
    def create(self, vals):
        vals['vendor_code'] = self.env['ir.sequence'].next_by_code('res.partner')
        result = super(Partner, self).create(vals)
        return result

    def compute_purchase_order_history(self):
        for rec in self:
            order_line = self.env['purchase.order.line'].search([('partner_id', '=', rec.id)])
            rec.purchase_order_history = order_line.ids


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_template_id_1 = fields.Many2many('product.template', string="Product")
    attatchmet_ids = fields.Many2many('ir.attachment', string="Bill Document")

    def _add_supplier_to_product(self):
        for line in self.order_line:
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            already_seller = (partner | self.partner_id) & line.product_id.seller_ids.mapped('partner_id')
            if line.product_id and not already_seller and len(line.product_id.seller_ids) <= 10:
                # Convert the price in the right currency.
                currency = partner.property_purchase_currency_id or self.env.company.currency_id
                price = self.currency_id._convert(line.price_unit, currency, line.company_id,
                                                  line.date_order or fields.Date.today(), round=False)
                # Compute the price for the template's UoM, because the supplier's UoM is related to that UoM.
                if line.product_id.product_tmpl_id.uom_po_id != line.product_uom:
                    default_uom = line.product_id.product_tmpl_id.uom_po_id
                    price = line.product_uom._compute_price(price, default_uom)

                supplierinfo = self._prepare_supplier_info(partner, line, price, currency)
                # In case the order partner is a contact address, a new supplierinfo is created on
                # the parent company. In this case, we keep the product name and code.
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.order_id.date_order and line.order_id.date_order.date(),
                    uom_id=line.product_uom)

                supplierinfo['product_name'] = line.product_id.name
                supplierinfo['product_code'] = line.vendor_product_code
                vals = {
                    'seller_ids': [(0, 0, supplierinfo)],
                }
                # supplier info should be added regardless of the user access rights
                line.product_id.standard_price = price
                line.product_id.product_tmpl_id.sudo().write(vals)

    def print_product_label(self):
        product_ids = self.order_line
        plist = [(5, 0, 0)]
        for product in product_ids:
            for quantity in range(1, int(product.product_qty)+ 1):
                val = {
                    'selected': True,
                    'product_id': product.product_id.id,
                    'barcode': product.product_id.barcode,
                    'vendor_product_code': product.vendor_product_code
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


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    partner_rf = fields.Char(string="Bill Reference", related="order_id.partner_ref")
    vendor_product_code = fields.Char(string="Vendor Product Code")
    product_tmpl_id = fields.Many2one("product.template", related="product_id.product_tmpl_id")
    hsn_code = fields.Many2one('hsn.tax', string="HSN Code", related="product_tmpl_id.hsn_code", readonly=False)

    @api.onchange('hsn_code', 'price_unit')
    def _onhange_hsncode(self):
        if self.hsn_code:
            if self.hsn_code.name.startswith('6'):
                if self.product_id.product_tmpl_id.mrp_price < 1000:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount == 2.5).ids
                else:
                    self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: not x.name.lower().startswith('igst') and x.amount > 2.5).ids
            else:
                self.taxes_id = self.hsn_code.tax_ids.filtered(lambda x: x.name.lower() != "igst").ids
        
    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id._get_fiscal_position(line.order_id.partner_id)
            # filter taxes by company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == line.env.company)
            line.taxes_id = fpos.map_tax(taxes)
            line.taxes_id += line.hsn_code.tax_ids
