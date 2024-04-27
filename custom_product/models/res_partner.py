from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    vendor_code = fields.Char(string="Vendor Code")
    purchase_order_history = fields.Many2many('purchase.order.line',compute="compute_purchase_order_history")

    def compute_purchase_order_history(self):
        for rec in self:
            order_line = self.env['purchase.order.line'].search([('partner_id', '=', rec.id)])
            rec.purchase_order_history = order_line.ids


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_template_id_1 = fields.Many2many('product.template', string="Product")
