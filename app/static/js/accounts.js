$(document).ready(function(){
    $("#accountsTable #checkall").click(function () {
        if ($("#accountsTable #checkall").is(':checked')) {
            $("#accountsTable input[type=checkbox]").each(function () {
                $(this).prop("checked", true);
            });

        } else {
            $("#accountsTable input[type=checkbox]").each(function () {
                $(this).prop("checked", false);
            });
        }
    });

    //forms validator
    $('form').each(function () {
        $(this).validate({
            errorClass: "invalid",
            focusCleanup: true,
            rules: {
                inputAccountUserName: {
                    required: true,
                    email:true,
                    maxlength:30
                },
                inputAccountPassword:{
                    required:true
                    // regx:/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/
                }
            },
            messages:{
                inputAccountUserName: {
                    required:"Please enter account",
                    email: "Input is not in email format",
                    maxlength: "Input is too long"
                },
                inputAccountPassword:{
                    required: "Please enter password"
                    // regx: "Password format is wrong"
                }
            }

        });
    });

    $("[data-toggle=tooltip]").tooltip();
    var tableControl= document.getElementById('accountsTable');
    $('#btnEditAccount').click(function () {
        var updatedAccounts = {};
        if($('#editAccountForm').valid()) {

            var username = ($('#inputAccountUserName').val());
            var password = ($('#inputAccountPassword').val());
            $('input:checkbox:checked', tableControl).each(function() {
                var $tr = $(this).closest('tr');
                if($tr.children('td.app').text() != "") {
                    var app = $tr.children('td.app').text();
                    updatedAccounts[app] = {};
                    updatedAccounts[app]["username"] = username;
                    updatedAccounts[app]["password"] = password;
                }
            }).get();
            console.log(updatedAccounts)
            var mac = ($('.card_mac').text());
            $.ajax({
                url:'/updateAccounts',
                data:JSON.stringify({'accounts':updatedAccounts,
                    'mac':mac.split("Mac:")[1]}),
                dataType: 'json',
                contentType: 'application/json',
                type:'POST',
                success: function(response){
                    $('#editAccounts').modal('hide');
                    if(response.hasOwnProperty('error')){
                        console.log(response);
                    }else{
                        $("#accountsTable input[type=checkbox]").each(function () {
                            $(this).prop("checked", false);
                        });
                        location.reload();
                    }
                },
                error: function(error){
                    $('#editAccounts').modal('hide');
                    console.log(error);
                }
            });
        }

    });

    $('#btnCreateAccount').click(function () {
        if($('#createAccountForm').valid())
            var mac = ($('.card_mac').text());
        $.ajax({
            url:'/createAccount',
            data:JSON.stringify({'app':$('#createAccountAppName').val(),
                'username':$('#createAccountUserName').val(),
                'password':$('#createAccountPassword').val(),
                'mac':mac.split("Mac:")[1]}),
            dataType: 'json',
            contentType: 'application/json',
            type:'POST',
            success: function(response){
                $('#createAccount').modal('hide');
                if(response.hasOwnProperty('error')){
                    console.log(response);
                }else{
                    $("#accountsTable input[type=checkbox]").each(function () {
                        $(this).prop("checked", false);
                    });
                    location.reload();
                }
            },
            error: function(error){
                $('#createAccount').modal('hide');
                console.log(error);
            }
        });
    })

});