
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
                inputName:{
                    required:true,
                    maxlength:30,
                    regx:/^([A-Za-z]+?)\s([A-Za-z]+?)$/
                },
                inputEmail: {
                    required: true,
                    email:true,
                    maxlength:30
                },
                inputPassword:{
                    required:true
                    // regx:/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/
                },
                inputUserRule:{
                    required:true
                }
            },
            messages:{
                inputName: {
                    required:"Please enter name",
                    maxlength: "Input is too long",
                    regx: "Input is in wrong format"
                },
                inputEmail: {
                    required:"Please enter account",
                    email: "Input is not in email format",
                    maxlength: "Input is too long"
                },
                inputPassword:{
                    required: "Please enter password"
                    // regx: "Password format is wrong"
                },
                inputUserRule: "User role is not selected!!!"
            }

        });
    });

    $('#btnSignUp').click(function () {

        if ($('#createUserForm').valid()){
            $.ajax({
                url: '/signUp',
                data: $('form').serialize(),
                type: 'POST',
                success: function (response) {
                	var res = JSON.parse(response);
                	if(res.hasOwnProperty('error')){
                        $('#modalOnResponseHeader').css('background', '#E2747E');
                        $('#modalResponseTitle').text("Failed");
                        $('#modalResponseBody').text("Failed to create user with error, "+res.error);
					}else{
                        $('#modalResponseTitle').text("User created");
                        $('#modalResponseBody').text("User created successfully");
					}
                    $('#modalResponse').modal('show');
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    });
    $('#btnCloseResponseModal').click(function(){
        $("#createUserForm").validate().resetForm();
        $("#createUserForm")[0].reset();
    });

});