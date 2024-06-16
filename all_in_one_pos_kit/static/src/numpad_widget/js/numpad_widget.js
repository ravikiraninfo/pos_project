odoo.define('pos_blackbox_be.NumpadWidget', function(require) {
    'use strict';

    const NumpadWidget = require('point_of_sale.NumpadWidget');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');



    const AccessNumpadWidget = NumpadWidget => class extends NumpadWidget {
        async changeMode(mode) {
            if (this.env.pos.get_cashier().role !== 'manager' && (mode == "discount" || mode === "discount_amount")) {
                const { confirmed, payload } =  await Gui.showPopup('ManagerPasswordPopup', {
                    title: this.env._t("Password Required"),
                });
                if (confirmed) {
                    return super.changeMode(mode);
                }
                return
            }
            return super.changeMode(mode);
        }
    };

    Registries.Component.extend(NumpadWidget, AccessNumpadWidget);

    
    class ManagerPasswordPopup extends AbstractAwaitablePopup { 
        setup() {
            super.setup();
        }

    
        async confirm() {
            console.log("OKaY")
            var input_class = ".o_manager_password_input"
            var input_password = $(input_class).val();
            var password = this.env.pos.config.manager_password
            console.log("this.env.pos.config", this.env.pos.config)
            console.log("input_password", input_password)
            console.log("password", password)
            if (input_password != password) {
                await this.showPopup('ErrorPopup', { title: "Wrong Password", body:"You have entered wrong password." });
            } else {
                return super.confirm()
            }
        }
    }
    ManagerPasswordPopup.template = 'ManagerPasswordPopup';
    // ManagerPasswordPopup.defaultProps = { cancelKey: false };
    Registries.Component.add(ManagerPasswordPopup);
    
    return {
        NumpadWidget: NumpadWidget,
        ManagerPasswordPopup: ManagerPasswordPopup,
        };
 });
