$(document).ready(function() {
    var activeEl = 0;
    var djangoData = $('#selectedAttack').data();
    // $('.level2 ul').hide();
    $(function() {
        // console.log(djangoData['name']);
        var items = $('.btn-nav');
        activeEl = $.map(items, function(obj, index) {
            if(obj.id == djangoData['name']) {
                return index;
            }
        });
        $( items[activeEl] ).addClass('active');
        $( ".btn-nav" ).click(function() {
            $( items[activeEl] ).removeClass('active');
            $( this ).addClass('active');
            activeEl = $( ".btn-nav" ).index( this );
            djangoData = ($(this).attr('id'));
            var mac = $('.macAddress').text();
            console.log(mac);
            window.location.replace("/loadDeviceReports/"+mac+"/"+djangoData);
        });
    });





    $(function () {
        $('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Collapse this branch');

        $('.tree li.parent_li > span').on('click', function (e) {
            var children = $(this).parent('li.parent_li').find(' > ul > li');

            if (children.is(":visible")) {
                children.hide('fast');
                $(this).attr('title', 'Expand this branch').addClass('fa-plus-circle').removeClass('fa-minus-circle');
            } else {
                children.show('fast');
                $(this).attr('title', 'Collapse this branch').addClass('fa-minus-circle').removeClass('fa-plus-circle');
            }
            // $('.level2 ul').show();
            e.stopPropagation();
        });
    });

    $(".status").click(function (e) {
        e.preventDefault();
        $(this).toggleClass('selected');
    });
    function setSelected(color, msg) {
        $('.selected').css('background', color);
        $('.selected').text(msg);
        flushSelected();
    }
    $('#addToSuccess').click(function () {
        setSelected('#5cb85c', "success");
    });

    $('#addToFailed').click(function () {
        setSelected('#d9534f', "failed");
    });

    $('#addToPartial').click(function () {
        setSelected('#f0ad4e', "partial");
    });

    $('#addTodo').click(function () {
        setSelected('#777', "todo");
    });

    $('span').each(function() {
        if ($.trim($(this).text()) == 'todo') {
            $(this).css('background', '#777');
        }
        if ($.trim($(this).text()) == 'success') {
            $(this).css('background', '#5cb85c');
        }
        if ($.trim($(this).text()) == 'failed') {
            $(this).css('background', '#d9534f');
        }
        if ($.trim($(this).text()) == 'partial') {
            $(this).css('background', '#f0ad4e');
        }
        if ($.trim($(this).text()) == 'issues') {
            $(this).css('background', '#d9534f');
            $(this).css('color', '#fff');
        }
    });

    $('.fab').hover(function () {
        $(this).toggleClass('active');
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    function flushSelected() {
        $('.selected').removeClass('selected')
    };

    $(".issues").click(function (e) {
        e.preventDefault();
        // alert($(this).attr('id'));
    });
    $(".add_issues").click(function () {
        $('#modalIssue').modal('show');
    });
    $("#addIssues").click(function () {
        $('#modalIssue').modal('hide');
        var url = $('#issue_url').val();
        var url_desc = $('#issue_desc').val();
        var li = $('<li></i> ' +
            '<span class="span_issue_url " title="'+url_desc+'"> ' +
            '<a class="url_hyper_link " target="_blank" href="'+url+'"> '+url+'</a>' +
            '</span> <i class="fa fa-minus-square delete_issue"> ' +
            '</li>');
        $('.issues_list').append(li);
    });

    $(document).on('click', "i.delete_issue",(function () {
        console.log("delete li")
        $(this).closest('li').remove();
    }));

    /**
     * building JSON report based on depth and key
     * @param reportToJson JSON object holding the data
     * @param mapkeyToDepth - Representing relationship between key and depth
     * @param key - key of value
     * @param value - data value
     * @param reportDepth - depth of the item
     */
    function setReportValKey(reportToJson, mapkeyToDepth, key, value, reportDepth) {
        switch(reportDepth) {
            case 1:
                reportToJson[key] = {};
                mapkeyToDepth[reportDepth] = key;
                if (value != null) {
                    reportToJson[key] = value
                }
                break;
            case 2:
                reportToJson[mapkeyToDepth[1]][key] = {};
                if (value != null) {
                    reportToJson[mapkeyToDepth[1]][key] = value
                }
                mapkeyToDepth[reportDepth] = key;
                break;
            case 3:
                reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][key] = {};
                if (value != null) {
                    reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][key] = value
                }
                mapkeyToDepth[reportDepth] = key;
                break;
            case 4:
                reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][mapkeyToDepth[3]][key] = {};
                mapkeyToDepth[reportDepth] = key;
                if (value != null) {
                    reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][mapkeyToDepth[3]][key] = value
                }
                break;
            case 5:
                reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][mapkeyToDepth[3]][mapkeyToDepth[4]][key] = {};
                if (value != null) {
                    reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][mapkeyToDepth[3]][mapkeyToDepth[4]][key] = value
                }
                mapkeyToDepth[reportDepth] = key;
                break;
            case 6:
                reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][mapkeyToDepth[3]][mapkeyToDepth[4]][mapkeyToDepth[5]][key] = {};
                if (value != null) {
                    reportToJson[mapkeyToDepth[1]][mapkeyToDepth[2]][mapkeyToDepth[3]][mapkeyToDepth[4]][mapkeyToDepth[5]][key] = value
                }
                mapkeyToDepth[reportDepth] = key;
                break;
            default:
                break;
        }
    }

    /**
     * Parsing report tree into json object
     */
    $('#saveReport').click(function() {
        $('#processing-modal').modal('show');
        setTimeout(function(){
            $('#processing-modal').modal('hide');
        }, 10000);
        var reportToJson = {};
        var mapkeyToDepth = {};
        $('ul.treeList').each(function(i, ul) {
            $(ul).find("li").each(function(j,li){
                // Now you can use $(ul) and $(li) to refer to the list and item
                var value = $($(li).children("span")).text();
                var key = ($($(li).children("span")).attr('id'));
                var reportDepth = $($(li).children("span")).parents('li').length;
                // console.log(li);
                if ($(li).hasClass('parent_li') ) {
                    setReportValKey(reportToJson, mapkeyToDepth, key, null,reportDepth)

                } else {
                    if (typeof key == "undefined") {
                        var key = ($($(li).children("span")).attr('class'));
                    }
                    if ($($(li).children("span")).hasClass('span_issue_url')) {
                        console.log(reportDepth)
                        value = $($(li).children("span")).attr('title');
                        key =   ($($(li).children("span")).find('a:first').attr('href')).split("https://")[1]

                        console.log(key)
                        console.log(value)
                    }
                    if ($($(li).children("span")).hasClass('add_issues')) {
                        return true;
                    }

                    setReportValKey(reportToJson, mapkeyToDepth, key, value,reportDepth);
                }
            });
        });
        console.log(reportToJson);
        if (reportToJson) {
            $.ajax({
                url:'/updateReportDocument',
                data:JSON.stringify({'report':reportToJson,
                    'mac':$('.macAddress').text(),
                    'attack':djangoData['name']}),
                dataType: 'json',
                contentType: 'application/json',
                type:'POST',
                success: function(response){
                    $('#processing-modal').modal('hide');
                    if(response.hasOwnProperty('error')){
                        console.log(response);
                    }else{
                        location.reload();
                    }
                },
                error: function(error){
                    $('#processing-modal').modal('hide');
                    console.log(error);
                }
            });
        }
    });
});