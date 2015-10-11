
$(document).ready(function() {
    var $readed_checkbox = $('.notifications-item__readed-checkbox');
    $readed_checkbox.on('change', function(){
        var pk = $(this).data('pk');
        var $cb = $(this);
        var readed = 0;
        if ($(this).prop('checked')) {
            readed = 1;
        }
        $.get('/notifications/set-readed/'+pk, {readed: readed}, function(data){
            if ($('#id_readed').val() === 'unreaded') {
                $cb.closest('tr').hide();
            }
            app.notification.update_counts_in_main_menu();
        }).fail(function(){
            if (readed) {
                $cb.prop('checked', false);
            }
            else {
                $cb.prop('checked', true);
            }
        });
    });
});
