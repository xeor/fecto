var oTable;

/* Formating function for row details */
function fnFormatDetails ( nTr )
{
    var aData = oTable.fnGetData( nTr );
    var id_server=aData[1]; // table -> first column value
    $.ajax({
	    type:"GET",
		url: '/serverinfo/details-min/' + id_server,
		cache: false,
		//data:'...' + id_server, # We are doing this above. To keep it cleaner in urls.py
		success: function(msg)
		{
		    oTable.fnOpen( nTr, msg, 'serv_details' );
		}
	});
    return '';
}

/* Event handler function */
function fnOpenClose ( oSettings )
{
    $('td img', oTable.fnGetNodes() ).each( function () {
	    $(this).click( function () {
		    var nTr = this.parentNode.parentNode;
		    if ( this.src.match('details_close') )
			{
			    /* This row is already open - close it */
			    this.src = "/media/img/details_open.png";
			    var nRemove = $(nTr).next()[0];
			    nRemove.parentNode.removeChild( nRemove );
			    // oTable.fnClose( nTr );
			}
		    else
			{
			    /* Open this row */
			    this.src = "/media/img/details_close.png";
			    oTable.fnOpen( nTr, fnFormatDetails(nTr), 'serv_details' );
			}
		} );
	} );
}

function fnShowHide( iColName )
{
    /* Get the DataTables object again - this is not a recreation, just a get of the object */
    var oTable = $('#serverlist').dataTable();

    var iCol = iColIDMap[iColName];

    var bVis = oTable.fnSettings().aoColumns[iCol].bVisible;

    // Its annoying, but looks like we haveto do this every time, even at the beginning when we hide
    // many at once..
    oTable.fnSetColumnVis( iCol, bVis ? false : true );
    oTable.fnAdjustColumnSizing();
    oTable.fnDraw();
}

function fnResetAllFilters() {
    var oSettings = oTable.fnSettings();
    for(iCol = 0; iCol < oSettings.aoPreSearchCols.length; iCol++) {
	oSettings.aoPreSearchCols[ iCol ].sSearch = '';
    }
    $('.dataTables_filter input').val('').keyup();
    $('#ipLoc').val('').keyup();

    $("tfoot input").each( function (i) {
	    //this.className = "search_init";
	    this.value = '';
	    //this.value = asInitVals[$("tfoot input").index(this)];
	} );


    oTable.fnSortNeutral();
    oTable.fnDraw();

    //console.log(oSettings);
}

function fnCreateSelect( aData )
{
    var r='<select><option value=""></option>', i, iLen=aData.length;
    for ( i=0 ; i<iLen ; i++ )
	{
	    r += '<option value="'+aData[i]+'">'+aData[i]+'</option>';
	}
    return r+'</select>';
}


$(document).ready(function() {
	//TableToolsInit.sSwfPath = "/media/lib/dataTables-1.7/extras/TableTools/media/swf/ZeroClipboard.swf";

	oTable = $('#serverlist').dataTable( {
		"aLengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All (dont use if not needed)"]],
		"bProcessing": true,
		"bServerSide": true,
		"bAutoWidth": false, // If we dont do this, it will look ugly when toggling columns hide/show
		"bStateSave": true,
		"sPaginationType": "full_numbers",
		"sAjaxSource": "/serverinfo/json/",
		"fnServerData": function (sSource, aoData, fnCallback ) {
		    aoData.push( { "name": "vlanID", "value": $("select#subnet").val() } );
		    aoData.push( { "name": "lastPingDays", "value": $("select#lastAlive").val() } );
		    aoData.push( { "name": "lastPingDaysWay", "value": $("select#lastAliveWay").val() } );
		    aoData.push( { "name": "lastMonitorDays", "value": $("select#lastMonitor").val() } );
		    aoData.push( { "name": "lastMonitorDaysWay", "value": $("select#lastMonitorWay").val() } );
		    aoData.push( { "name": "lastWinUpd", "value": $("select#lastWinUpd").val() } );
		    aoData.push( { "name": "lastWinUpdWay", "value": $("select#lastWinUpdWay").val() } );
		    aoData.push( { "name": "vlanLoc", "value": $("select#ipLoc").val() } );
		    aoData.push( { "name": "virtual", "value": $("input#virtual").val() } );
		    aoData.push( { "name": "ous_shared", "value": $("input#ous_shared").val() } );
		    aoData.push( { "name": "filter_name", "value": $("input#filter_name").val() } ); // Stupid standard filter function is buggy!!
		    aoData.push( { "name": "filter_domain", "value": $("input#filter_domain").val() } ); // Using this method instead..
		    aoData.push( { "name": "filter_function", "value": $("input#filter_function").val() } ); // sSearch_X or something is set anyway, but
		    aoData.push( { "name": "filter_description", "value": $("input#filter_description").val() } ); // a refresh wont zero it out correctly
		    aoData.push( { "name": "filter_IP", "value": $("input#filter_IP").val() } );
		    aoData.push( { "name": "filter_OS", "value": $("input#filter_OS").val() } );
		    aoData.push( { "name": "filter_system", "value": $("input#filter_system").val() } );
		    aoData.push( { "name": "filter_VMcomment", "value": $("input#filter_VMcomment").val() } );
		    aoData.push( { "name": "special_filter", "value": $("input#special_filter").val() } );

		    $.ajax( {
			    "dataType": 'json',
				"type": "GET",
				"url": sSource,
				"data": aoData,
				"success": fnCallback,
				error: function() {
				  alert("Error grabbing data from server..");
			        }
				});
		},
		"sDom": 'T<"clear">lfrtip',
		"oLanguage": {
		    "sSearch": "Search all visible columns:"
		},
		"aoColumns": [

        // DONT use % to do sizing, it will screw up the autosizing when showing/hiding columns
	{ "sClass": "center", "sWidth": "1px", "bSortable": false }, // + / - image.
	{ "sWidth": "15em" }, // name
	null, // domain
	{ "bSortable": false }, // IP
	null, // OS
	null, // System
	null, // function
	null, // vmComment
	null, // description
	null  // Actions
			      ],
		"aaSorting": [[1, 'asc']],
		"fnDrawCallback": fnOpenClose
	    } );

	$("#serverlist_filter input").select()

	$("#serverlist_filter").append('&nbsp;&nbsp;<a href="#" id="reset">Reset</a>');
	$("#reset").click(function(event) {
		fnResetAllFilters();
	    });


   // Footer stuff
	$("tfoot input").keyup( function () {
		/* Filter on the column (the index) of this element */
		oTable.fnFilter( this.value, $("tfoot input").index(this) );
	    } );

	/* We are getting weird results when using this. Last values jumps around and such.. FIXME sometime :)
	$("tfoot input").each( function (i) {
		if ( this.value == "" ) {
		    this.value = asInitVals[i];
		}
	    } );
	
	$("tfoot input").focus( function () {
		if ( this.className == "search_init" )
		    {
			this.className = "";
			this.value = "";
		    }
	    } );
	
	$("tfoot input").blur( function (i) {
		if ( this.value == "" )
		    {
			this.className = "search_init";
			this.value = asInitVals[$("tfoot input").index(this)];
			//oTable.fnDraw();
		    }
	    } );
	*/


   // Filter options
    $('.filterOption').each( function () {
	    $('#row_' + this.id).hide()
    });

   $('.filterOption').toggle(function() {
	   $(this).css({"font-weight": "bold"});
	   $('#row_' + this.id).show();
   }, function() {
	   $(this).css({"font-weight": ""});
	   $('#row_' + this.id).hide();
   });

   // Row selector
   $('.rowSelect').click(function() {
	   if ( $(this).css("font-weight") == "bold" ) {
	       $(this).css({"font-weight": ""});
	   } else {
	       $(this).css({"font-weight": "bold"});
	   }
	   fnShowHide(this.id);
   });

   // Dont bother showing this as standard
   $("#rowDomain").click();
   $("#rowOS").click();
   $("#rowSystem").click();
   $("#rowDescription").click();
   $("#rowActions").click();


   // Below here is subnet code
   var options = '';

   $.ajax({
      async: false,
      dataType: "json",
      url: "/admin/json/subnet/?type=location",
        success: function(j){
         for (var i = 0; i < j.length; i++) {
            options += '<option value="' + j[i].optionValue + '">' + j[i].optionDisplay + '</option>';
          }
        }
   });

    var htmlFormSubnet = '\
<form action="">\
  <select name="id" id="ipLoc">\
    <option value="">** Select location **</option>' + options + '\
  </select>\
  <select name="sub_id" id="subnet">\
    <option value="0"></option>\
  </select>\
</form>\
';

   $("#subnetOpts").html(htmlFormSubnet);

   $("select#ipLoc").bind('change keyup keydown', function(){
     $("select#subnet").html('');
     $.getJSON("/admin/json/subnet/",{id: $(this).val(), type: 'subnet'}, function(j){
       var options = '';
       options += '<option value=""></option>';
       for (var i = 0; i < j.length; i++) {
         options += '<option value="' + j[i].optionVlanID + '">' + j[i].optionName + ' - ' + j[i].optionNetwork + '</option>';
       }
       $("select#subnet").html(options);
     })
     oTable.fnDraw();
   })


   $("select#subnet").bind('change keyup keydown', function(){
     oTable.fnDraw();
   })

   $("select#lastAlive").bind('change keyup keydown', function(){
     oTable.fnDraw();
   })
   $("select#lastAliveWay").bind('change keyup keydown', function(){
     oTable.fnDraw();
   })

   $("select#lastMonitor").bind('change keyup keydown', function(){
     oTable.fnDraw();
   })
   $("select#lastMonitorWay").bind('change keyup keydown', function(){
     oTable.fnDraw();
   })

   $("select#lastWinUpd").bind('change keyup keydown', function(){
     oTable.fnDraw();
   })
   $("select#lastWinUpdWay").bind('change keyup keydown', function(){
     oTable.fnDraw();
   })

   $("#special_filter_apply").click(function(){
	   oTable.fnDraw();
   })
   $('#special_filter').keyup(function(e) {
	   if(e.keyCode == 13) {
	       oTable.fnDraw();
	   }
       });




});