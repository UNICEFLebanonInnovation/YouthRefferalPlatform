/* eslint-disable no-undef */
/**
 * Created by ali on 7/7/17.
 */
$(document).ready(function() {

  change_education_status($('select#id_education_status').val());
  change_employment_status($('input[name=employment_status]:checked').val());
  change_communication_preference($('select#id_communication_preference').val());

  // $('#id_birthdate').datetimepicker({
  //   format: 'mm/dd/yyyy',
  //   pickTime: false,
  //   viewMode: 'years',
  //   stepping: 0,
  //   showClear: true,
  //   showClose: true,
  //   disabledHours: true,
  // });

  $('select#id_education_status').change(function() {
    change_education_status($(this).val());
  });

  $('input[name=employment_status]').click(function() {
    change_employment_status($(this).val());
  });

  $('select#id_communication_preference').change(function() {
    change_communication_preference($(this).val());
  });


  if ($(document).find('#id_search_youth').length == 1) {

    $('#id_search_youth').autocomplete({
      source: function(request, response) {
        $.ajax({
          url: '/api/young-person/',
          dataType: 'json',
          data: {
            term: request.term,
          },
          success: function(data) {
            response(data);
          },
        });
      },
      minLength: 3,
      select: function(event, ui) {
        let registry_id = 0;
        console.log(ui.item);
        registry_id = ui.item.id;
        let params = {
          youth_id: registry_id,
        };
        let str = '?' + jQuery.param(params);
        window.location = $(document).find('form').attr('action') + str;
        return false;
      },
    }).autocomplete('instance')._renderMenu = function(ul, items) {
      let that = this;
      $.each(items, function(index, item) {
        that._renderItemData(ul, item);
      });
      $(ul).find('li:odd').addClass('odd');
    };

    $('#id_search_youth').autocomplete('instance')._renderItem = function(ul, item) {
      return $('<li>')
                .append("<div style='border: 1px solid;'>"
                   + '<b>Base Data:</b>' + item.last_name + ' ' + item.father_name + ' ' + item.first_name
                    + '<br/> <b>Gender - Birthday:</b> ' + item.sex + ' - ' + item.birthday_day + '/' + item.birthday_month + '/' + item.birthday_year
                    + '</div>')
                .appendTo(ul);
    };

    $('#continue').click(function() {
        $('#id_override_submit').attr('value',1);
        $('form').submit();
    });


  }




});

function change_education_status(value) {

  $('#education_type_q').addClass('hidden');
  $('#div_id_education_type').parent().addClass('hidden');

  $('#education_level_q').addClass('hidden');
  $('#div_id_education_level').parent().addClass('hidden');

  $('#leaving_education_reasons_q').addClass('hidden');
  $('#div_id_leaving_education_reasons').parent().addClass('hidden');

  if (value == 'currently_studying') {
    $('#education_type_q').removeClass('hidden');
    $('#div_id_education_type').parent().removeClass('hidden');
  } else if (value == 'stopped_studying') {
    $('#education_level_q').removeClass('hidden');
    $('#div_id_education_level').parent().removeClass('hidden');

    $('#leaving_education_reasons_q').removeClass('hidden');
    $('#div_id_leaving_education_reasons').parent().removeClass('hidden');
  }
}


$(document).on('click', '.delete-registration-row', function() {
  let item = $(this);
  if (confirm($(this).attr('translation'))) {
    let callback = function() {
      item.parents('tr').remove();
    };
    delete_entry(item, callback());
  }
});



function delete_entry(item, callback) {
  let url = item.attr('data-action');
  let pk = item.attr('itemscope');
  $.ajax({
    type: 'DELETE',
    url: url + pk + '/',
    cache: false,
    async: false,
    headers: getHeader(),
    dataType: 'json',
    success: function(response) {
      if (callback != undefined) {
        callback();
      }
      console.log(response);
    },
    error: function(response) {
      console.log(response);
    },
  });
}


function change_employment_status(value) {

  $('#employment_sectors_q').addClass('hidden');
  $('#employment_sectors_q').parent().addClass('hidden');

  $('#through_whom_q').addClass('hidden');
  $('#through_whom_q').parent().addClass('hidden');

  $('#obstacles_for_work_q').addClass('hidden');
  $('#obstacles_for_work_q').parent().addClass('hidden');

  if (value == 'full_time' || value == 'part_time' || value == 'summer_only') {
    $('#employment_sectors_q').removeClass('hidden');
    $('#employment_sectors_q').parent().removeClass('hidden');
  } else if (value == 'looking_for_work') {
    $('#through_whom_q').removeClass('hidden');
    $('#through_whom_q').parent().removeClass('hidden');

    $('#obstacles_for_work_q').removeClass('hidden');
    $('#obstacles_for_work_q').parent().removeClass('hidden');
  }
}

function change_communication_preference(value) {
  // console.log(value);

  $('#communication_channel_q').addClass('hidden');
  $('#communication_channel_q').parent().addClass('hidden');
  $('#div_id_communication_channel').parent().addClass('hidden');

  if (value == 'facebook' || value == 'email' || value == 'mobile') {
    $('#communication_channel_q').removeClass('hidden');
    $('#communication_channel_q').parent().removeClass('hidden');
    $('#div_id_communication_channel').parent().removeClass('hidden');
  }
}
