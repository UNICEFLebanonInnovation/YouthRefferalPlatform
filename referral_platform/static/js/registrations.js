/**
 * Created by ali on 7/7/17.
 */
$(document).ready(function(){

    change_education_status($('select#id_education_status').val());
    
    $('#id_birthdate').datetimepicker({
        "format": "mm/dd/yyyy",
        "pickTime": false,
        "viewMode": "years",
        "stepping": 0,
        "showClear": true,
        "showClose": true,
        "disabledHours": true
    });

    $('select#id_education_status').change(function(){
        change_education_status($(this).val());
    });

});

function change_education_status(value) {

    $('#education_type_q').addClass('hidden');
    $('#div_id_education_type').parent().addClass('hidden');

    $('#education_level_q').addClass('hidden');
    $('#div_id_education_level').parent().addClass('hidden');

    $('#leaving_education_reasons_q').addClass('hidden');
    $('#div_id_leaving_education_reasons').parent().addClass('hidden');

    if(value == 'currently_studying') {
        $('#education_type_q').removeClass('hidden');
        $('#div_id_education_type').parent().removeClass('hidden');
    }else if(value == 'stopped_studying'){
        $('#education_level_q').removeClass('hidden');
        $('#div_id_education_level').parent().removeClass('hidden');

        $('#leaving_education_reasons_q').removeClass('hidden');
        $('#div_id_leaving_education_reasons').parent().removeClass('hidden');
    }
}
