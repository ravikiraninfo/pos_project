from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    extra_cost_ids = fields.One2many("extra.cost", inverse_name="purchase_order_id")

