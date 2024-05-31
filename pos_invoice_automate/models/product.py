from odoo import fields, models

class Product(models.Model):
    _inherit = "product.product"

    qty_for_jobwork = fields.Float()

    def set_jobwork_qty(self, vals):
        prod = self.env["product.product"].browse(int(vals.get("prod_id")))
        prod.qty_for_jobwork = vals.get("qty")
