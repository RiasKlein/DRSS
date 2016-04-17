$(document).ready(function() {
    // toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'inline';
 	
    $('.donor_record').editable({
    	// if entry deleted, don't show on html page
        emptytext: '',
        // if error, pop-up with the message/prevent edit
		error: function(response) {
			alert(response.responseText);
		}
	});
});

