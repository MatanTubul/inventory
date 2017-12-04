$(document).ready(function(){
    loadUsers();
    $.validator.addMethod("regx", function(value, element, regexpr) {
        return regexpr.test(value);
    }, "Please enter a valid Mac Address.");

    //forms validator
    $('form').each(function () {
        $(this).validate({
            errorClass: "invalid",
            focusCleanup: true,
            rules: {
                inputDeviceName:{
                    maxlength:30
                },
                inputAccount: {
                    required: true,
                    email:true,
                    maxlength:30
                },
                inputMacAddress: { required:true,
                    regx: /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/,
                    maxlength:30
                },
                inputPhoneNumber: {
                    required:false,
                    regx:/\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})/,
                    maxlength:14

                }

            },
            messages:{
                inputDeviceName: {
                    maxlength: "Input is too long"
                },
                inputAccount: {
                    required:"Please enter account",
                    email: "Input is not in email format",
                    maxlength: "Input is too long"
                },
                inputMacAddress: {
                    required: "Please enter device Mac Address",
                    regx: "Wrong format"

                },
                inputPhoneNumber:{
                    regx: "Wrong format phone number",
                    maxlength: "Input is too long"
                }
            }

        });
    });
    //handle create device request
    $('#btnCreateDevice').click(function(){
        if ($('#createDeviceForm').valid()){
            $.ajax({
                url: '/createDevice',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response){
                    $('#createDevice').hide();
                    if(response.hasOwnProperty('error')){

                        $('#modalResponseTitle').text("Failed");
                        $('#modalResponseBody').text("Failed to create device with error, "+res.error);
                    }
                    else{
                        $('#modalResponse').modal('show');
                    }

                },
                error: function(error){
                    console.log(error);
                }
            });
        }
    });

    $('.report').click(function () {
        var $tr = $(this).closest('tr');
        var mac = $tr.children('td.macAddress').text();
        var attack = "gold_apple"
        if ($tr.children('td.os').text() == "Android") {
            attack = "gallery"
        }

        window.open("/loadDeviceReports/"+mac+"/");
    });
    //Handling lock device
    $('body').on('click', '.btn-lock-clicked', function () {
        var $tr = $(this).closest('tr');
        $('#lockModalBody').text("Are you sure you want to lock device "+$tr.children('td.deviceName').text());
        $('#approveDeviceDelete').data('mac', $tr.find(".macAddress").text());
        $('#lockDevice').modal('show');
    });
    $('#btnLockYes').click(function () {
        var mac = $('#approveDeviceDelete').data('mac');
        $.ajax({
            url: '/lockDevice',
            data: {'mac_address':mac},
            type: 'POST',
            success: function(response){
                $('#lockDevice').modal('hide');
                console.log(response);
                if(response.hasOwnProperty('error')){
                    $('#modalOnResponseHeader').css('background', '#E2747E');
                    $('#responseModalTitle').text("Failed");
                    $('#modalResponseBody').text(response.error);

                }else{
                    $('#responseModalTitle').text("Locked");
                    $('#modalResponseBody').text(response.message);
                }
                $('#modalResponse').modal('show');

            },
            error: function(error){
                console.log(error);
            }
        });
    });

    //Handling unlock device
    $('body').on('click', '.btn-unlock-clicked', function () {
        var $tr = $(this).closest('tr');
        $('#unlockModalBody').text("Are you sure you want to unlock device "+$tr.children('td.deviceName').text());
        $('#unlockDeviceTitle').text('Unlock')
        $('#unlockDevice').data('mac', $tr.find(".macAddress").text());
        $('#unlockDevice').modal('show');
    });
    $('#btnUnLockYes').click(function () {
        var mac = $('#unlockDevice').data('mac');
        $.ajax({
            url: '/unlockDevice',
            data: {'mac_address':mac},
            type: 'POST',
            success: function(response){
                $('#unlockDevice').modal('hide');
                if(response.hasOwnProperty('error')){
                    $('#modalOnResponseHeader').css('background', '#E2747E');
                    $('#modalResponseTitle').text("Failed");
                    $('#modalResponseBody').text("Failed to lock device with error, "+response.error);
                }else{
                    $('#responseModalTitle').text("Locked");
                    $('#modalResponseBody').text(response.message);
                    $('#modalResponse').modal('show');
                }

            },
            error: function(error){
                // console.log(error);
            }
        });
    });

    //Handling edit onClick event
    $('body').on('click','.btn-default-clicked', function(){
        var $tr = $(this).closest('tr');
        var $osVersions = $('#editOsVersion');
        $('#editDeviceName').val($tr.children('td.deviceName').text());
        $('#editAccount').val($tr.children('td.account').text());
        $('#editMacAddress').val($tr.children('td.macAddress').text());
        $('#editPhoneNumber').val($tr.children('td.phoneNumber').text());
        $('#editOwner').val($tr.children('td.owner').text());
        $('#editOs').val($tr.children('td.os').text());
        $('#editOs').attr('disabled','disabled');
        $('#editMacAddress').attr('disabled','disabled');
        //loading os versions
        $osVersions.empty();
        var request = new XMLHttpRequest();

        request.open("GET", "../static/os_versions.json", false);
        request.send(null);
        var vals = JSON.parse(request.responseText.toString());

        $osVersions.empty();
        $.each(vals[$tr.children('td.os').text().toString().toLowerCase()],function (index, value) {
            $osVersions.append("<option>" + value + "</option>");
        });
        $osVersions.val($tr.children("td.osVersion").text());
        $('#editDevice').modal('show');
    });

    //Handling update device request
    $('#btnEditDevice').click(function () {
        var disabled = $('#editDeviceForm').find(':input:disabled').removeAttr('disabled');
        $.ajax({
            url: '/updateDevice',
            data: $('#editDeviceForm').serialize(),
            type: 'POST',
            success: function(response){
                disabled.attr('disabled','disabled');
                $('#editDevice').modal('hide');
                if(response.hasOwnProperty('error')){
                    $('#modalOnResponseHeader').css('background', '#E2747E');
                    $('#modalResponseTitle').text("Failed");
                    $('#modalResponseBody').text(response.error);
                }else{
                    $('#responseModalTitle').text("Device updated");
                    $('#modalResponseBody').text("Device updated successfully");
                }
                $('#modalResponse').modal('show');

            },
            error: function(error){
                disabled.attr('disabled','disabled');
                // console.log(error);
            }
        });
    });

    $("#modalResponse").on('hide.bs.modal', function () {
        window.location.reload();
    });

    $('#btnDeviceFormClose').click(function(){
        $("#createDeviceForm").validate().resetForm();
        $("#createDeviceForm")[0].reset();
    });

    $('#btnEditDeviceFormClose').click(function(){
        $("#editDeviceForm").validate().resetForm();


    });

//Handling delete onClick event
    $('body').on('click','.btn-danger-clicked',function(){
        var $tr = $(this).closest('tr');
        $('#approveDeviceDelete').data('mac', $tr.find(".macAddress").text());
        $('#approveDeviceDelete').data('rowid', $tr.index()+1);
        $('#approveDeviceDelete').modal('show');
        // $tr.remove();
    });

    //Delete selected device row
    $('#btnDelteYes').click(function () {
        var mac = $('#approveDeviceDelete').data('mac');
        var rowIndex = $('#approveDeviceDelete').data('rowid');
        console.log(rowIndex);
        $('#approveDeviceDelete').modal('hide');
        $.ajax({
            url: '/deleteDevice',
            data: {'mac_address':mac},
            type: 'POST',
            success: function(response){
                if(response.hasOwnProperty('error')) {
                    $('#modalOnResponseHeader').css('background', '#E2747E');
                    $('#modalResponseTitle').text("Failed");
                    $('#modalResponseBody').text("Failed to create device with error, " + res.error);
                }else{
                    window.location.reload();
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    });
    function loadUsers () {
        $.ajax({
            url: '/getUserNamesList',
            data: {},
            type: 'GET',
            success: function (response) {
                if (response.hasOwnProperty('error')) {
                    $('#modalOnResponseHeader').css('background', '#E2747E');
                    $('#modalResponseTitle').text("Failed");
                    $('#modalResponseBody').text("Failed to create device with error, " + res.error);
                } else {
                    // window.location.reload();

                    $.each( response['users'], function( index, value ){
                        $('#inputOwner').append($('<option/>', {
                            value: value,
                            text : value
                        }));
                        $('#editOwner').append($('<option/>', {
                            value: value,
                            text : value
                        }));
                    });
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }

    //loading os version depend on  os type
    $('#inputOs').change(function () {
        var $osVersions = $('#inputOsVersion');

        var vals = [];
        var entry = "";

        switch($(this).val()) {
            case "Android":
                entry = "android";
                break;

            case "IOS":
                entry = "ios";
                break;
            default:
                vals = ['Please select OS type'];
                $osVersions.empty();
                $osVersions.append("<option> Please select OS type </option>");
                return;
        }
        var request = new XMLHttpRequest();
        request.open("GET", "../static/os_versions.json", false);
        request.send(null);
        vals = JSON.parse(request.responseText.toString());

        $osVersions.empty();
        $.each(vals[entry],function (index, value) {
            $osVersions.append("<option>" + value + "</option>");
        });
    });

    //trigger on change event for os version dropdown
    $('#inputOs').trigger('change');
});







