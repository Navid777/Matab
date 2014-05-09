$(document).ready(function() {
    $(".form-group input[type='text']").addClass('form-control').each(function(i, input) {
        var $input = $(input);
        var $parent = $input.parent();
        $input.attr('placeholder', $parent.find('label').html());
    });
    $(".btn input[checked='checked']").removeAttr('checked').prop('checked', true).parent().addClass('active');
});