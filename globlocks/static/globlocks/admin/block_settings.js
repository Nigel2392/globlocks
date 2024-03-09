$(document).ready(function(){
    $(document).on('click', '.goodadvice-collapsible button', function(){

        if (!$(this).parent().hasClass('collapsed')) {
            $(this).parent().addClass('collapsed');
            $(this).parent().find(".goodadvice-collapsible").addClass('collapsed');
            $(this).parent().find('.goodadvice-collapsible-target').hide('fast');
        } else {
            $(this).parent().removeClass('collapsed');
            $(this).parent().find('> .goodadvice-collapsible-target').show('fast');
        }
    });
    $(document).on('click', '.goodadvice-collapsible-close', function(){

        const parent = $(this).closest('.goodadvice-collapsible');

        if (!parent.hasClass('collapsed')) {
            parent.addClass('collapsed');
            parent.find(".goodadvice-collapsible").addClass('collapsed');
            parent.find('.goodadvice-collapsible-target').hide('fast');
        } else {
            parent.removeClass('collapsed');
            parent.find('> .goodadvice-collapsible-target').show('fast');
        }
    });
});