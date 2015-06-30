/*
 * Превращает несколько checkbox-элементов в радио-баттоны.
 * Другими словами не позволяет выбрать несколько чебоксов из набора.
 * Пример использования:
 * $('.container-with-checkboxes').single_choice_checkboxes({
 *     checkbox: '.checkbox-css-id'
 * });
 */
$.fn.single_choice_checkboxes = function(settings) {
    function checkboxes_binding() {
        $(settings.checkbox).not('.single-choices-checkboxes-processed').each(function(i, elem) {
            $(elem).on('change', function() {
                if ($(this).is(':checked')) {
                    var $checkbox = $(settings.checkbox);
                    $checkbox.not(this).removeAttr('checked');
                }
            }).addClass('single-choices-checkboxes-processed');
        });
    }

    checkboxes_binding();

    $(this).on('DOMNodeInserted', function(event) {
        checkboxes_binding();
    });

    return this;
};
