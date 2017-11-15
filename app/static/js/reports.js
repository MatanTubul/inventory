$(document).ready(function() {
    var activeEl = 0;
    var selectedLi = null;
    $(function() {
        var items = $('.btn-nav');
        $( items[activeEl] ).addClass('active');
        $( ".btn-nav" ).click(function() {
            $( items[activeEl] ).removeClass('active');
            $( this ).addClass('active');
            console.log($(this).attr('id'));
            activeEl = $( ".btn-nav" ).index( this );
            $.ajax({
                url: '/getReportByAttack',
                data: {'attack':$(this).attr('id')}
            });
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

    $('body').on('click', 'li', function() {
        // if (($(this).parent('ul').attr('class')) !=)
        if (selectedLi == null) {
            selectedLi = ($(this).parent('ul').attr('class'));
            console.log(selectedLi);
        }
        $(this).toggleClass('selected');
    });

    $('#addToSuccess').click(function () {
        $('.success').append($('.'+selectedLi+' .selected').removeClass('selected'));
        selectedLi = null
    });

    $('#addToFailed').click(function () {
        $('.danger').append($('.'+selectedLi+' .selected').removeClass('selected'));
        selectedLi = null
    });

    $('#addToPartial').click(function () {
        $('.warning').append($('.'+selectedLi+' .selected').removeClass('selected'));
        selectedLi = null
    });

    $('#addTodo').click(function () {
        $('.todo').append($('.'+selectedLi+' .selected').removeClass('selected'));
        selectedLi = null
    });
});