/**
 * Created with PyCharm.
 * User: fan
 * Date: 13-8-31
 * Time: PM11:32
 * To change this template use File | Settings | File Templates.
 */
function quit_success() {
    $("#quit_group").removeClass("btn-danger").addClass("disabled").attr('disabled', true);
    $("#join_group").addClass("btn-primary").removeClass("disabled").attr('disabled', false);
    $("#apply_join_group").addClass("btn-primary").removeClass("disabled").attr('disabled', false);
    $.globalMessenger().post({
        message: "成功退出",
        hideAfter: 2,
        type: 'success',
        showCloseButton: true
    })
}
$(document).ready(function () {
    // 退出小组
    $("#quit_group").click(function () {
        if (confirm("确认退出该群组?")) {
            $.ajax({
                async: false,
                cache: false,
                url: "/group/ajax_quite_group/",     //url: "{% url 'ajax_quite_group' %}",
                type: "POST",
                data: {"group_id": $(this).data("group-id")},
                dataType: "json",
                success: quit_success()
//                fail: $.globalMessenger().post({
//                    message: "服务器错误,请稍后再试",
//                    hideAfter: 2,
//                    type: 'error',
//                    showCloseButton: true
//                })
            })
        }

    })
});
