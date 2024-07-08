;
var account_permission_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_account_permission_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var name_target = $(".wrap_account_permission_set input[name=name]");
            var name = name_target.val();

            var description_target = $(".wrap_account_permission_set input[name=description]");
            var description = description_target.val();


            if (name.length < 1) {
                common_ops.tip("请输入符合规范的权限ID~~", name_target);
                return false;
            }

            if (description.length < 1) {
                common_ops.tip("请输入符合规范的权限名称~~", description_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                name: name,
                description: description,
                id: $(".wrap_account_permission_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/account/permission_set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/account/permission");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });
        });
    },
};

$(document).ready(function () {
    account_permission_set_ops.init();
});