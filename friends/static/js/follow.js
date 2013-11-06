/**
 * Created by fan on 13-11-6.
 */

$('.follow').bind('click' ,function(e){
    e.preventDefault();
    var self = $(this);
    var user_id = $(this).data('user_id');
    $.ajax({
        url: "/friends/follow/",
        data: {'user_id': user_id},
        dataType: "json",
        type: 'post',
        success: function(){
            self.hide();
            $('.unfollow', self.parent()).show()
        }
    })
});

$('.unfollow').bind('click', function(e){
    e.preventDefault();
    var self = $(this);
    var user_id = $(this).data('user_id');
    $.ajax({
        url: "/friends/unfollow/",
        data: {'user_id': user_id},
        dataType: "json",
        type: 'post',
        success: function(){
            self.hide();
            $('.follow', self.parent()).show()
        }
    })
});
