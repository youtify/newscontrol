function User() {
    var self = this;
    
    self.id = null;
    self.nickname = null;
    self.email = null;
    
    self.init = function() {
    };
    
    $.getJSON('/me').success(function(data) {
        console.log('user loaded', data);
        self.id = data.id;
        self.nickname = data.nickname;
        self.email = data.email;
        $('.dropdown.user .username').text(self.email);
        $('.dropdown.user').show();
        
        console.log('calling me_loaded listeners');
        $(document).trigger('me_loaded');
    });
}