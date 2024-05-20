odoo.define('pos_product_creation.jobworkpopup', function(require) {
    'use strict';
    const { useState } = owl;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class jobworkpopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.propsInfo = this.props.info
            console.log("this.propsInfo.currentOrder.orderlines", this.propsInfo.orderlines)
            var productitems = []
            _.each(this.propsInfo.orderlines, function (line) {
                productitems.push(line.product.name)
            });
            this.state = useState({
                partnerName: this.propsInfo.partner && this.propsInfo.partner.name || "",
                orderNumber: this.propsInfo.currentOrder.name,
                itemDetail: this.props.itemDetail,
                typeValue: this.props.startingValue,
                productValue: this.props.startingValue,
                priceValue: this.props.priceValue,
                productRef: this.props.startingValue,
                productImg: this.props.productImage,
                productItems: productitems
            });
        }
        getPayload() {
            var selected_vals = [];
            var category = this.state.typeValue;
            var product = this.state.productValue;
            var image = this.state.productImg;
            var product_reference = this.state.productRef;
            var price = this.state.priceValue;
            var unit = this.state.unitValue;
            var product_category = this.state.categoryValue;
            var barcode = this.state.barcodeValue;
            selected_vals.push(category);
            selected_vals.push(product);
            selected_vals.push(image);
            selected_vals.push(product_reference);
            selected_vals.push(price);
            selected_vals.push(unit);
            selected_vals.push(product_category);
            selected_vals.push(barcode);
            return selected_vals
        }

        confirm() {
            console.log("this.propsInfo.currentOrder.id", this.propsInfo.currentOrder.partial_payment)
            let partnerId = this.rpc({
                model: 'job.work',
                method: 'create',
                args: [{payment_status: this.propsInfo.currentOrder.partial_payment && "partial" || "paid", partner_id: this.propsInfo.partner.id, description: this.state.itemDetail}],
            });
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


    jobworkpopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        array: [],
        title: 'Create ?',
        body: '',
        startingValue: '',
        priceValue: 1,
        list: []
    }

    jobworkpopup.template = 'jobworkpopup';
    Registries.Component.add(jobworkpopup);

    return jobworkpopup;
});