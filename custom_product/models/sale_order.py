from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    salesperson_ids = fields.Many2one('res.users', string="Sales Person")
    price_id = fields.Many2one('pos.multi.price', string='Choose a Price')

    # @api.onchange('salesperson_ids')
    # def _onchange_salesperson_ids(self):
    #     for rec in self.order_line:
    #         rec.salesperson_ids = self.salesperson_ids.ids
    #
    # @api.onchange('price_id')
    # def _onchange_price_id(self):
    #     for rec in self.order_line:
    #         rec.price_id = self.price_id.id


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    salesperson_ids = fields.Many2one('res.users', string="Sales Person")
    price_id = fields.Many2one('pos.multi.price', string='Choose a Price')
