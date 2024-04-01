/**@odoo-module **/
import AbstractAwaitablePopup from "point_of_sale.AbstractAwaitablePopup";
import Registries from "point_of_sale.Registries";
const { useRef } = owl;
var core = require('web.core');
const { Gui } = require('point_of_sale.Gui');
var _t = core._t;
class PricesPopup extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.salePersonRef = useRef('priceRef')
    }
    confirm() {
        if (this.env.pos.selectedOrder.selected_orderline) {
            var order = this.env.pos.get_order();
         order.get_orderlines().filter(line => line.get_product())
    .forEach(line => {
        const product = line.get_product();
        const multiUomIds = product.pos_multi_uom_ids;

        if (multiUomIds && multiUomIds.length > 0) {
            const option = this.salePersonRef.el.selectedOptions[0];
            let matchedRecord = null;
            multiUomIds.forEach(id => {
                const record = this.env.pos.pos_multi_uom.find(record =>
                    record.id === id && record.uom_id[0] === parseInt(option.id));
                if (record) {
                    matchedRecord = record;
                }
            });

            if (matchedRecord) {
                const price = matchedRecord.price;
                line.set_unit_price(price);
            } else {
                console.error('No matching record found for multiUomIds and selected option');
            }
        }
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
PricesPopup.template = "PricesPopup";
Registries.Component.add(PricesPopup);
