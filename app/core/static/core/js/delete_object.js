$(document).ready(function() {
    $('.object-delete-btn').on('click', function(){
        var $form = $(this).closest('form');
        var delete_confirmation = confirm('Удалить?');
        if (delete_confirmation) {
            $form.find('input[name="deleted"]').val('True');
            $form.submit();
        }
    });
});

