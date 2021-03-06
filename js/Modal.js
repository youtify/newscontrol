var Modal = {
    
    init: function(newsControl) {
        // Invite
        $('#inviteModal .btn-primary').click(function(event) {
            var email = $('#inviteModal input[name=email]').val();
            
            if (!email || email.indexOf('@') === -1 || email.indexOf('.') === -1) {
                alert('An valid email must be provided')
                event.preventDefault();
                
                // TODO: don't close modal
                
                return;
            }
            
            var params = {
                email: email
            };
            
            newsControl.loadingBar.setPercent(10);
            console.log('inviting', email);
            
            $.post('/invite', params).success(function(data) {
                console.log('user invited', data);
            }).complete(function() {
                newsControl.loadingBar.setPercent(100);
            });
        });

        // Nickname
        $('#nicknameModal a.tag-link').click(function() {
            newsControl.topBar.changeTab('tags');
        });
        $('#nicknameModal .save').click(function() {
            newsControl.user.changeNickname($('#nicknameModal input.nickname').val());
        });
    },
    
	showInvite: function() {
        $('#inviteModal').modal({
            backdrop: 'static',
            keyboard: true,
            show: true
        });
    },
    
	showLogin: function() {
        $('#loginModal').modal({
            backdrop: 'static',
            keyboard: false,
            show: true
        });
    },

    showError: function(message) {
        $('#errorModal .message').html(message);
        $('#errorModal').modal({
            backdrop: 'static',
            keyboard: true,
            show: true
        });
    },

    showInformation: function(message) {
        $('#infoModal .message').html(message);
        $('#infoModal').modal({
            backdrop: 'static',
            keyboard: true,
            show: true
        });
    },

    showUnauthorized: function(message) {
        $('#unauthorizedModal').modal({
            backdrop: 'static',
            keyboard: false,
            show: true
        });
    },

    showNickname: function() {
        $('#nicknameModal input.nickname').val(newsControl.user.nickname);
        $('#nicknameModal').modal({
            backdrop: 'static',
            keyboard: true,
            show: true
        });
    }, 
};