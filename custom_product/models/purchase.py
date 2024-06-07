from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    extra_cost_ids = fields.One2many("extra.cost", inverse_name="purchase_order_id")

    total_extra_cost = fields.Float(compute="_compute_total_extra_cost")

    @api.depends("extra_cost_ids", "extra_cost_ids.amount", "order_line")
    def _compute_total_extra_cost(self):
        for order in self:
            order.total_extra_cost = sum(order.extra_cost_ids.mapped("amount"))


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"


    # @api.depends("order_id.total_extra_cost")
    # def _compute_price_unit_and_date_planned_and_name(self):
    #     res = super()._compute_price_unit_and_date_planned_and_name()
    #     total_qty = sum(self.mapped("product_qty"))
    #     if not total_qty:
    #         return res
    #     avg_ext_cost = self[0].order_id.total_extra_cost / total_qty
    #     if not avg_ext_cost:
    #         return res
    #     # print('\n\n\n\n2-2-2-2', self.filtered(lambda line: line.order_id.extra_cost_ids))
    #     for line in self.filtered(lambda line: line.order_id.extra_cost_ids):
    #         line.price_unit += avg_ext_cost
