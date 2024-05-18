odoo.define('pos_product_creation.jobworkpopup', function(require) {
    'use strict';
    const { useState } = owl;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class jobworkpopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.propsInfo = this.props.info
            this.state = useState({
                partnerName: this.propsInfo.partner && this.propsInfo.partner.name || "",
                orderNumber: this.propsInfo.currentOrder.name,
                itemDetail: this.props.itemDetail,
                typeValue: this.props.startingValue,
                productValue: this.props.startingValue,
                priceValue: this.props.priceValue,
                productRef: this.props.startingValue,
                productImg: this.props.productImage,
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
        }

        // cancel() {
        //     this.closePopup("jobworkpopup")
        // }
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