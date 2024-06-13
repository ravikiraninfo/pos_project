# Copyright © 2018 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models


class PrintProductLabelLine(models.TransientModel):
    _name = "print.product.label.line"
    _description = 'Line with a Product Label Data'
    _order = 'sequence'

    sequence = fields.Integer(default=900)
    selected = fields.Boolean(string='Print', default=True)
    vendor_product_code = fields.Char()
    wizard_id = fields.Many2one(comodel_name='print.product.label')  # Not make required
    product_id = fields.Many2one(comodel_name='product.product', required=True)
    barcode = fields.Char(compute='_compute_barcode')
    qty_initial = fields.Integer(string='Initial Qty', default=1)
    qty = fields.Integer(string='Label Qty', default=1)
    company_id = fields.Many2one(
        comodel_name='res.company',
        compute='_compute_company_id',
    )
    price_unit = fields.Float()

    def _compute_tax_included(self, price):
        res = self.product_id.product_tmpl_id.taxes_id.compute_all(price, product=self.product_id.product_tmpl_id, partner=self.env['res.partner'])
        included = res['total_included']
        return included

    @api.depends('wizard_id.company_id')
    def _compute_company_id(self):
        for label in self:
            label.company_id = \
                label.wizard_id.company_id and label.wizard_id.company_id.id \
                or self.env.user.company_id.id

    @api.depends('product_id')
    def _compute_barcode(self):
        for label in self:
            label.barcode = label.product_id.barcode

    def action_plus_qty(self):
        self.ensure_one()
        if not self.qty:
            self.update({'selected': True})
        self.update({'qty': self.qty + 1})

    def action_minus_qty(self):
        self.ensure_one()
        if self.qty > 0:
            self.update({'qty': self.qty - 1})
            if not self.qty:
                self.update({'selected': False})
