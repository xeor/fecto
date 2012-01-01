var oTable;

function dump(arr, level) {
    var dumped_text = "";
    if(!level) level = 2;

    //The padding given at the beginning of the line.
    var level_padding = "";
    for(var j=0;j<level+1;j++) level_padding += "    ";

    if(typeof(arr) == 'object') { //Array/Hashes/Objects
	for(var item in arr) {
	    var value = arr[item];

	    if(typeof(value) == 'object') { //If it is an array,
		dumped_text += level_padding + "'" + item + "' ...\n";
		dumped_text += dump(value,level+1);
	    } else {
		dumped_text += level_padding + "'" + item + "' => \"" + value + "\"\n";
	    }
	}
    } else { //Stings/Chars/Numbers etc.
	dumped_text = "===>"+arr+"<===("+typeof(arr)+")";
    }
    return dumped_text;
}

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

// From http://stackoverflow.com/questions/439463/how-to-get-get-and-post-variables-with-jquery
function getQueryParams(qs) {
    qs = qs.split("+").join(" ");
    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;
    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])]
            = decodeURIComponent(tokens[2]);
    }

    return params;
}


/* Formating function for row details */
function fnFormatDetails(nTr, thisObj) {
    var aData = oTable.fnGetData( nTr );
    var id_server = $(thisObj).attr('rel');

    $.ajax({
        type: 'GET',
    	url: serverinfoRootURL + 'details/' + id_server,
    	cache: false,
    	success: function(msg)
    	{
    	    oTable.fnOpen( nTr, msg, 'serv_details' );
    	}
    });
}

/* Event handler function */
function fnOpenClose(oSettings) {
    $('td img', oTable.fnGetNodes() ).each( function () {
	$(this).click( function () {
	    var nTr = this.parentNode.parentNode;
	    if ( this.src.match('details_close') ) {
		/* This row is already open - close it */
		this.src = '/static/serverinfo/img/details_open.png';
		oTable.fnClose( nTr );

                // If we do an fnDraw() here, it will refresh the
                // table the correct way, but it will also close every
                // open details. FIXME, check if any details is open,
                // if there is, dont run fnDraw...
                //oTable.fnDraw(false);
	    } else {
		/* Open this row */
		this.src = '/static/serverinfo/img/details_close.png';
		oTable.fnOpen( nTr, fnFormatDetails(nTr,this), 'serv_details' );
	    }
	});
    });
}

function fnShowHide(iColName) {
    /* Get the DataTables object again - this is not a recreation, just a get of the object */
    var oTable = $('#serverlist').dataTable();
    var iCol = iColIDMap[iColName];
    var bVis = oTable.fnSettings().aoColumns[iCol].bVisible;

    // We haveto do this every time, even at the beginning when we hide many at once..
    oTable.fnSetColumnVis( iCol, bVis ? false : true );
    oTable.fnAdjustColumnSizing();
    oTable.fnDraw();
}

function fnResetAllFilters() {
    var oSettings = oTable.fnSettings();
    for (iCol = 0; iCol < oSettings.aoPreSearchCols.length; iCol++) {
	oSettings.aoPreSearchCols[ iCol ].sSearch = '';
    }
    $('.dataTables_filter input').val('').keyup();

    $('tfoot input').each( function (i) {
	this.value = '';
    });

    // FIXME, should also delete oTable cookie
    oTable.fnSortNeutral();
    oTable.fnDraw();
}

function fnCreateSelect(aData) {
    var r = '<select><option value=""></option>', i, iLen = aData.length;
    for (i = 0; i<iLen; i++) {
	r += '<option value="'+aData[i]+'">'+aData[i]+'</option>';
    }
    return r + '</select>';
}


// In case the input form is of type "location", we should get form details..
// 'get_ip_' + type...
function get_ip_location(thisObj) {
    var id_server = $(thisObj).closest('.detaillist').attr('rel');
    if (id_server == undefined) {
        // We are using the function outside the normal server details
        // frame. Example for use in the subnet filter, custom filter.
        // The serverid of 000 will never happend, but is used here
        // because we need to know which id to replace below.
        // Therefor, always use #net_form_helpers-standalone when using this
        // in "standalone" modus
        id_server = 'standalone';
    }
    var dataArray = $(thisObj).closest('form').serializeArray();

    $.ajax({
        type:"GET",
    	url: serverinfoRootURL + 'api/getIpHelperForms/?_accept=text/raw',
    	cache: false,
        data: dataArray,
    	success: function(form_data)
    	{
            $('#net_form_helpers-' + id_server).html(form_data);
            return true;
    	}
    });
}

// In case the type is "vlan", we are ready to get and populate the
// next IP address.. 'get_ip_' + type...
function get_ip_vlan(thisObj) {
    var id_server = $(thisObj).closest('.detaillist').attr('rel');
    var dataArray = $(thisObj).closest('form').serializeArray();

    $.ajax({
        type:"GET",
    	url: serverinfoRootURL + 'api/getIpHelperNext/?_accept=text/raw',
    	cache: false,
        data: dataArray,
    	success: function(form_data)
    	{
            // input.ip on the same level as #net_form_....
            $('#net_form_helpers-' + id_server + ' ~ input.ip').val(form_data);
            return true;
    	}
    });
}


$(document).ready(function() {

    // Start of table stuff
    oTable = $('#serverlist').dataTable( {
	'aLengthMenu': [[10, 25, 50, -1], [10, 25, 50, 'All (dont use if not needed)']],
	'bProcessing': true,
	'bServerSide': true,
	'bAutoWidth': false, // If we dont do this, it will look ugly when toggling columns hide/show
	'bStateSave': true,
	'sPaginationType': 'full_numbers',
	'sAjaxSource': serverinfoRootURL + 'api/server/datatables/',
	'fnServerData': function(sSource, aoData, fnCallback ) {

            $('.filter_value').each(function(index) {
		aoData.push({'name': this.id, 'value': $(this).val()});
            });

	    for (var i = 0, len = columns.length; i<len; ++i) {
		val = $('#columnfilter_' + columns[i]).val();
		if (typeof val === 'undefined') {
		    val = '';
		}
		aoData.push( { "name": "columnfilter_" + columns[i], "value": val } );
	    }

            if ($('span.newserver').length) {
		aoData.push({'name': 'newserver', 'value': $('span.newserver').attr('id')});
            }

            var extraGETs = getQueryParams(document.location.search);
            if (extraGETs) {
                for(var gets in extraGETs) {
                    aoData.push({'name': 'extra_' + gets, 'value': extraGETs[gets]});
                }
            }

            var columnsVisibleFilterableArr = []
	    $('.search_init').each(function() {
		columnsVisibleFilterableArr.push($(this).attr('id'));
	    });

            var columnsVisibleFilterable = columnsVisibleFilterableArr.join('.');
	    aoData.push({'name': 'columnsVisibleFilterable', 'value': columnsVisibleFilterable});

	    $.ajax({
		dataType: 'json',
		type: 'GET',
		url: sSource,
		data: aoData,
		success: function(json) {
                    $('#admLink_frozenlist').attr('href', serverinfoRootURL + '?freezeByID=' + json['serversCSV']);
                    fnCallback(json)
                },
		error: function() {
		    // FIXME, this should be a notifier instead
		    alert("Error grabbing data from server..");
		}
	    });
	},
	'sDom': 'T<"clear">lfrtip',
        'oTableTools': {
            'sSwfPath': '/static/serverinfo/lib/DataTables-1.8.1/media/swf/copy_cvs_xls.swf'
        },
	'oLanguage': {
	    'sSearch': 'Search all visible columns:'
	},
	'aoColumns': aoColumns,
	'aaSorting': [[1, 'asc']],
	'fnDrawCallback': fnOpenClose,
    }); // End of oTable = ...

    $('#serverlist_filter input').select()

    $('#serverlist_filter').append('&nbsp;&nbsp;<a href="#" id="reset">Reset</a>');
    $('#reset').click(function(event) {
	fnResetAllFilters();
    });

    // Footer stuff
    $('tfoot input').keyup( function () {
	/* Filter on the column (the index) of this element */
	oTable.fnFilter( this.value, $("tfoot input").index(this) );
    });
    $('tfoot select').change( function () {
	oTable.fnFilter( this.value, $("tfoot select").index(this) );
    });

    // New server button
    $('#admLink_newserv').click(function() {
        var dataArray = new Array();
        dataArray.push({'name': 'custominfo', 'value': ''}); // placeholder
        dataArray.push({'name': 'csrftoken', 'value': getCookie('csrftoken')});

        $.ajax({
            type: 'POST',
            async: false,
            url: serverinfoRootURL + 'api/server/new/',
            data: dataArray,
            success: function(serverName){
                // This span (.newserver) id is important, dont delete it..
                $('#messagebox').html('Created new server <span class="newserver" id="' + serverName + '">' + serverName + '.</span> <a href="#" class="button newserverrefresh">Refresh view</a>');
                $('#messagebox').addClass('info');
                $('#messagebox').show();
                oTable.fnDraw();

                // fnDraw wont let us run this right after itself
                // is runned. It will be called automaticly later
                // in the code and makes our click action just
                // flash. If we dont call fnDraw, our new server
                // wont show up at all. Little catch22 which ends
                // up in that we haveto delay our click, and live
                // with doublecall to fnDraw within a very short timeperiod
                setTimeout("$('td img:first').click(); $('td img:first').hide()", 500);
            },
        });
    });

    // Newserver save and refresh button
    $('.newserverrefresh').live('click', function() {
        location.reload(true);
        return false;
    });

    // Filter options
    $('.filterJail').each( function () {
        $(this).hide()
    });

    $('.filterToggle').toggle(function() {
	$(this).css({'font-weight': 'bold'});
	$('#jail_' + this.id).show();
    }, function() {
	$(this).css({'font-weight': ''});
	$('#jail_' + this.id).hide();
	$('#' + this.id + '_value').val('');
	oTable.fnDraw();
    });


    // Row selector
    $('.rowSelect').click(function() {
	if ( $(this).css('font-weight') == 'bold' ) {
	    $(this).css({'font-weight': ''});
	} else {
	    $(this).css({'font-weight': 'bold'});
	}
	fnShowHide(this.id);
    });

    $('.administerLinks').toggle(function() {
	$(this).css({'font-weight': 'bold'});
	$('#table_' + this.id).show();
    }, function() {
	$(this).css({'font-weight': ''});
	$('#table_' + this.id).hide();
    });

    $('#special_filter_apply').click(function(){
	oTable.fnDraw();
    })

    $('#special_filter').keyup(function(e) {
	if(e.keyCode == 13) {
	    oTable.fnDraw();
	}
    });

}); // End of $(document).ready(
