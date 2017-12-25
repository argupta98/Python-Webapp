$(function() {    
    $('#btnAddWish').click(function() {
        $.ajax({
            url: '/addWish',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});