/**
 * Плагин, для галочки удаления формы из formset.
 * При включении галочки удаления форма скрывается.
 *
 * Пример использования:
 *  $(document).ready(function() {
 *      $('.formset-form-items').formset_delete_field({
 *          // галочка удаления формы
 *          checkbox: '.formset-form-items .formset__item .formset-delete-container input[type="checkbox"]',
 *          // контейнер с одной формой из formset
 *          form_item_container: '.formset-form-items .formset__item',
 *      });
 *  });
 */

$.fn.formset_delete_field = function(settings) {
    function checkboxes_binding() {
        $(settings.checkbox).not('.formset-delete-field-processed').each(function(i, elem) {
            $(elem).on('change', function() {
                var $form_item = $(elem).closest(settings.form_item_container);
                if ($(this).is(':checked')) {
                    $form_item.hide();
                }
                else {
                    $form_item.show();
                }
            }).addClass('formset-delete-field-processed');
        });
    }

    checkboxes_binding();

    $(this).on('DOMNodeInserted', function(event) {
        checkboxes_binding();
    });

    return this;
};
