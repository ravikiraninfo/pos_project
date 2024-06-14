odoo.define('all_in_one_pos_kit.ClosePosPopup', function (require) {
    'use strict';

    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const Registries = require('point_of_sale.Registries');

    const AccessClosePopup = (ClosePosPopup) =>
        class extends ClosePosPopup {
            async confirm() {
                if (this.env.pos.get_cashier().role !== 'manager') {
                        await this.showPopup('ErrorPopup', {
                            title: this.env._t("POS error"),
                            body: this.env._t("You have no Closing access."),
                        });
                        return;
                }
                return super.confirm();
            }

        };

    Registries.Component.extend(ClosePosPopup, AccessClosePopup);

    return ClosePosPopup;
});
