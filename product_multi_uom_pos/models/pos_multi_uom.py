# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Arwa V V (Contact : odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import fields, models, api


class PosMultiUom(models.Model):
    """
    Model for managing Point of Sale (POS) Multi Unit of Measure (UoM).

    This model represents the association between a product template and its
    multiple unit of measure options for the Point of Sale module.
    """
    _name = 'pos.multi.uom'
    _description = 'POS Multi UoM'

    product_template_id = fields.Many2one('product.template',
                                          string='Product Template',
                                          help='Inverse field of one2many'
                                               'field POS Multiple UoM in'
                                               'product.template')
    category_id = fields.Many2one(
        related='product_template_id.uom_id.category_id',
        string='UoM Category', help='Category of unit of measure')
    uom_id = fields.Many2one('pos.multi.price', string='Choose a Price')
    profit = fields.Many2one('pos.profit', string="Profit(%)")

    price = fields.Float(string='Sale Price', )

    @api.onchange('profit', 'product_template_id.standard_price')
    def compute_price(self):
        for rec in self:
            if rec.profit:
                price = (
                                rec.product_template_id.standard_price * rec.profit.value) / 100 + rec.product_template_id.standard_price
                tax = rec.product_template_id.taxes_id
                amount = 0
                for tax in tax:
                    amount += tax.amount
                tax_amount = (rec.product_template_id.standard_price * amount) / 100
                rec.price = price + tax_amount
            else:
                rec.price = 0


class PosPrice(models.Model):
    _name = 'pos.multi.price'

    name = fields.Char(string="Name")


class PosProfit(models.Model):
    _name = 'pos.profit'

    name = fields.Char(string="Name")
    value = fields.Float(string="Value")
