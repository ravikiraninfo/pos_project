from odoo import api, models, fields, _


class JobWork(models.Model):
    _name = "job.work"

    partner_id = fields.Many2one('res.partner', string="Customer")
    bill_number = fields.Many2one('account.move', string="Bill Number")
    payment_status = fields.Selection(related="bill_number.payment_state", string="Payment Status")
    garmets_id = fields.Many2one('product.product', string="Garment Details")
    services = fields.Selection(
        [('saree_fall', 'Saree Fall'), ('pico', 'Pico'), ('polishing', 'Polishing'), ('alteration', 'Alteration')],
        string="Services")
    description = fields.Text(string="Description")
    vendor_id = fields.Many2one('res.partner', string="Vendor/Team Selection")
    urgent = fields.Boolean(string="Urgent")
    delivery_dates = fields.Date(string="Delivery Date")
    estimated_delivery_dates = fields.Date(string="Estimated Delivery Date")
    order_id = fields.Many2one('pos.order')
