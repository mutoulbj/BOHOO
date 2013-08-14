'use strict';

(function($) {
    $(document).ready(function(){
        $(".friend").live("click", function() {
            var self = this,
                to_user = $(this).attr('username') ;
            $.ajax({
                type: "POST",
                url: "/relation/action/",
                data: { to_user: to_user }
            }).done(function( msg ) {
                $(self).val(msg);
            });
            return false;
        });
    });
})(jQuery);
