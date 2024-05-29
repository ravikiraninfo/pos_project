from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_open_label_layout(self):
        # flake8: noqa: E501
        if not self.env['ir.config_parameter'].sudo().get_param('garazd_product_label.replace_standard_wizard'):
            return super(ProductProduct, self).action_open_label_layout()
        action = self.env['ir.actions.act_window']._for_xml_id('garazd_product_label.action_print_label_from_product')
        action['context'] = {'default_product_ids': self.ids}
        return action

    def _get_att_vals(self):
        vals = {}
        for line in self.product_tmpl_id.attribute_line_ids:
            vals[line.attribute_id.name] = ""
            variant_att_vals = self.product_template_attribute_value_ids.mapped("name")
            if line.attribute_id.name.lower() in ["color", 'colour']:
                for value in variant_att_vals:
                    if value in line.value_ids.mapped('name'):
                        vals[line.attribute_id.name] = value
            else:
                vals[line.attribute_id.name] = line.value_ids[0].name
        work_tags = ",".join(self.product_tmpl_id.product_tag_ids.mapped("name"))
        if work_tags:
            vals["Work"] = work_tags
        return vals