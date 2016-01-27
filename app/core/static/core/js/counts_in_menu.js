
$(document).ready(function() {
    var url_for_counts = '/core/get-count-for-menu.json';

    app.core.update_counts_in_main_menu = function() {
        $.get(url_for_counts, function(data){
            $('.main-menu-item__suffix_notifications').text(data['unreaded_notifications'] || '0');
            $('.main-menu-item__suffix_goals').text(data['all_goals'] || '0');
        });
    }

    app.core.update_counts_in_main_menu();
    setInterval(app.core.update_counts_in_main_menu, 100000);
});
