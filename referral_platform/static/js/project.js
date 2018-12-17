/* Project specific Javascript goes here. */
/* Project specific Javascript goes here. */
/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');
var user_token = null;
var csrftoken = getCookie('csrftoken');
var href_full_path = '';
var db = null;

hashCode = function(str){
    var hash = 0;
    if (str.length == 0) return hash;
    for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash);
};

djb2Code = function(str){
    var hash = 5381;
    for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash = ((hash << 5) + hash) + char; /* hash * 33 + c */
    }
    return hash;
};

sdbmCode = function(str){
    var hash = 0;
    for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash = char + (hash << 6) + (hash << 16) - hash;
    }
    return hash;
};

loseCode = function(str){
    var hash = 0;
    for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash += char;
    }
    return hash;
};

$(document).on('click', '#radioBtn a', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).prop('value', sel);
    $('#'+tog+'_'+sel).trigger('click');

    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 *
 * @returns yyyy-mm-dd
 */
function getCurrentDate()
{
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!

    var yyyy = today.getFullYear();
    if(dd<10){
        dd='0'+dd
    }
    if(mm<10){
        mm='0'+mm
    }
    return yyyy+'-'+mm+'-'+dd;
}

function generate_student_number(student)
{
    var first_name = student.student_first_name;
    var father_name = student.student_father_name;
    var last_name = student.student_last_name;
    var mother_name = student.student_mother_fullname;
    var gender = student.student_sex;
    var bd_year = student.student_birthday_year;
    var bd_month = student.student_birthday_month;
    var bd_day = student.student_birthday_day;

    var ttl_char_student = first_name.length+father_name.length+last_name.length;
    var ttl_char_mother = mother_name.length;
    var gender_char = gender.charAt(0);
    var fullname_code = hashCode(first_name)+hashCode(father_name)+hashCode(last_name);
    var mother_name_code = hashCode(mother_name);

    var number = String(ttl_char_student)+String(ttl_char_mother)+String(fullname_code)+String(mother_name_code)+gender_char+bd_day+bd_month+bd_year;
    return number;
}

function scrollToBottom()
{
    $("html, body").animate({ scrollTop: $(document).height() }, 10);
}

function getHeader()
{
    var header = {
        'Authorization': 'Token '+user_token,
//        'HTTP_REFERER': $(location).attr('href'),
        'HTTP_REFERER': href_full_path,
        'Cookie': 'token=Token '+user_token,
        'X-CSRFToken': csrftoken
    };
    return header;
}

function getStoreByName(name)
{
    var store = db.transaction([name], "readwrite").objectStore(name);
    return store;
}

function synchronize_offline_data(store_name, url, callback)
{
    var store = getStoreByName(store_name);
    var request = store.getAll();
    request.onsuccess = function() {
        var result = request.result;
        $(result).each(function(i, item){
            if(item.synchronized == false && item.completed == true) {
                push_data_to_server_item(item, url, store_name);
            }
        });
        if(callback){
            callback();
        }
    };
}

function push_data_to_server_item(item, url, store_name)
{
    $.ajax({
        type: "POST",
        url: url,
        data: item,
        cache: false,
        async: false,
        headers: getHeader(),
        dataType: 'json',
        success: function (response, result, jqXHR) {
            if(jqXHR.status == 201 || jqXHR.status == 201){
                update_item_store(parseInt(item.id), 'synchronized', true, store_name);
            }
        },
        error: function (response) {
            var required_fields = JSON.parse(response.responseText);
            console.log(response);
        }
    });
}

function pull_data_from_server(url, store_name)
{
    $.ajax({
        type: "GET",
        url: url,
        cache: false,
        async: false,
        headers: getHeader(),
        dataType: 'json',
        success: function (response) {
            var store = getStoreByName(store_name);
            var data = response;
            if(response.data) {
                data = response.data;
            }
            $(data).each(function(i, item){
                store.put(item);
            });
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function delete_data_from_server(url, original_id, itemid, store_name)
{
    $.ajax({
        type: "DELETE",
        url: url+original_id+'/',
        cache: false,
        headers: getHeader(),
        dataType: 'json',
        success: function (response, result, jqXHR) {
            if(jqXHR.status = 200) {
                var store = getStoreByName(store_name);
                store.delete(parseInt(itemid));
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function update_data_server(url, item, itemid, callback_success, callback_error)
{
    $.ajax({
        type: "PUT",
        url: url+itemid+'/',
        data: item,
        cache: false,
        headers: getHeader(),
        dataType: 'json',
        success: function (response, result, jqXHR) {
            if(jqXHR.status == 200){
                if(callback_success){
                    callback_success();
                }
            }
        },
        error: function (response) {
            if(callback_error){
                callback_error();
            }
            console.log(response);
        }
    });
}

function submitForm(url, form, callback)
{
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        cache: false,
        headers: getHeader(),
        dataType: 'json',
        success: function (response, result, jqXHR) {
            if(jqXHR.status == 200){
                if(callback){
                    callback();
                }
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function initializeSly(block)
{
    var $frame = block;
    var $wrap = $frame.parent();

    var sly = new Sly(block,
        {
        horizontal: 1,
        itemNav: 'forceCentered',
        smart: 1,
        activateMiddle: 1,
        mouseDragging: 0,
        touchDragging: 0,
        releaseSwing: 1,
        startAt: 0,
        scrollBar: $wrap.find('.scrollbar'),
        scrollBy: 0,
        pagesBar: $wrap.find('.pages'),
        activatePageOn: 'click',
        speed: 300,
        elasticBounds: 1,
        easing: 'easeOutExpo',
        dragHandle: 1,
        dynamicHandle: 1,
        clickBar: 1,

        // Buttons
        prev: $wrap.find('.prev'),
        next: $wrap.find('.next')
    });

    sly.init();

    return sly;
}

function initializeSignature()
{
    var wrapper = document.getElementById("signature-pad"),
        clearButton = wrapper.querySelector("[data-action=clear]"),
        saveButton = wrapper.querySelector("[data-action=save]"),
        canvas = wrapper.querySelector("canvas"),
        signaturePad;

    signaturePad = new SignaturePad(canvas);

    clearButton.addEventListener("click", function (event) {
        signaturePad.clear();
        $('.m-signature-pad--footer').find('.btn-success').show();
        $('#alert-signature-error').hide();
    });

    saveButton.addEventListener("click", function (event) {
        $('#alert-signature-error').hide();
        if (signaturePad.isEmpty()) {
            $('#alert-signature-error').show();
        } else {
            $('#id_signature').val(signaturePad.toDataURL());
            $('#id_signature').trigger('blur');
            update_item_store(parseInt($('#main_id').val()), 'signature', signaturePad.toDataURL(), 'registrations');
            $('.m-signature-pad--footer').find('.btn-success').hide();
        }
    });

    //window.addEventListener("resize", resizeCanvas(canvas));
    //resizeCanvas(canvas);

    // Returns signature image as data URL (see https://mdn.io/todataurl for the list of possible paramters)
    signaturePad.toDataURL(); // save image as PNG
    signaturePad.toDataURL("image/jpeg"); // save image as JPEG

    // Draws signature image from data URL
    //signaturePad.fromDataURL("data:image/png;");

    // Clears the canvas
    signaturePad.clear();

    // Returns true if canvas is empty, otherwise returns false
    signaturePad.isEmpty();

    // Unbinds all event handlers
    signaturePad.off();

    // Rebinds all event handlers
    signaturePad.on();
}

function resizeCanvas(canvas) {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
    //alert(canvas.width);
    //alert(canvas.height);
    //alert(ratio);
    //signaturePad.clear(); // otherwise isEmpty() might return incorrect value
}

