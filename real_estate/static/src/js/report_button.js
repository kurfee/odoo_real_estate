// static/src/js/report_button.js
odoo.define('real_estate.report_button', function (require) {
    'use strict';

    var ListController = require('web.ListController');

    ListController.include({
        _onButtonClicked: function (event) {
            if (event.data.attrs.custom === 'generate_report') {
                window.location.href = '/report/xlsx/real.estate/' + this.model.localData[event.data.id].res_id;
            } else {
                this._super(event);
            }
        }
    });
});
