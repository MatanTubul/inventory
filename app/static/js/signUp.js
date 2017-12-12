
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
            $('#modalCreateUserBody').modal('hide');
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
    // On closing response modal
    $('#btnCloseResponseModal').click(function(){
        window.location.reload();
    });

    //Handling edit user action
    $('body').on('click', '.btn-default-clicked', function () {
        var $tr = $(this).closest('tr');
        $('#userRole').val($tr.children('td.role').text());
        $('#editUser').data('username',$tr.children('td.userName').text())
        $('#editUser').data('role',$tr.children('td.role').text())
        $('#editUser').modal('show');
    });

    $('#btnEditUser').click(function () {
        $.ajax({
            url: '/updateUser',
            data: {
                'username':$('#editUser').data('username'),
                'role':$('#userRole').val()
            },
            type: 'POST',
            success: function (response) {
                if(response.hasOwnProperty('error')){
                    $('#modalOnResponseHeader').css('background', '#E2747E');
                    $('#modalResponseTitle').text("Failed");
                    $('#modalResponseBody').text(response.error);
                    $('#modalResponse').modal('show');
                }else{
                    window.location.reload();
                }

            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    //Handling delete user action
    $('body').on('click','.btn-danger-clicked', function () {
        var $tr = $(this).closest('tr');
        $('#approveUserDelete').data('username', $tr.find(".userName").text());
        $('#approveUserDelete').data('rowid', $tr.index()+1);
        $('#approveUserDelete').modal('show');
    });

    //Delete selected device row
    $('#btnDelteYes').click(function () {
        var mac = $('#approveUserDelete').data('mac');
        var rowIndex = $('#approveUserDelete').data('rowid');
        console.log(rowIndex);
        $('#approveUserDelete').modal('hide');
        $.ajax({
            url: '/deleteUser',
            data: {
                'username':$('#approveUserDelete').data('username')
            },
            type: 'POST',
            success: function(response){
                if(response.hasOwnProperty('error')) {
                    $('#modalOnResponseHeader').css('background', '#E2747E');
                    $('#modalResponseTitle').text("Failed");
                    $('#modalResponseBody').text(response.error);
                }else{
                    window.location.reload();
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});