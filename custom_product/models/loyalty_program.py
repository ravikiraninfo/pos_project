# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models

class LoyaltyProgram(models.Model):
    _inherit = 'loyalty.program'

    pos_categ_id = fields.Many2one(
        'pos.category', string='Point of Sale Category',
        help="Category used in the Point of Sale.")