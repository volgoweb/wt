
$(document).ready(function() {
    var url_for_counts = '/notifications/get-count.json';

    function update_counts_in_main_menu() {
        $.get(url_for_counts, function(data){
            $('.main-menu-item__suffix_notifications').text(data['all'] || '0');
        });
    }

    update_counts_in_main_menu();
    setInterval(update_counts_in_main_menu, 10000);
});
