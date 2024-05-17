/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { Orderline } from 'point_of_sale.models';


patch(Orderline.prototype, 'order_line_patch', {
    /**
     * Sets onboarding step state as completed.
     *
     * @override
     */
        get_all_prices(qty = this.get_quantity()){

        var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
        if (this.pos.numpadMode == 'discount_amount') {
            var price_unit = this.get_unit_price() - this.get_discount();
        }
        var taxtotal = 0;
    
        var product =  this.get_product();
        var taxes_ids = this.tax_ids || product.taxes_id;
        taxes_ids = _.filter(taxes_ids, t => t in this.pos.taxes_by_id);
        var taxdetail = {};
        var product_taxes = this.pos.get_taxes_after_fp(taxes_ids, this.order.fiscal_position);
    
        var all_taxes = this.compute_all(product_taxes, price_unit, qty, this.pos.currency.rounding);
        var all_taxes_before_discount = this.compute_all(product_taxes, this.get_unit_price(), qty, this.pos.currency.rounding);
        _(all_taxes.taxes).each(function(tax) {
            taxtotal += tax.amount;
            taxdetail[tax.id] = {
                amount: tax.amount,
                base: tax.base,
            };
        });
    
        return {
            "priceWithTax": all_taxes.total_included,
            "priceWithoutTax": all_taxes.total_excluded,
            "priceWithTaxBeforeDiscount": all_taxes_before_discount.total_included,
            "priceWithoutTaxBeforeDiscount": all_taxes_before_discount.total_excluded,
            "tax": taxtotal,
            "taxDetails": taxdetail,
            "tax_percentages": product_taxes.map((tax) => tax.amount),
        };
    },

    get_discount_amount_str(){
        if (this.pos.numpadMode == "discount_amount") {
            return this.discountStr;
        }
        return '0'
    }

        
});
