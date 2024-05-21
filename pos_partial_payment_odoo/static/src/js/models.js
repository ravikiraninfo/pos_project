/** @odoo-module **/
import models from 'point_of_sale.models';
import {Order} from 'point_of_sale.models';
import  Registries from "point_of_sale.Registries";
// Define the Partial class
const Partial = (Order) => class Partial extends Order {
     constructor() {
     super(...arguments);
     this.partial_payment =  false
     this.include_igst =  false
     this.is_partial_payment = this.is_partial_payment || false;
     }
     set_order_suggestion(suggestion){
     this.is_partial_payment = is_partial_payment
     }
     //send order data to send to the server
     export_as_JSON() {
     const json = super.export_as_JSON(...arguments)
     json.is_partial_payment = this.is_partial_payment ;
     json.include_igst = this.include_igst ;
     json.religion = this.religion ;
     json.date_of_birth = this.date_of_birth ;
     json.relation = this.relation ;
     json.customer_id = this.customer_id ;
     return json;
     }
     init_from_JSON(json) {
     super.init_from_JSON(...arguments);
     this.is_partial_payment = json.is_partial_payment;
     this.include_igst = json.include_igst;
      this.religion = this.religion ;
     this.date_of_birth = this.date_of_birth ;
     this.relation = this.relation ;
     this.customer_id = this.customer_id ;
      }
};
Registries.Model.extend(Order, Partial)