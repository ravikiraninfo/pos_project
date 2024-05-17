# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models

class ExtraCost(models.Model):
    _name = 'extra.cost'

    name = fields.Char("Description")
    product_tmpl_id = fields.Many2one("product.template")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
    
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True)


    amount = fields.Monetary(currency_field='currency_id')