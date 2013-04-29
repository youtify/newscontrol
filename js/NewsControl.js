function NewsControl() {
	var self = this;

	self.init = function() {
		// Make sure we can log without breaking old browsers
		if (typeof(window.console) === 'undefined') {
			window.console = { 
				log: function() {}, 
				error: function(exception) { alert(exception); }
			};
		}
		
		// Handle unsuccessful requests
		$(document).ajaxError(function (e, r, ajaxOptions, thrownError) {
    		switch (r.status) {
    			case 403:
    				self.showLoginModal();
    				break;
				case 500:
					self.showError(r.responseText);
					break;
	    	}
		});
	};

}
