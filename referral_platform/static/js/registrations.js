/**
 * Created by ali on 7/7/17.
 */
$(document).ready(function(){

    $('#id_birthdate').datetimepicker({
        "format": "mm/dd/yyyy",
        "pickTime": false,
        "viewMode": "years",
        "stepping": 0,
        "showClear": true,
        "showClose": true,
        "disabledHours": true
    });

});
