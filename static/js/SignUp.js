
$(function() {    
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                var x = document.getElementById("success");
                x.style.display = "block";
                document.getElementById('success-msg').innerHTML = response;
                $.ajax({
                    url: '/showSignIn'
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});