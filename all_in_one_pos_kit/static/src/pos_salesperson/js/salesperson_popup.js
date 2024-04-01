/**@odoo-module **/
import AbstractAwaitablePopup from "point_of_sale.AbstractAwaitablePopup";
import Registries from "point_of_sale.Registries";
const { useRef } = owl;
var core = require('web.core');
const { Gui } = require('point_of_sale.Gui');
var _t = core._t;
class SalesPersonPopup extends AbstractAwaitablePopup {
    /**
     * Set up the custom popup component and initialize its reference to the salesperson dropdown.
     */
    setup() {
        super.setup();
        this.salePersonRef = useRef('salePersonRef')
    }
    /**
     * Confirm the selection of a salesperson for the selected orderline, and close the popup.
     * If no orderline is selected, an error message is displayed instead.
     */
    confirm() {
        if (this.env.pos.selectedOrder.selected_orderline) {
             var order = this.env.pos.get_order();
order.get_orderlines().filter(line => line.get_product())
    .forEach(line => {
        const product = line.get_product();
        let option = this.salePersonRef.el.selectedOptions[0];
        const newSalesperson = [parseInt(option.id), option.value];

        // Check if salesperson array exists, if not initialize it
        if (!line.salesperson) {
            line.salesperson = [];
        }

        // Check if the new salesperson already exists in the list
        const existingSalesperson = line.salesperson.find(salesperson => salesperson[0] === newSalesperson[0]);
        if (!existingSalesperson) {
            // Add new salesperson to the list
            line.salesperson.push(newSalesperson);
        }
        console.log('saaaaaaaa',line.salesperson)
    });
            this.env.posbus.trigger("close-popup", {
                popupId: this.props.id,
                response: {
                    confirmed: true,
                    payload: null,
                },
            });
        }
        else {
            Gui.showPopup("ErrorPopup", {
                'title': _t("Error"),
                'body': _.str.sprintf(_t('You should add product first')),
            });
            return false;
        }
    }
    /**
     * Cancel the selection of a salesperson for the selected orderline, and close the popup.
     */
    cancel() {
        this.env.posbus.trigger("close-popup", {
            popupId: this.props.id,
            response: {
                confirmed: false,
                payload: null,
            },
        });
    }
}
SalesPersonPopup.template = "SalesPersonPopup";
Registries.Component.add(SalesPersonPopup);
