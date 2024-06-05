odoo.define('pos_product_creation.jobworkpopup', function(require) {
    'use strict';
    const { useState } = owl;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class jobworkpopup extends AbstractAwaitablePopup {
        init() {
            super.init(...arguments);
            $("select.advanced-select").select2();

        }
        setup() {
            super.setup();
            this.propsInfo = this.props.info;
            var productitems = [];
            _.each(this.propsInfo.orderlines, function (line) {
                productitems.push(line.product)
            });
            
            this.state = useState({
                selectedItem: [],
                itemQty : {},
                selectedService: false,
                isUrgent: false,
                currentInputQty: 0,
                jobwork_product: {},
                deliveryDate: false,
                estimatedDeliveryDate: false,
                partnerName: this.propsInfo.partner && this.propsInfo.partner.name || "",
                orderNumber: this.propsInfo.currentOrder.name,
                itemDetail: this.props.itemDetail,
                typeValue: this.props.startingValue,
                productValue: this.props.startingValue,
                priceValue: this.props.priceValue,
                productRef: this.props.startingValue,
                productImg: this.props.productImage,
                productItems: productitems,
                product_checked : false,
                jobwork_product_ids : []
            });
        }

        
        async _onSelectService (pro_id) {
            var input_class = ".service_selection_" + pro_id
            var service = $(input_class).val();
            if (!this.state.selectedItem.includes(pro_id)) {
                return
            }
            var self = this

            await this.rpc({
                model: 'job.work.product',
                method: 'set_jobwork_services',
                args: [[], {
                    prod_id: pro_id,
                    service: service,
                }],
                
            }).then(function (jobworkproduct) {
                if (jobworkproduct) {
                    self.state.jobwork_product_ids.push(jobworkproduct)
                }

            }); 
        
        }

        async _onSelectProduct (pro_id) {
            var item_checkbox_id = "item_checkbox_" + pro_id
            const checkbox = document.getElementById(item_checkbox_id);

            const isChecked = checkbox.checked;
            const input_qty_id = document.querySelector('.'+"input_qty_" + pro_id);
            const service_selection_id = document.querySelector('.'+"service_selection_" + pro_id);
            const service_detail_id = document.querySelector('.'+"input_service_detail_" + pro_id);
            if (isChecked) {
                input_qty_id.style.removeProperty("display")
                service_selection_id.style.removeProperty("display")
                service_detail_id.style.removeProperty("display")
            } else {
                service_detail_id.style.display = "none"
                service_selection_id.style.display = "none"
                input_qty_id.style.display = "none"
            }

            if (isChecked && !this.state.selectedItem.includes(pro_id)) {
                this.state.selectedItem.push(pro_id)
            } else if (!isChecked && this.state.selectedItem.includes(pro_id)) {
                this.state.selectedItem.pop(pro_id)   
            }

            var input_class = ".input_qty_" + pro_id
            var pro_qty = $(input_class).val();
            if (!this.state.selectedItem.includes(pro_id)) {
                return
            }
            var self = this
            
            if (!this.state.jobwork_product.hasOwnProperty(pro_id)) {

                await this.rpc({
                    model: 'job.work.product',
                    method: 'create_job_work_product',
                    args: [[], {
                        prod_id: pro_id,
                        qty: pro_qty,
                    }],
                    
                }).then(function (jobworkproduct) {
                    if (jobworkproduct) {
                        self.state.jobwork_product_ids.push(jobworkproduct)
                        self.state.jobwork_product[pro_id] = jobworkproduct
                    }
                    
                }); 
            }

            
        }

        
        async _onChangeServiceDetails (pro_id) {
            var input_class = ".input_service_detail_" + pro_id
            var service_details = $(input_class).val();
            if (!this.state.selectedItem.includes(pro_id)) {
                return
            }
            var self = this

            await this.rpc({
                model: 'job.work.product',
                method: 'set_jobwork_service_details',
                args: [[], {
                    prod_id: pro_id,
                    service_details: service_details,
                }],
                
            }).then(function (jobworkproduct) {
                if (jobworkproduct) {
                    self.state.jobwork_product_ids.push(jobworkproduct)
                }

            }); 
        
        }

        async _onChangeQty (pro_id) {
            var input_class = ".input_qty_" + pro_id
            var pro_qty = $(input_class).val();
            if (!this.state.selectedItem.includes(pro_id)) {
                return
            }
            var self = this

            await this.rpc({
                model: 'job.work.product',
                method: 'set_jobwork_qty',
                args: [[], {
                    prod_id: pro_id,
                    qty: pro_qty,
                }],
                
            }).then(function (jobworkproduct) {
                if (jobworkproduct) {
                    self.state.jobwork_product_ids.push(jobworkproduct)
                }

            }); 
        
        }
        

        getPayload() {
            var selected_vals = [];
            var category = this.state.typeValue;
            var product = this.state.productValue;
            var image = this.state.productImg;
            var product_reference = this.state.productRef;
            var price = this.state.priceValue;
            var unit = this.state.unitValue;
            var product_category = this.state.categoryValue;
            var barcode = this.state.barcodeValue;
            selected_vals.push(category);
            selected_vals.push(product);
            selected_vals.push(image);
            selected_vals.push(product_reference);
            selected_vals.push(price);
            selected_vals.push(unit);
            selected_vals.push(product_category);
            selected_vals.push(barcode);
            return selected_vals
        }

        confirm() {
            var values = {
                job_work_product_ids: this.state.jobwork_product_ids, bill_number: this.propsInfo.currentOrder.pos.invoice, product_ids: this.state.selectedItem, services: this.state.selectedService, priority: this.state.isUrgent, estimated_delivery_dates: this.state.estimatedDeliveryDate, delivery_dates: this.state.deliveryDate, payment_status: this.propsInfo.currentOrder.partial_payment && "partial" || "paid", partner_id: this.propsInfo.partner.id, description: this.state.itemDetail
            }
            this.rpc({
                model: 'job.work',
                method: 'create_jobwork',
                args: [[], values],
            });
            this.env.posbus.trigger("close-popup", {
                popupId: this.props.id,
                response: {
                    confirmed: false,
                    payload: null,
                },
            });
        }

        cancelb() {
            this.env.posbus.trigger("close-popup", {
                popupId: this.props.id,
                response: {
                    confirmed: false,
                    payload: null,
                },
            });
        }
    }


    jobworkpopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        array: [],
        title: 'Create ?',
        body: '',
        startingValue: '',
        priceValue: 1,
        list: []
    }

    jobworkpopup.template = 'jobworkpopup';
    Registries.Component.add(jobworkpopup);

    return jobworkpopup;
});