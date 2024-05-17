odoo.define('all_in_one_pos_kit.pos_show_customer_details_button', function(require) {
    'use strict';
        const Registries = require('point_of_sale.Registries');
        const PosComponent = require('point_of_sale.PosComponent');
        const ProductScreen = require('point_of_sale.ProductScreen');
        const { useListener } = require("@web/core/utils/hooks");

        class ShowCustomerDetails extends PosComponent {
    //    Extend the POS session to add order line edit button
            setup() {
                super.setup();
                useListener('click', this.onClick);
            }

            onClick() {
                const partner = this.env.pos.get_order().get_partner();
                const searchDetails = partner ? { fieldName: 'PARTNER', searchTerm: partner.name } : {};
                this.showScreen('TicketScreen', {
                    ui: { filter: 'SYNCED', searchDetails },
                    destinationOrder: this.env.pos.get_order(),
                    customerDetail: true
                });
            }
            
            // async onClick() {
            //     // SHOW DETAIL button Onclick()
            //     var current_order = this.env.pos.get_order();
            //     var current_customer = current_order.get_partner();
            //     var all_orders = this.env.pos.db.load('orders');
            //     console.log("all_orders", all_orders)
            //     // var all_receipts = this.env.pos.get_order().get_orderlines();
            //     if (!current_customer) {
            //         return this.showPopup('ErrorPopup', {
            //             title: this.env._t('Customer not Set'),
            //             body: this.env._t('There is no Customer set for the order.'),
            //         });
            //     }
            //     if (!all_orders.length){
            //     //        Popup if no product in pos order line
            //         return this.showPopup('ErrorPopup', {
            //             title: this.env._t('Not Found'),
            //             body: this.env._t('There is no past orders for this customer.'),
            //         });
            //     }
            //     const { confirmed } = await this.showTempScreen(
            //         'CustomerDetailsScreen',
            //         { order: current_order }
            //     );
               
            // }
        }
        ShowCustomerDetails.template = 'ShowCustomerDetails';
        ProductScreen.addControlButton({
            component: ShowCustomerDetails,
            condition: function() {
              return this.env.pos;
            },
        });
        Registries.Component.add(ShowCustomerDetails);
        return ShowCustomerDetails;
    });
    