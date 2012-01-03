/*
  FIXME:
    We are using mostly . separated identifiers in rel= now.
    Migrate over to using just id= for attribute/field names, and then
    grab the servername via the parent id.
*/

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we
            // want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function add_attribute(thisObj, tableObj) {
    var dataArray = $(thisObj).closest('form').serializeArray();
    dataArray.push({'name': 'csrftoken', 'value': getCookie('csrftoken')});

    $.post( serverinfoRootURL + 'api/server/attribute/', dataArray, function(data) {
        tableObj.html(
            $(data.row).hide().fadeIn(300)
        );
    }, 'json');
    return false;
}

function add_ip(thisObj, tableObj) {
    var dataArray = $(thisObj).closest('form').serializeArray();
    dataArray.push({'name': 'csrftoken', 'value': getCookie('csrftoken')});

    $.post( serverinfoRootURL + 'api/server/ip/', dataArray, function(data) {
        tableObj.html(
            $(data.row).hide().fadeIn(300)
        );
    }, 'json');
    return false;
}


$.editable.addInputType('checkbox', {
    element : function(settings, original) {
        var input = $('<input type="checkbox">test</input>');
        $(this).append(input);
        return(input);
    }
});

$(document).ready(function() {
    $(".edit-text").editable( serverinfoRootURL + 'api/server/inlineForm/?_accept=text/raw', {
        submitdata: {csrftoken: getCookie('csrftoken')},
        tooltip: 'Click to edit...',
        placeholder: '** Click to set **',
        type: 'text',
        cancel: 'Cancel',
        submit: 'OK',
        style: 'display: inline',
	cssclass: 'autosize',
    });

    $(".edit-textarea").editable( serverinfoRootURL + 'api/server/inlineForm/?_accept=text/raw', {
        submitdata: {csrftoken: getCookie('csrftoken')},
        tooltip: 'Click to edit...',
        placeholder: '** Click to set **',
        type: 'textarea',
        cancel: 'Cancel',
        submit: 'OK',
        style: 'display: inline',
        rows: 3,
    });

    $(".edit-select").editable( serverinfoRootURL + 'api/server/inlineForm/?_accept=text/raw', {
        submitdata: {csrftoken: getCookie('csrftoken')},
        tooltip: 'Click to edit...',
        placeholder: '** Click to set **',
        type   : 'select',
        loadurl : serverinfoRootURL + 'api/server/inlineForm/',
        cancel: 'Cancel',
        submit: 'OK',
        style: 'display: inline',
    });

    // We dont use checkboxes yet.. But it is a custom type with a
    // true/false select box..
    $(".edit-checkbox").editable( serverinfoRootURL + 'api/server/inlineForm/?_accept=text/raw', {
        submitdata: {csrftoken: getCookie('csrftoken')},
        tooltip: 'Click to edit...',
        placeholder: '** Click to set **',
        type   : 'checkbox',
        loadurl : serverinfoRootURL + 'api/server/inlineForm/',
        cancel: 'Cancel',
        submit: 'OK',
        style: 'display: inline',
    });



    // Attribute form/button handeling
    $('.attr_remove').die().live('click', function() {
        // Kill previous live, to handle duplicate simulated clicks when more than one .attr_remove is visible
        var dataArray = new Array();
        dataArray.push({'name': 'csrftoken', 'value': getCookie('csrftoken')});
        dataArray.push({'name': 'id', 'value': $(this).attr('rel')});
        var table_obj = $(this).closest('.attr_table_wrapper');
        $.ajax({
            url: serverinfoRootURL + 'api/server/attribute/?remove',
            type: 'GET',
            dataType: 'json',
            data: dataArray,
            success: function(data) {
                table_obj.html(
                    $(data.row).hide().fadeIn(300)
                );
            }
        });
        return false;
    });
    $('.attr_add').unbind('click').click(function() {
        // Unbind click first, to handle duplicate clicks, same as we do with .attr_remove above
        var tableobj = $(this).parent().siblings('.attr_table_wrapper');
        add_attribute(this, tableobj);
        return false;
    });
    $('.form_attributes').unbind('keypress').bind('keypress', function(e){
        if ( e.which == 13 ) {
            var tableobj = $(this).siblings('.attr_table_wrapper');
            add_attribute(this, tableobj);
            return false;
        }
    });



    // IP form/button handeling
    $('.ip_remove').die().live('click', function() {
        var dataArray = new Array();
        var id_server = $(this).closest('.detaillist').attr('rel');
        var table_obj = $(this).closest('.ip_table_wrapper');

        dataArray.push({'name': 'csrftoken', 'value': getCookie('csrftoken')});
        dataArray.push({'name': 'id', 'value': $(this).attr('rel')});
        dataArray.push({'name': 'serverid', 'value': id_server});

        $.ajax({
            url: serverinfoRootURL + 'api/server/ip/?remove',
            type: 'GET',
            dataType: 'json',
            data: dataArray,
            success: function(data) {
                table_obj.html(
                    $(data.row).hide().fadeIn(300)
                );
            }
        });
        return false;
    });
    $('.ip_add').unbind('click').click(function() {
        var tableobj = $(this).parent().siblings('.ip_table_wrapper');
        add_ip(this, tableobj);
        return false;
    });
    $('.form_ip').unbind('keypress').bind('keypress', function(e){
        if ( e.which == 13 ) {
            var tableobj = $(this).siblings('.ip_table_wrapper');
            add_ip(this, tableobj);
            return false;
        }
    });
    $('.ip_check').unbind('click').click(function() {
        var dataArray = $(this).closest('form').serializeArray();
        var statusObj = $(this).siblings('.ip_check_status');

        $.ajax({
            url: serverinfoRootURL + 'api/server/ip/?check',
            type: 'GET',
            dataType: 'json',
            data: dataArray,
            success: function(data) {
                statusObj.html(data.status);
            }
        });

        return false;
    });

    $('.notetype').unbind('change').change(function() {
        var dataArray = new Array();
        var id_server = $(this).closest('.detaillist').attr('rel');
        var notetype = $(this).closest('.notetype').val();

        var statusObj = $(this).siblings('.note_status');
        var noteObj = $(this).siblings('.details_notefield');
        var note = noteObj.val();

        dataArray.push({'name': 'serverid', 'value': id_server});
        dataArray.push({'name': 'note', 'value': note});
        dataArray.push({'name': 'notetype', 'value': notetype});

        $.ajax({
            url: serverinfoRootURL + 'api/server/note/',
            type: 'GET',
            dataType: 'json',
            data: dataArray,
            success: function(data) {
                noteObj.val(data.note);
                $(statusObj).show()
                $(statusObj).html('Changed, ' + data.lastchange);
            }
        });
    });

    // Set default
    $('input:radio[name=notetype][value=public]').click();

    $('.note_save').unbind('click').click(function() {
        var dataArray = new Array();

        var statusObj = $(this).siblings('.note_status');
        var note = $(this).siblings('.details_notefield').val();
        var id_server = $(this).closest('.detaillist').attr('rel');
        var notetype = $(this).siblings('input[name=notetype]:checked').val();

        dataArray.push({'name': 'csrftoken', 'value': getCookie('csrftoken')});
        dataArray.push({'name': 'serverid', 'value': id_server});
        dataArray.push({'name': 'note', 'value': note});
        dataArray.push({'name': 'notetype', 'value': notetype});

        $.ajax({
            type:'POST',
    	    url: serverinfoRootURL + 'api/server/note/',
            data: dataArray,
    	    success: function(form_data)
    	    {
                $(statusObj).show()
                $(statusObj).html('Saved...');
                $(statusObj).fadeOut('slow');
                return 'saved';
    	    }
        });


    });

    $('.autosize').autoResize({
	maxHeight: 200,
	minHeight: 60,
	extraSpace: 16,
	animate: false,
    });


}); // End of $(document).ready(
