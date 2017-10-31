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
                inputEmail: {
                    required: true,
                    email:true,
                    maxlength:30
                }
            },
            messages:{
                inputEmail: {
                    required:"Please enter account",
                    email: "Input is not in email format",
                    maxlength: "Input is too long"
                }
            },
            errorPlacement: function (error, element) {
                $(element).val(error.text());
            }

        });
    });

    $('#resetPasswordBtn').click(function () {
        if ($('#register-form').valid()){
            console.log($('#email').val());
            $.ajax({
                url: '/resetPassword',
                data: $('form').serialize(),
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
    $('#email').focus(function () {
        $('#email').val('');
    });

    $('#btnCloseResponseModal').click(function(){
        $("#createUserForm").validate().resetForm();
        $("#createUserForm")[0].reset();
    });
});