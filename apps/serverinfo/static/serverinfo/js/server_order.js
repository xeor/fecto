//jQuery.noConflict();

$(document).ready(function() {

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
<select name="ipsubnet_loc" id="ipsubnet_loc">\
<option value="">** Select location **</option>' + options + '\
</select>\
<select name="ipsubnet" id="id_ipsubnet">\
<option value="0"></option>\
</select>\
';
    
    $("#subnetOpts").html(htmlFormSubnet);

    $("select#ipsubnet_loc").bind('change keyup keydown', function(){
	$("select#id_ipsubnet").html('');
	$.getJSON("/admin/json/subnet/",{id: $(this).val(), type: 'subnet'}, function(j){
	    var options = '';
	    options += '<option value=""></option>';
	    for (var i = 0; i < j.length; i++) {
		options += '<option value="' + j[i].optionVlanID + '">' + j[i].optionName + ' - ' + j[i].optionNetwork + '</option>';
	    }
	    $("select#id_ipsubnet").html(options);
	})
    })
});