odoo.define('pos_product_creation.selectItemPopup', function(require) {
    'use strict';
    const { useState } = owl;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class selectItemPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            // this.propsInfo = this.props.info
            // var productnames = {}
            // _.each(this.propsInfo.orderlines, function (line) {
            //     productnames[line.id] = line.product.name
            // });
            // console.log("productNames", productnames)
            this.state = useState({
                currentOrder: this.props.currentOrder
               
            });
        }
        // getPayload() {
        //     var selected_vals = [];
        //     var category = this.state.typeValue;
        //     var product = this.state.productValue;
        //     var image = this.state.productImg;
        //     var product_reference = this.state.productRef;
        //     var price = this.state.priceValue;
        //     var unit = this.state.unitValue;
        //     var product_category = this.state.categoryValue;
        //     var barcode = this.state.barcodeValue;
        //     selected_vals.push(category);
        //     selected_vals.push(product);
        //     selected_vals.push(image);
        //     selected_vals.push(product_reference);
        //     selected_vals.push(price);
        //     selected_vals.push(unit);
        //     selected_vals.push(product_category);
        //     selected_vals.push(barcode);
        //     return selected_vals
        // }

        confirm() {
            // let partnerId = this.rpc({
            //     model: 'project.task',
            //     method: 'create',
            //     args: [{name: this.propsInfo.currentOrder.name, partner_id: this.propsInfo.partner.id, description: this.state.itemDetail}],
            // });
            this.env.posbus.trigger("close-popup", {
                popupId: this.props.id,
                response: {
                    confirmed: false,
                    payload: null,
                },
            });
        }

        cancelb() {
            this.env.posbus.trigger("close-popup", {
                popupId: this.props.id,
                response: {
                    confirmed: false,
                    payload: null,
                },
            });
        }

    }


    selectItemPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        array: [],
        title: 'Select Items',
        body: '',
        startingValue: '',
        priceValue: 1,
        list: []
    }

    selectItemPopup.template = 'selectItemPopup';
    Registries.Component.add(selectItemPopup);

    return selectItemPopup;
});