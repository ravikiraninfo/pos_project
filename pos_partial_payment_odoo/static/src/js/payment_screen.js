odoo.define('pos_button.CustomButtonPaymentScreen', function (require) {
    'use strict';
    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { identifyError } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Chrome = require('point_of_sale.Chrome');
    const { useRef } = owl;
    var rpc = require('web.rpc')


    // Define the PartialPaymentButtonPaymentScreen class
    const PartialPaymentButtonPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup();
                this.root = useRef('PartialPayment');
            }
        //Partial Payment Button Functionality
        PartialPaymentButton() {
                if (this.currentOrder.partial_payment === false) {
                    this.currentOrder.partial_payment = true;
                    var validate = this.root.el
                    $(validate).addClass('highlight');
                } else {
                    this.currentOrder.partial_payment = false;
                    var validate = this.root.el
                    $(validate).removeClass('highlight');
                }
            }

            set_igst() {
                if (this.currentOrder.include_igst === false) {
                    this.currentOrder.include_igst = true;
                    console.log("this.currentOrder.include_igst", this.currentOrder.include_igst)
                    // var validate = this.root.el
                    // $(validate).addClass('highlight');
                } else {
                    this.currentOrder.include_igst = false;
                    // var validate = this.root.el
                    // $(validate).removeClass('highlight');
                }
            }
             async validateOrder(isForceValidate) {

                if (!this.currentOrder.partial_payment){
                await super.validateOrder(isForceValidate);
                    }
                else{

                if (this.currentOrder.get_partner().prevent_partial_payment ) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Partial Payment Not Allowed'),
                    body: this.env._t(
                        'The Customer is not allowed to make Partial Payments.'
                    ),
                });
                return false;
            };
            if (!this.currentOrder.get_partner().street) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Partial Payment Not Allowed'),
                    body: this.env._t(
                        'Customer address is required'
                    ),
                });
                return false;
            };
            //If Invoice not Selected Show Error
                if(!this.currentOrder.to_invoice){
                   this.showPopup('ErrorPopup', {
                    title: this.env._t('Cannot Validate This Order'),
                    body: this.env._t(
                        'You need to Set Invoice for Validating Partial Payments'
                    ),
                });
                return false;
            };
            //If amount is fully paid show error
            if(!this.currentOrder.get_due()){
                   this.showPopup('ErrorPopup', {
                    title: this.env._t('Cannot Validate This Order'),
                    body: this.env._t(
                        'The Amount is Fully Paid Disable Partial Payment to Validate this Order'
                    ),
                });
                return false;
            };
                this.currentOrder.is_partial_payment = true
                this._isOrderValid(isForceValidate)
                await this._finalizeValidation();
                }
                // await super.validateOrder(isForceValidate);

            }
        //Validate Payment Button Functionality
       async validateOrder(isForceValidate) {

               if (!this.currentOrder.partial_payment){
               await super.validateOrder(isForceValidate);
                   }
               else{
               if (this.currentOrder.get_partner().prevent_partial_payment ) {
               this.showPopup('ErrorPopup', {
                   title: this.env._t('Partial Payment Not Allowed'),
                   body: this.env._t(
                       'The Customer is not allowed to make Partial Payments.'
                   ),
               });
               return false;
           };
           if (!this.currentOrder.get_partner().street) {
               this.showPopup('ErrorPopup', {
                   title: this.env._t('Partial Payment Not Allowed'),
                   body: this.env._t(
                       'Customer address is required'
                   ),
               });
               return false;
           };
           //If Invoice not Selected Show Error
               if(!this.currentOrder.to_invoice){
                  this.showPopup('ErrorPopup', {
                   title: this.env._t('Cannot Validate This Order'),
                   body: this.env._t(
                       'You need to Set Invoice for Validating Partial Payments'
                   ),
               });
               return false;
           };
           //If amount is fully paid show error
           if(!this.currentOrder.get_due()){
                  this.showPopup('ErrorPopup', {
                   title: this.env._t('Cannot Validate This Order'),
                   body: this.env._t(
                       'The Amount is Fully Paid Disable Partial Payment to Validate this Order'
                   ),
               });
               return false;
           };
               this.currentOrder.is_partial_payment = true
               this._isOrderValid(isForceValidate)
               await this._finalizeValidation();
               }

               var info = {
                currentOrder : this.currentOrder,
                partner : this.currentOrder.get_partner(),
                orderlines : this.currentOrder.orderlines
            }
            var self = this
            const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter(); // Generate QR code and retrieve additional information from the server

            rpc.query({
                model: 'pos.order',
                method: 'get_invoice',
                args: [this.env.pos.selectedOrder.name]
            }).then(function(result) {
                const address = `${result.base_url}/my/invoices/${result.invoice_id}?`
                let qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(address, 150, 150));
                self.env.pos.qr_image = "data:image/svg+xml;base64," + window.btoa(qr_code_svg);
                let barcode_svg = new XMLSerializer().serializeToString(codeWriter.write(result.barcode, 150, 150));
                self.env.pos.barcode_image = "data:image/svg+xml;base64," + window.btoa(barcode_svg);
                self.env.pos.barcode = result.barcode
                self.env.pos.invoice = result.invoice_name
            });
            if (this.currentOrder.partial_payment) {
                await this.showPopup("jobworkpopup", { info: info });

            }

            //    await super.validateOrder(isForceValidate);
           }
        };
    Registries.Component.extend(PaymentScreen, PartialPaymentButtonPaymentScreen);
    return PartialPaymentButtonPaymentScreen;
});
