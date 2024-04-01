from odoo import models,fields


class Partner(models.Model):
    _inherit = "res.partner"

    vendor_code = fields.Char(string="Vendor Code")