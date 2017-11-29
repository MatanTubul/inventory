$(document).ready(function() {
    var activeEl = 0;
    var djangoData = $('#selectedAttack').data();
    $(function() {
        console.log(djangoData['name']);
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
                $(this).attr('title', 'Expand this branch').find(' > i').addClass('fa-plus-circle').removeClass('fa-minus-circle');
            } else {
                children.show('fast');
                $(this).attr('title', 'Collapse this branch').find(' > i').addClass('fa-minus-circle').removeClass('fa-plus-circle');
            }
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
            $(this).css('background', '#5bc0de');
        }
    });
    function flushSelected() {
        $('.selected').removeClass('selected')
    };

    $(".issues").click(function (e) {
        e.preventDefault();
        // alert($(this).attr('id'));
    });

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
            default:
                break;
        }
    }

    /**
     * Parsing report tree into json object
     */
    $("#buttonList").click(function() {
        var reportToJson = [];
        var mapkeyToDepth = {};
        $('ul.treeList').each(function(i, ul) {
            $(ul).find("li").each(function(j,li){
                // Now you can use $(ul) and $(li) to refer to the list and item
                var value = $($(li).children("span")).text();
                var key = ($($(li).children("span")).attr('id'));
                var reportDepth = $($(li).children("span")).parents('li').length;
                if ($(li).hasClass('parent_li') ) {
                    setReportValKey(reportToJson, mapkeyToDepth, key, null,reportDepth)

                } else {
                    setReportValKey(reportToJson, mapkeyToDepth, key, value,reportDepth);
                }
            });
        });
    });
});