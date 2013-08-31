/**
 * Created with PyCharm.
 * User: fan
 * Date: 13-8-31
 * Time: PM11:25
 * To change this template use File | Settings | File Templates.
 */
function join_success() {
    $("#join_group").removeClass("btn-primary").addClass("disabled").attr('disabled', true);
    $.globalMessenger().post({
        message: "成功加入",
        hideAfter: 2,
        type: 'success',
        showCloseButton: true
    })
}
// 加入小组
$(document).ready(function () {
    $("#join_group").click(function () {
        if (confirm("确认加入该群组?")) {
            $.ajax({
                async: false,
                url: "/group/ajax_join_group/", //url: "{% url 'ajax_join_group' %}",
                type: "POST",
                data: {"group_id": $(this).data("group-id")},
                dataType: "json",
                success: join_success()
//                                        fail: $.globalMessenger().post({
//                                            message: "服务器错误,请稍后再试",
//                                            hideAfter: 2,
//                                            type: 'error',
//                                            showCloseButton: true
//                                        })
            })
        }

    });
});
