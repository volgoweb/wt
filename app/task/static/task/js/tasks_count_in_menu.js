$(document).ready(function() {
    var url_for_sec_menu = '/tasks/get-count-tasks.json';
    
    function update_count_in_sec_menu() {
        $.get(url_for_sec_menu, function(data){
            for (key in data) {
                $('.sec-menu-item__suffix_tasks_' + key).text(data[key] || '0');
                $('.main-menu-subitem__suffix_tasks_' + key).text(data[key] || '0');
            }
            $('.main-menu-item__suffix_tasks').text(data['today'] || '0' + '|' + data['overdue'] || '0');
        });
    }

    update_count_in_sec_menu();
    setInterval(update_count_in_sec_menu, 60000);
});
