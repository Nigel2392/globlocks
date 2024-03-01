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
});