from odoo import api, models, fields, _


class JobWork(models.Model):
    _name = "job.work"

    partner_id = fields.Many2one('res.partner', string="Customer")
    jobwork_title = fields.Char()
    bill_number = fields.Many2one('account.move', string="Bill Number")
    payment_status = fields.Selection(selection=[("partial", "Partially Paid"), ("paid", "Paid")], string="Payment Status")
    garmets_id = fields.Many2one('product.product', string="Garment Details")
    services = fields.Selection(
        [('saree_fall', 'Saree Fall'), ('pico', 'Pico'), ('polishing', 'Polishing'), ('alteration', 'Alteration')],
        string="Services", default="saree_fall")
    description = fields.Text(string="Description")
    vendor_id = fields.Many2one('res.partner', string="Vendor/Team Selection", domain="[('is_jobwork_team', '=', True)]")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'High'),
    ], default='0', index=True, string="Priority", tracking=True)    
    delivery_dates = fields.Date(string="Delivery Date")
    estimated_delivery_dates = fields.Date(string="Estimated Delivery Date")
    order_id = fields.Many2one('pos.order')
    stage = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('received', 'Received'), ('packed', 'Packed'), ('delivered', 'Delivered')],
        string="Stage", default="new")
    product_ids = fields.Many2many("product.product")
    product_tmpl_ids = fields.Many2many("product.template", compute="_compute_product_tmpl_ids")

    job_work_product_ids = fields.One2many("job.work.product", "job_work_id")

    def _compute_product_tmpl_ids(self):
        for job in self:
            job.product_tmpl_ids = False
            for product_id in job.product_ids:
                job.product_tmpl_ids += product_id.product_tmpl_id

    def create_jobwork(self, vals):
        jobwork_product_ids = vals.get("job_work_product_ids")
        service = vals.get("services") and vals.get("services").lower().replace(" ", "_") or False
        invoice = self.env["account.move"].search([("name", "=", vals.get("bill_number")), ("move_type", "=", "out_invoice")])
        new_vals = {
        'partner_id' : int(vals.get("partner_id")),
        'description' : vals.get("description"),
        'services' :  service,
        'priority' :  '1' if vals.get("priority") else '0',
        'estimated_delivery_dates' :  vals.get("estimated_delivery_dates"),
        'delivery_dates' :  vals.get("delivery_dates"),
        'payment_status' :  vals.get("payment_status"),
        "jobwork_title": vals.get("bill_number"),
        "bill_number": invoice and invoice.id ,
        "job_work_product_ids": [(6, 0, jobwork_product_ids)]
        }

        jd = self.env["job.work"].create(new_vals)
        for pro_id in vals.get("product_ids"):
            pro = self.env["product.product"].browse(int(pro_id))
            jd.product_ids = [(4, int(pro.id))]

    def mark_as_sent(self):
        self.stage = 'in_progress'

    def mark_as_complete(self):
        self.stage = 'received'

    def mark_as_packed(self):
        self.stage = 'packed'

    def mark_as_delivered(self):
        self.stage = 'delivered'

    def reset_to_new(self):
        self.stage = 'new'

