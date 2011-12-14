
(function($) {
    function getNextIPfor(vlan_id, obj_id) {
	$.getJSON("/serverinfo/json/nextip/", {vlan_id: vlan_id},
		  function(ret, textStatus) {
		      alert(obj);
		      alert(ret.ip);
		      $("id_ip_set-" + obj_id + "-ip").val(ret.ip);
		      return ret.ip;
		  }
	);
    }

    $(document).ready(function() {
	    $(".vlan").each(function(index) {
		    $("select#id_ip_set-" + index + "-vlan").bind('change keyup keydown', function(){
			    var ip = $(this).val();
			    //var ip = getNextIPfor($(this.val));
			    getNextIPfor($(this.val), index);
			    var txtIndex = index;
			    $("#id_ip_set-" + txtIndex + "-ip").val(ip);
			})
	    });

	    $("#id_county").change(function() { fill_municipalities($(this).val()); });

	});
})(django.jQuery);
