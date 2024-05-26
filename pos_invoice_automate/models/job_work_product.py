from odoo import fields, models


class JobWorkProduct(models.Model):
    _name = 'job.work.product'

    product_id = fields.Many2one("product.product")
    qty_for_job_work = fields.Float("")
    job_work_id = fields.Many2one("job.work")

    def set_jobwork_qty(self, vals):
        prod = self.env["product.product"].browse(int(vals.get("prod_id")))
        job_work_product = self.env["job.work.product"].search([("product_id", "=", prod.id), ("job_work_id", "=", False)])
        if job_work_product:
            job_work_product.qty_for_job_work = vals.get("qty")
        else:
            jw = self.env["job.work.product"].create({"product_id": prod.id, "qty_for_job_work": vals.get("qty")})
            return jw.id