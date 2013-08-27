'use strict';

(function($) {
    $(document).ready(function(){
    
        //鼠标移动到user头像时显示user相关信息
        $("li.media").on("mouseleave", function(e){
            e.preventDefault();
            $(this).find(".user-img").popover("hide");
        });
        $('.user-img').on("mouseenter", function(e){
            e.preventDefault();
            $(this).popover("show", 
                {html: true}
            );
            
        });
        
        $(document).on("click", ".friend", function() {
            var self = this,
                to_user = $(this).attr('username');
            $.ajax({
                type: "POST",
                url: "/relation/action/",
                data: { "to_user": to_user }
            }).done(function( msg ) {
                $(self).html(msg);
            });
            return false;
        });
    });
})(jQuery);
