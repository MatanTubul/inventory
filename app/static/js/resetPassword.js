/**
 * Created by matant on 31/10/17.
 */
/**
 * Created by matant on 31/10/17.
 */
$(document).ready(function(){
    //forms validator
    $('form').each(function () {
        $(this).validate({
            errorClass: "invalid",
            focusCleanup: true,
            onfocusout: false,
            onkeyup: false,
            onclick: false,
            rules: {
                password: {
                    required: true,
                    maxlength:30
                },
                confirmPassword:{
                    required:true,
                    equalTo: "#password"
                }
            },
            messages:{
                password: {
                    required:"Please enter password",
                    maxlength: "Input is too long"
                },
                confirmPassword:{
                    required: "Confirm Password is required",
                    equalTo: "Password do not match"
                }
            },
            errorPlacement: function (error, element) {
                alert(error.text());
            }

        });
    });

    $('#updatePasswordBtn').click(function () {
        if ($('#reset-password-form').valid()){
            $.ajax({
                url: '/updatePassword',
                data: {'password':$('#password').val(),'token':$('#token').val()},
                type: 'POST',
                success: function (response) {
                    if(response.hasOwnProperty('error')){
                        $('#modalOnResponseHeader').css('background', '#E2747E');
                        $('#modalResponseTitle').text("Failed");
                        $('#modalResponseBody').text(response.error);
                    }else{
                        $('#modalOnResponseHeader').css('background', '#3FC59D');
                        $('#modalResponseTitle').text(response.title);
                        $('#modalResponseBody').text(response.message);
                    }
                    $('#modalResponse').modal('show');
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    });
    $('#confirmPassword').focus(function () {
        $('#confirmPassword').val('');
    });
    $('#password').focus(function () {
        $('#password').val('');
    });

    $('#btnCloseResponseModal').click(function(){
        console.log("rediredt");
        window.location.replace("/");
    });
});