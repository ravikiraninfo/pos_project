from odoo import fields, models, api, _

class GateInOut(models.Model):
    _name = "gate.in.out"
    _descriptiin = "Gate In/Out"

    name = fields.Char(default="New", readonly=True)
    in_state = fields.Selection(selection=[("new", "New"), ('received', 'Received'), ('unpacked', 'Unpacked')], default="new", readonly=False)
    out_state = fields.Selection(selection=[("new", "New"), ('packed', 'Packed'), ('dispatched', 'Dispatched')], default="new", readonly=False)

    type = fields.Selection(selection=[("in", "IN"), ("out", "OUT")], required=True)
    receipt_invoice = fields.Char("Delivery Challan / Invoice number")
    courier_company = fields.Many2one("res.partner")
    vendor_id = fields.Many2one("res.partner", string="Vendor")
    courier_company_phone = fields.Char("")
    delivery_boy = fields.Char("Delivery Boy")
    delivery_boy_phone = fields.Char("Delivery Boy Phone")
    goods_quantity = fields.Float()
    product_tmpl_ids = fields.Many2many("product.template")
    gate_in_date = fields.Datetime()
    gate_out_date = fields.Datetime()
    no_of_packages = fields.Float("No. Of Packages", required=True)

    goods_return = fields.Float()

    customer_name = fields.Many2one("res.partner")
    description = fields.Char()
    vehicle_no = fields.Char()
    
    customer_address = fields.Char()
    tracking_number = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('gate.in.out') or _('New')
        return super().create(vals_list)


    def mark_as_packed(self):
        self.out_state = 'packed'

    def mark_as_dispatched(self):
        self.out_state = 'dispatched'

    def mark_as_received(self):
        self.in_state = 'received'
    
    def mark_as_unpacked(self):
        self.in_state = 'unpacked'

    def reset_to_new(self):
        self.in_state = 'new'
        self.out_state = 'new'