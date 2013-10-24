/**
 * Created with PyCharm.
 * User: fan
 * Date: 13-8-31
 * Time: PM11:31
 * To change this template use File | Settings | File Templates.
 */
function join_success() {
    $("#join_group").removeClass("btn-primary").addClass("disabled").attr('disabled', true);
    $("#quit_group").addClass("btn-primary").removeClass("disabled").attr('disabled', false);
    $.globalMessenger().post({
        message: "成功加入",
        hideAfter: 2,
        type: 'success',
        showCloseButton: true
    });
    location.reload();
}
function apply_join_success() {
    $("#apply_join_group_modal").modal("hide");
    $("#apply_join_modal_trigger").html("处理中...").removeClass("btn-primary").addClass("disabled").attr('disabled', true);
    $.globalMessenger().post({
        message: "申请成功,等待管理员通过申请",
        hideAfter: 2,
        type: 'success',
        showCloseButton: true
    })
}
function apply_be_manager_success() {
    $("#apply_be_manager_modal").modal("hide");
    $("#apply_be_manager_modal_trigger").html("处理中...").removeClass("btn-primary").addClass("disabled").attr('disabled', true);
    $.globalMessenger().post({
        message: "申请成功,等待管理员通过申请",
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
                url: "/group/ajax_join_group/",     //url: "{% url 'ajax_join_group' %}",
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
    $("#apply_join_group").click(function () {
        $.ajax({
            async: false,
            url: "/group/ajax_apply_join_group/",     //url: "{% url 'ajax_apply_join_group' %}",
            type: "POST",
            data: {"group_id": $(this).data("group-id"), "apply_reason": $("#apply_reason").val()},
            dataType: "json",
            success: apply_join_success()
        })
    });

    // 申请成为管理员
    $("#apply_be_manager").click(function () {
        $.ajax({
            async: false,
            url: "/group/ajax_apply_be_manager/",     //url: "{% url 'ajax_apply_join_group' %}",
            type: "POST",
            data: {"group_id": $(this).data("group-id"), "apply_reason": $("#apply_be_manager_reason").val()},
            dataType: "json",
            success: apply_be_manager_success()
        })
    });
});
