odoo.define('custom_product.models', function (require) {
    "use strict";

    var { Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PatchPosLotaltyOrder = (Order) => class PatchPosLotaltyOrder extends Order {
        _updateRewards () {
            if (this.pos.programs === 0 || this.pos.programs.length === 0) {
                return;
            }
            super._updateRewards();
        }
    }

    Registries.Model.extend(Order, PatchPosLotaltyOrder);


});