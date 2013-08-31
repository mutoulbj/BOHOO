/**
 * Created with PyCharm.
 * User: fan
 * Date: 13-8-31
 * Time: PM11:25
 * To change this template use File | Settings | File Templates.
 */
function quit_success() {
    $("#quit_group").html("已退出").removeClass("btn-primary").addClass("disabled").attr('disabled', true);
    $.globalMessenger().post({
        message: "成功退出",
        hideAfter: 2,
        type: 'success',
        showCloseButton: true
    })
}
$(document).ready(function () {
    $("#quit_group").click(function () {
        if (confirm("确认退出该小组?")) {
            $.ajax({
                async: false,
                cache: false,
                url: "/group/ajax_quite_group/",    //url: "{% url 'ajax_quite_group' %}",
                type: "POST",
                data: {"group_id": $(this).data("group-id")},
                dataType: "json",
                success: quit_success()
//                                        fail: $.globalMessenger().post({
//                                            message: "服务器错误,请稍后再试",
//                                            hideAfter: 2,
//                                            type: 'error',
//                                            showCloseButton: true
//                                        })
            })
        }
    })

})