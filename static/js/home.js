$(document).ready(function(){

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
                    $('#modalResponse').modal('show');


                },
                error: function(error){
                    console.log(error);
                }
            });
        }else{console.log(1);
        }
    });

    //validate editDevice form
    $('#editDeviceForm').click(function () {
        if($('#editDeviceForm').valid()){

        }

    });

    //Handling edit onClick event
    $('body').on('click','.btn-default-clicked',function(){
        var $tr = $(this).closest('tr');
        var $osVersions = $('#editOsVersion');
        $('#editDeviceName').val($tr.children('td.deviceName').text());
        $('#editAccount').val($tr.children('td.account').text());
        $('#editMacAddress').val($tr.children('td.macAddress').text());
        $('#editPhoneNumber').val($tr.children('td.phoneNumber').text());
        $('#editOwner').val($tr.children('td.owner').text());
        $('#editOs').val($tr.children('td.os').text());
        $('#editOs').attr('disabled','disabled');
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

        $.ajax({
            url: '/updateDevice',
            data: $('#editDeviceForm').serialize(),
            type: 'POST',
            success: function(response){
                $('#editDevice').modal('hide');
                $('#responseModalTitle').text("Device updated");
                $('#modalResponseBody').text("Device updated successfully");
                $('#modalResponse').modal('show');
            },
            error: function(error){
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

        $('#approveDeviceDelete').modal('hide');
        $.ajax({
            url: '/deleteDevice',
            data: {'mac_address':mac},
            type: 'POST',
            success: function(response){
                $("tr").eq(rowIndex).remove();
            },
            error: function(error){
                console.log(error);
            }
        });
    });

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

    $(".search").keyup(function () {
        var searchTerm = $(".search").val();
        var listItem = $('.results tbody').children('tr');
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('");

        $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
            return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
        }
        });

        $(".results tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
            $(this).attr('visible','false');
        });

        $(".results tbody tr:containsi('" + searchSplit + "')").each(function(e){
            $(this).attr('visible','true');
        });

        var jobCount = $('.results tbody tr[visible="true"]').length;
        $('.counter').text(jobCount + ' items');

        if(jobCount == '0') {$('.no-result').show();}
        else {$('.no-result').hide();}
    });

});







