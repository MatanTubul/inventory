$(document).ready(function() {
    var activeEl = 0;
    $(function() {
        var items = $('.btn-nav');
        $( items[activeEl] ).addClass('active');
        $( ".btn-nav" ).click(function() {
            $( items[activeEl] ).removeClass('active');
            $( this ).addClass('active');
            activeEl = $( ".btn-nav" ).index( this );
            // loadReport($(this).attr('id'));
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

    $('#addToSuccess').click(function () {
        console.log("success");
        $('.selected').css('background', '#5cb85c');
        $('.selected').val("success");
        flushSelected()
    });

    $('#addToFailed').click(function () {
        $('.selected').css('background', '#d9534f');
        $('.selected').val("failed");
        flushSelected()
    });

    $('#addToPartial').click(function () {
        $('.selected').css('background', '#f0ad4e');
        $('.selected').val("partial");
        flushSelected()
    });

    $('#addTodo').click(function () {
        $('.selected').css('background', '#777');
        $('.selected').val("todo");
        flushSelected()
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
});