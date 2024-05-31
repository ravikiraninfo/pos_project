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


class ProductTemplate(models.Model):
    """Inherits model 'product.template' and adds field to set multiple units
    of measure"""
    _inherit = 'product.template'

    multi_uom = fields.Boolean(compute='_compute_multi_uom', string='Multi UoM',
                               help='A boolean field to show the one2many field'
                                    'POS Multiple UoM if the Multi UoM option'
                                    ' is enabled in Configuration settings')
    pos_multi_uom_ids = fields.One2many('pos.multi.uom', 'product_template_id',
                                        string="POS Multiple Price",
                                        )
    
    @api.depends('pos_multi_uom_ids', "pos_multi_uom_ids.price")
    def _compute_list_price(self):
        for tmpl in self:
            price_id = self.env['pos.multi.price'].search([('name', '=', 'List Price')]).id
            tmpl.list_price = sum(tmpl.pos_multi_uom_ids.filtered(lambda x: x.uom_id.id == price_id).mapped('price'))


    def _compute_multi_uom(self):
        """
         Updates the 'multi_uom' field based on the configuration parameter
          'product_multi_uom_pos.pos_multi_uom'.
        """
        status = self.env['ir.config_parameter'].sudo().get_param(
            'product_multi_uom_pos.pos_multi_uom')
        self.write({
            'multi_uom': status
        })

class Productproduct(models.Model):
    """Inherits model 'product.template' and adds field to set multiple units
    of measure"""
    _inherit = 'product.product'

    multi_uom = fields.Boolean(compute='_compute_multi_uom', string='Multi UoM',
                               help='A boolean field to show the one2many field'
                                    'POS Multiple UoM if the Multi UoM option'
                                    ' is enabled in Configuration settings')
    pos_multi_uom_ids = fields.One2many('pos.multi.uom', 'product_template_id_2',
                                        string="POS Multiple Price",
                                        )

    def _compute_multi_uom(self):
        """
         Updates the 'multi_uom' field based on the configuration parameter
          'product_multi_uom_pos.pos_multi_uom'.
        """
        status = self.env['ir.config_parameter'].sudo().get_param(
            'product_multi_uom_pos.pos_multi_uom')
        self.write({
            'multi_uom': status
        })
