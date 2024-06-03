from odoo import fields, models


class JobWorkProduct(models.Model):
    _name = 'job.work.product'

    product_id = fields.Many2one("product.product")
    qty_for_job_work = fields.Float("")
    job_work_service_details = fields.Text("")
    job_work_service = fields.Selection(
        [('saree_fall', 'Saree Fall'), ('pico', 'Pico'), ('polishing', 'Polishing'), ('alteration', 'Alteration')],
        string="Job Work Services")
    job_work_id = fields.Many2one("job.work", ondelete="cascade")

    def set_jobwork_qty(self, vals):
        job_work_product = self.env["job.work.product"].search([("product_id", "=", int(vals.get("prod_id"))), ("job_work_id", "=", False)])
        if job_work_product:
            job_work_product.qty_for_job_work = vals.get("qty")
        else:
            jw = self.env["job.work.product"].create({"product_id": int(vals.get("prod_id")), "qty_for_job_work": vals.get("qty")})
            return jw.id
        
    def set_jobwork_services(self, vals):
        job_work_product = self.env["job.work.product"].search([("product_id", "=", int(vals.get("prod_id"))), ("job_work_id", "=", False)])
        if job_work_product:
            job_work_product.job_work_service = vals.get("service").lower().replace(" ", "_")
    
    def set_jobwork_service_details(self, vals):
        job_work_product = self.env["job.work.product"].search([("product_id", "=", int(vals.get("prod_id"))), ("job_work_id", "=", False)])
        if job_work_product:
            job_work_product.job_work_service_details = vals.get("service_details")

    def create_job_work_product(self, vals):
        jw = self.env["job.work.product"].create({"product_id": int(vals.get("prod_id")), "qty_for_job_work": vals.get("qty")})
        return jw.id