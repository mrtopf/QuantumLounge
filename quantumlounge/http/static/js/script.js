/* Author: 

*/


var tm = TemplateManager();

function LoginView() {    

    function submit() {
        var data = $(this).serialize();
        var uri = new jsUri(document.location.href);
        var redirect_uri = uri.getQueryParamValue('redirect_uri');
        var state = uri.getQueryParamValue('state');

        // call the login view to log the user in
        // TODO: add error handler for network and login failed
        $.ajax({
            url: "/users/authorize/login",
            data: data,
            type: "POST",
            success: function (data, textResponse) {
                var status = data.status || 'error';
                if (status==='error') {
                    console.log("ERROR");
                    console.log(data);
                    return
                }
                // retrieve the code and redirect to the redirect uri
                var u = uri.clone();
                u.setPath("/users/authorize/authcode")
                  .replaceQueryParam('redirect_uri', redirect_uri);
                
                // login is correct, now lets retrieve the auth code
                // as we skip the grant screen.
                $.ajax({
                    url: u.toString(),
                    success: function(data, textResponse) {
                        if (!data.error) {
                            var u = new jsUri(redirect_uri)
                                .replaceQueryParam('code', data.code);                                
                            if (state) {
                                u.replaceQueryParam('state', state);
                            }
                            document.location.href=u.toString();
                        } else {
                            // TODO: What to do on error when trying to receive auth code?
                        }
                    }
                })
            }
        })
        return false;
    }

    // render the login form
    function render() {
        tm.render('login', function (d) {
            $("#content").html(d);
            $("#loginform").submit(submit);
        },{})
    }
    
    return {
        render: render
    }
}

function MainView() {    
    // render the login form
    function render() {
        tm.render('pm/main', function (d) {
            $("#content").html(d);
        },{})
    }
    
    return {
        render: render
    }

}

var views = {
    login: LoginView(),
    'pm/main' : MainView()
}

;(function($) {
  var app = $.sammy(function() {
      
    this.get('#/loginform', function() {
        LoginView().render();
    });
  });

  $(function() {
    app.run()
  });
})(jQuery);

