odoo.define('pos_partiel_payment_odoo.PartnerDetailsEdit', function (require) {
    'use strict';

    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    const PartnerDetailsEditCust = PartnerDetailsEdit => class extends PartnerDetailsEdit {
            setup() {
                super.setup();
                const partner = this.props.partner;

                this.changes = useState({
                    name: partner.name || "",
                    street: partner.street || "",
                    city: partner.city || "",
                    zip: partner.zip || "",
                    state_id: partner.state_id && partner.state_id[0],
                    country_id: partner.country_id && partner.country_id[0],
                    lang: partner.lang || "",
                    email: partner.email || "",
                    phone: partner.phone || "",
                    mobile: partner.mobile || "",
                    barcode: partner.barcode || "",
                    vat: partner.vat || "",
                    property_product_pricelist: this.getDefaultPricelist(partner),
                    customer_id: partner.vendor_code,
                    date_of_anniversary: partner.date_of_anniversary
                });
            }
        };
        Registries.Component.extend(PartnerDetailsEdit, PartnerDetailsEditCust);
        return PartnerDetailsEdit;
});
