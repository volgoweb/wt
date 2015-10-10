$(document).ready(function() {
    var url_for_sec_menu = '/tasks/get-count-tasks.json';
    
    function update_count_in_sec_menu() {
        $.get(url_for_sec_menu, function(data){
            for (key in data) {
                $('.sec-menu-item__suffix_tasks_' + key).text(data[key] || '0');
                $('.main-menu-subitem__suffix_tasks_' + key).text(data[key] || '0');
            }
            $('.main-menu-item__suffix_tasks').html('<span class="main-menu-item__suffix_tasks_today">' + (data['today'] || '0') + '</span>|<span class="main-menu-item__suffix_tasks_overdue">' + data['overdue'] || '0' + '</span>');
        });
    }

    update_count_in_sec_menu();
    setInterval(update_count_in_sec_menu, 60000);
});
