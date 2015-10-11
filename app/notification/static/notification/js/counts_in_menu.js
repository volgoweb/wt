
$(document).ready(function() {
    var url_for_counts = '/notifications/get-count.json';

    app.notification.update_counts_in_main_menu = function() {
        $.get(url_for_counts, function(data){
            $('.main-menu-item__suffix_notifications').text(data['unreaded'] || '0');
        });
    }

    app.notification.update_counts_in_main_menu();
    setInterval(app.notification.update_counts_in_main_menu, 10000);
});
