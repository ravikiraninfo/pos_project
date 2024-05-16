odoo.define('all_in_one_pos_kit.pos_customer_detail_line', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class OrderDetailLine extends PosComponent {
        get highlight() {
            return this._isOrderSelected ? 'highlight' : '';
        }
        get shortAddress() {
            const { order } = this.props;
            return order.address;
        }
        get _isorderSelected() {
            return this.props.order === this.props.selectedOrder;
        }

        clickOrder() {
            // SHOW DETAIL button Onclick()
            var current_order = this.env.pos.get_order();
            var current_customer = current_order.get_partner();
            var all_orders = this.env.pos.db.load('orders');
            // var all_receipts = this.env.pos.get_order().get_orderlines();
            if (!current_customer) {
                return this.showPopup('ErrorPopup', {
                    title: this.env._t('Customer not Set'),
                    body: this.env._t('There is no Customer set for the order.'),
                });
            }
            if (!all_orders.length){
            //        Popup if no product in pos order line
                return this.showPopup('ErrorPopup', {
                    title: this.env._t('Not Found'),
                    body: this.env._t('There is no past orders for this customer.'),
                });
            }
            const { confirmed } = this.showTempScreen(
                'singleOrderDetail',
                { order: current_order }
            );
           
        }
    }
    OrderDetailLine.template = 'OrderDetailLine';

    Registries.Component.add(OrderDetailLine);

    return OrderDetailLine;
});
