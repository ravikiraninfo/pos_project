odoo.define('all_in_one_pos_kit.updateprice', function(require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const {
        useListener
    } = require("@web/core/utils/hooks");
    var rpc = require('web.rpc');
    class UpdatePrice extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this._onClick);
        }
        async _onClick() { //Click button service charge
            var self = this;
            console.log('lll',this.env.pos.pos_multi_price)
            try {
            let list = this.productsList;
            this.showPopup("PricesPopup", {
                'prices': this.env.pos.pos_multi_price
            });

        } catch (error) {
            if (isConnectionError(error)) {
                this.showPopup("ErrorPopup", {
                    title: this.env._t("Network Error"),
                    body: this.env._t("Cannot access Product screen if offline."),
                });
            } else {
                throw error;
            }
        }

        }
    }
    UpdatePrice.template = 'MultiplePriceButton';
    ProductScreen.addControlButton({
        component: UpdatePrice,
        condition: function() {
            return true
        },
    });
    Registries.Component.add(UpdatePrice);
    return UpdatePrice;
});