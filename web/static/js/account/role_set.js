;
var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl('account/' + file_key) + '"/>'
            + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';
        if ($(".upload_pic_wrap .pic-account").size() > 0) {
            $(".upload_pic_wrap .pic-account").html(html);
        } else {
            $(".upload_pic_wrap").append('<span class="pic-account">' + html + '</span>');
        }
        account_set_ops.delete_img();
    }
};
var account_role_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {

        $(".wrap_account_role_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var role_name_target = $(".wrap_account_role_set input[name=role_name]");
            var role_name = role_name_target.val();

            var creator_target = $(".wrap_account_role_set input[name=creator]");
            var creator = creator_target.val();

            if (role_name.length < 1) {
                common_ops.tip("请输入符合规范的角色名称~~", role_name_target);
                return false;
            }

            if (creator.length < 1) {
                common_ops.tip("请输入符合规范的创建人~~", creator_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                role_name: role_name,
                creator: creator,
                id: $(".wrap_account_role_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/account/role_set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/account/role");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });


        });
    },
};

$(document).ready(function () {
    account_role_set_ops.init();
});