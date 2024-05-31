odoo.define('pos_invoice_automate.PosGlobalState', function(require) {
    'use strict';

    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');
    
    const posInvoiceAutomatePosGlobalState = (PosGlobalState) => class posInvoiceAutomatePosGlobalState extends PosGlobalState {
        get invoiceReportAction() {
            return "pos_invoice_automate.account_invoices_template";
          }
    }
    Registries.Model.extend(PosGlobalState, posInvoiceAutomatePosGlobalState);

});