;var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    }, success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl('sys/' + file_key) + '"/>' + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';
        if ($(".upload_pic_xcx .pic-each").size() > 0) {
            $(".upload_pic_xcx .pic-each").html(html);
        } else {
            $(".upload_pic_xcx").append('<span class="pic-each">' + html + '</span>');
        }
        sys_setting_set.delete_img();
    }
};

var upload_gzh = {
    error: function (msg) {
        common_ops.alert(msg);
    }, success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl('sys/' + file_key) + '"/>' + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';
        if ($(".upload_pic_gzh .pic-each").size() > 0) {
            $(".upload_pic_gzh .pic-each").html(html);
        } else {
            $(".upload_pic_gzh").append('<span class="pic-each">' + html + '</span>');
        }
        sys_setting_set.delete_img();
    }
};

var sys_setting_set = {
    init: function () {
        this.eventBind();
        this.delete_img();
    }, eventBind: function () {
        $(".wrap_sys_set .upload_pic_xcx input[name=pic]").change(function () {
            $(".wrap_sys_set .upload_pic_xcx").submit();
        });

        $(".wrap_sys_set .upload_pic_gzh input[name=pic]").change(function () {
            $(".wrap_sys_set .upload_pic_gzh").submit();
        });

        $(".wrap_sys_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理，请不要重复提交");
                return;
            }

            if ($(".upload_pic_xcx .pic-each").size() < 1) {
                common_ops.alert("请上传小程序码~~");
                return;
            }

            if ($(".upload_pic_gzh .pic-each").size() < 1) {
                common_ops.alert("请上传公众号码~~");
                return;
            }

            btn_target.addClass("disabled");

            var data = {
                mini_program_code_image: $(".upload_pic_xcx .pic-each .del_image").attr("data"),
                public_number_image: $(".upload_pic_gzh .pic-each .del_image").attr("data"),
            };

            $.ajax({
                url: common_ops.buildUrl("/sys/setting-set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/sys/setting-set");
                        }
                    }

                    common_ops.alert(res.msg, callback);
                }
            });

        });
    }, delete_img: function () {
        $(".wrap_sys_set .del_image").unbind().click(function () {
            $(this).parent().remove();
        });
    }
};

$(document).ready(function () {
    sys_setting_set.init();
});