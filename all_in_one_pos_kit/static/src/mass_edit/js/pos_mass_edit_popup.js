odoo.define('all_in_one_pos_kit.pos_mass_edit_popup', function(require) {
    'use strict';
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    class MassEditPopup extends AbstractAwaitablePopup {
        
        sendInput(ev, line_id) {
        //        Function to change quantity into 0
        console.log("this.props.body", this.props.body, line_id)
            _.each(this.props.body, function(edit) {
                if (edit.id == line_id) {
                    edit.quantity = ev.target.value
                }
            });

        }

        removeLine(line) {
            var order = this.env.pos.get_order()
            order.remove_orderline(line)
        }
    }
    MassEditPopup.template = 'MassEditPopup';
    MassEditPopup.defaultProps = {
    confirm: "Confirm",
    cancel: "Cancel",
    };
  Registries.Component.add(MassEditPopup);
  return MassEditPopup;
});
