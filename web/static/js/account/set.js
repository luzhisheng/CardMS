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
var account_set_ops = {
    init: function () {
        this.eventBind();
        this.delete_img();
    },
    eventBind: function () {

        $(".wrap_account_set .upload_pic_wrap input[name=pic]").change(function () {
            $(".wrap_account_set .upload_pic_wrap").submit();
        });

        $(".wrap_account_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var nickname_target = $(".wrap_account_set input[name=nickname]");
            var nickname = nickname_target.val();

            var mobile_target = $(".wrap_account_set input[name=mobile]");
            var mobile = mobile_target.val();

            var email_target = $(".wrap_account_set input[name=email]");
            var email = email_target.val()

            var sex_target = $(".wrap_account_set select[name=sex]");
            var sex = sex_target.val();

            var login_name_target = $(".wrap_account_set input[name=login_name]");
            var login_name = login_name_target.val();

            var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
            var login_pwd = login_pwd_target.val();

            if ($(".wrap_account_set .pic-account").size() < 1) {
                common_ops.alert("请上传头像~~");
                return;
            }

            if (nickname.length < 1) {
                common_ops.tip("请输入符合规范的姓名~~", nickname_target);
                return false;
            }

            if (mobile.length < 1) {
                common_ops.tip("请输入符合规范的手机号码~~", mobile_target);
                return false;
            }

            if (email.length < 1) {
                common_ops.tip("请输入符合规范的邮箱~~", email_target);
                return false;
            }

            if (sex.length !== 1) {
                common_ops.tip("请输入符合规范的性别~~", sex_target);
                return false;
            }

            if (login_name.length < 1) {
                common_ops.tip("请输入符合规范的登录用户名~~", login_name_target);
                return false;
            }

            if (login_pwd.length < 6) {
                common_ops.tip("请输入符合规范的登录密码~~", login_pwd_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                avatar: $(".wrap_account_set .pic-account .del_image").attr("data"),
                nickname: nickname,
                mobile: mobile,
                email: email,
                sex: sex,
                login_name: login_name,
                login_pwd: login_pwd,
                id: $(".wrap_account_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/account/set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/account/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });


        });
    },
    delete_img: function () {
        $(".wrap_account_set .del_image").unbind().click(function () {
            $(this).parent().remove();
        });
    }
};

$(document).ready(function () {
    account_set_ops.init();
});