$(document).ready(function() {
    $('.task-form__delete-btn').on('click', function(){
        var delete_confirmation = confirm('Удалить поручение?');
        if (delete_confirmation) {
            $('.task-form input[name="deleted"]').val('True');
            $('.task-form').submit();
        }
    });
});
