odoo.define('all_in_one_pos_kit.salesperson', function(require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const {
        useListener
    } = require("@web/core/utils/hooks");
    var rpc = require('web.rpc');
    class Salesperson extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this._onClick);
        }
        async _onClick() { //Click button service charge
            var self = this;
//            try {
            let list = this.productsList;
            this.showPopup("SalesPersonPopup", {
                'user_id': this.env.pos.res_users,
                'employee_id': this.env.pos.employee_ids
            });

//        }
//        catch (error) {
//            if (isConnectionError(error)) {
//                this.showPopup("ErrorPopup", {
//                    title: this.env._t("Network Error"),
//                    body: this.env._t("Cannot access Product screen if offline."),
//                });
//            } else {
//                throw error;
//            }
//        }

        }
    }
    Salesperson.template = 'SalesPersonButton';
    ProductScreen.addControlButton({
        component: Salesperson,
        condition: function() {
            return true
        },
    });
    Registries.Component.add(Salesperson);
    return Salesperson;
});