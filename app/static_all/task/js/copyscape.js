
$(document).ready(function() {
    var $check_btn = $('.plagiary__check-btn');
    var $plagiary_state_container = $('.plagiary__clone-items');

    $check_btn.on('click', function(event) {
        check_unique();
    });

    function check_unique() {
        var text = $('#id_article_text').val();
        $plagiary_state_container.html('Идет проверка на уникальность...');
        $.post('/copyscape/get-plagiary-state/', {
            text: text,
        }).done(function(data){
            console.log(data);
            $plagiary_state_container.html(data);
        });
    }
});
