$(document).ready(function() {
    $.validator.addMethod("regx", function(value, element, regexpr) {
        return regexpr.test(value);
    }, "Please enter a valid input.");

    //forms validator
    $('form').each(function () {
        $(this).validate({
            errorClass: "invalid",
            focusCleanup: true,
            rules: {
                inputEmail: {
                    required:true
                },
                inputPassword:{
                    required:true
                    // regx:/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/
                }
            },
            messages:{
                inputEmail:{
                    required: "Email is missing"
                },
                inputPassword:{
                    required: "Password is missing"
                    // regx: "Password format is wrong"
                }
            }
        });
    });

    $('#btnSignIn').click(function () {
        console.log(1);
        if ($('#formLogin').valid()){
            $.ajax({
                url: '/validateLogin',
                data: $('form').serialize(),
                type: 'POST',
                success: function (response) {
                    var res = JSON.parse(response);
                    console.log(res);
                    if(res.hasOwnProperty('error')) {
                        console.log(2);
                        $('#modalOnResponseHeader').css('background', '#E2747E');
                        $('#modalResponseTitle').text("Failed");
                        $('#modalResponseBody').text("Failed to login, "+res.error);
                        $('#modalResponse').modal('show');
                    } else{
                        console.log(res.url);
                        // window.location.replace(res.url);
                        window.location.href = res.url;
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    });

    $('#btnCloseResponseModal').click(function(){
        console.log(4);
        $("#formLogin").validate().resetForm();
        $("#formLogin")[0].reset();
    });

});