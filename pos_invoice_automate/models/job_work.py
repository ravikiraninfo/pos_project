from odoo import api, models, fields, _


class JobWork(models.Model):
    _name = "job.work"

    partner_id = fields.Many2one('res.partner', string="Customer")
    bill_number = fields.Many2one('account.move', string="Bill Number", related="order_id.account_move")
    payment_status = fields.Selection(selection=[("partial", "Partially Paid"), ("paid", "Paid")], string="Payment Status")
    garmets_id = fields.Many2one('product.product', string="Garment Details")
    services = fields.Selection(
        [('saree_fall', 'Saree Fall'), ('pico', 'Pico'), ('polishing', 'Polishing'), ('alteration', 'Alteration')],
        string="Services", default="saree_fall")
    description = fields.Text(string="Description")
    vendor_id = fields.Many2one('res.partner', string="Vendor/Team Selection")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'High'),
    ], default='0', index=True, string="Priority", tracking=True)    
    delivery_dates = fields.Date(string="Delivery Date")
    estimated_delivery_dates = fields.Date(string="Estimated Delivery Date")
    order_id = fields.Many2one('pos.order')
    stage = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done')],
        string="Stage", default="new")
    product_ids = fields.Many2many("product.product")
