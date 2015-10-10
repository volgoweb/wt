$(document).ready(function(){
    var $form = $('form.task-form');
    $form.find('#id_due_date').default_datetimepicker();
    $form.find('select[name="contact"]').not('select2-processed').select2().addClass('select2-processed');
    $form.find('select[name="performer_unit"]').not('select2-processed').select2().addClass('select2-processed');
});

