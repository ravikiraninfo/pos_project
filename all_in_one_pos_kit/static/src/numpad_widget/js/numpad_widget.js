odoo.define('pos_blackbox_be.NumpadWidget', function(require) {
    'use strict';

    const NumpadWidget = require('point_of_sale.NumpadWidget');
    const Registries = require('point_of_sale.Registries');

    const AccessNumpadWidget = NumpadWidget => class extends NumpadWidget {
        changeMode(mode) {
            if (this.env.pos.get_cashier().role !== 'manager' && (mode == "discount" || mode === "discount_amount")) {
                this.showPopup('ErrorPopup', {
                title: this.env._t("POS error"),
                body: this.env._t("You have no Discount access."),
            });
            return;
            }
            return super.changeMode(mode);
        }
    };

    Registries.Component.extend(NumpadWidget, AccessNumpadWidget);

    return NumpadWidget;
 });
