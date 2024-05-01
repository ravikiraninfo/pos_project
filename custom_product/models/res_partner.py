from odoo import models, fields, api


class Partner(models.Model):
    _inherit = "res.partner"

    vendor_code = fields.Char(string="Customer ID")
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


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    partner_rf = fields.Char(string="Bill Reference", related="order_id.partner_ref")
