;var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    }, success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl('member/' + file_key) + '"/>' + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';
        if ($(".upload_pic_wrap .pic-each").size() > 0) {
            $(".upload_pic_wrap .pic-each").html(html);
        } else {
            $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');
        }
        member_set_ops.delete_img();
    }
};
var member_set_ops = {
    init: function () {
        this.eventBind();
        this.delete_img();
    }, eventBind: function () {
        $(".wrap_member_set .upload_pic_wrap input[name=pic]").change(function () {
            $(".wrap_member_set .upload_pic_wrap").submit();
        });

        $(".wrap_member_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理，请不要重复提交");
                return;
            }

            var nickname_target = $(".wrap_member_set input[name=nickname]");
            var nickname = nickname_target.val();

            var mobile_target = $(".wrap_member_set input[name=mobile]");
            var mobile = mobile_target.val();

            if ($(".wrap_member_set .pic-each").size() < 1) {
                common_ops.alert("请上传头像~~");
                return;
            }

            if (nickname.length < 1) {
                common_ops.tip("请输入符合规范的姓名", nickname_target);
                return;
            }

            if (mobile.length < 1) {
                common_ops.tip("请输入符合规范的手机号码~~", mobile_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                avatar: $(".wrap_member_set .pic-each .del_image").attr("data"),
                nickname: nickname,
                mobile: mobile,
                id: $(".wrap_member_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/member/set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/member/index");
                        }
                    }

                    common_ops.alert(res.msg, callback);
                }
            });

        });
    }, delete_img: function () {
        $(".wrap_member_set .del_image").unbind().click(function () {
            $(this).parent().remove();
        });
    }
};

$(document).ready(function () {
    member_set_ops.init();
});