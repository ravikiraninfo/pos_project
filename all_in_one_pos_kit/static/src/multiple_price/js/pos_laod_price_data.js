odoo.define('all_in_one_pos_kit.pos_multi', function (require) {
"use strict";
    // Import the required modules
    var {PosGlobalState} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    // Extend the PosGlobalState class
    const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState {
    async _processData(loadedData){
        await super._processData(...arguments);
        this.pos_multi_price = loadedData['pos_multi_price'];
        }
    }
    // Extend the PosGlobalState model using the NewPosGlobalState class
    Registries.Model.extend(PosGlobalState,NewPosGlobalState)
 });
