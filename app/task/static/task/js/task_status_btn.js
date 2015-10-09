$(document).ready(function() {
    var $status_btn = $('.task-item__status-btn');
    var set_status_url = '/tasks/set-task-status/';

    $status_btn.on('click', function(){
        var chb = this;
        var new_status = '';
        var task_pk = $(this).data('task-pk');
        if ($(this).prop('checked')) {
            new_status = 'ready'
        }
        else {
            new_status = 'in_work'
        }
        $.get(set_status_url, {task: task_pk, new_status: new_status}, function(data){
            if (data !== 'ok') {
                if ($(this).prop('checked')) {
                    $(chb).prop('checked', false);
                }
                else {
                    $(chb).prop('checked', false);
                }
            }
        })
    });
});
