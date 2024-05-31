from odoo import api, models, fields, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_jobwork_team = fields.Boolean("Is a Job Work Team")
