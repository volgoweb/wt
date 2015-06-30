
$(document).ready(function() {
    var $form = $('form');
    var $iframe = $form.find('.publish-iframe iframe');
    var $iframe_desc = $form.find('.publish-iframe .iframe-desc');
    var $content_type = $form.find('#id_site_content_type');

    show_or_hide_iframe();
    
    $content_type.on('change', function(){
        show_or_hide_iframe();
    });

    function show_or_hide_iframe() {
        var selected_content_type = $content_type.val();
        if (selected_content_type) {
            iframe_update_and_show();
        }
        else {
            $iframe.hide();
            $iframe_desc.show();
        }
    }

    function iframe_update_and_show() {
        var url
        $iframe.attr('src', generate_url);
        $iframe.show();
        $iframe_desc.hide();
    }

    function generate_url() {
        var base_src = $iframe.data('base-src');
        var selected_content_type = $content_type.val();
        var src = base_src.replace('CONTENT_TYPE', selected_content_type);
        return src;
    }
});
