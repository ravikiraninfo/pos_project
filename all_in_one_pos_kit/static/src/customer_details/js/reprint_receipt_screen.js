odoo.define('all_in_one_pos_kit.ReprintReceiptScreen', function(require) {
    'use strict';

    const ReprintReceiptScreen = require('point_of_sale.ReprintReceiptScreen');
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');

    const ReprintReceiptScreenDetails = (ReprintReceiptScreen) =>
        class extends ReprintReceiptScreen {
            confirm() {
                this.showScreen('TicketScreen', { reuseSavedUIState: true, customerDetail: true });
            }
        }

    Registries.Component.extend(ReprintReceiptScreen, ReprintReceiptScreenDetails);
    return ReprintReceiptScreen;
});