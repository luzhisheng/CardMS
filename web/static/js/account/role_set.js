;
var account_role_set_ops = {
    init: function () {
        this.eventBind();
        this.bindEvents();
        this.setDefaultSelectedPermissions();
    },
    bindEvents: function () {
        $('input[name=selectAll]').change(this.handleSelectAllChange);
        $('.permission').change(this.handlePermissionChange);
    },
    handleSelectAllChange: function () {
        var parentDiv = $(this).closest('div');
        parentDiv.find('.permission').prop('checked', $(this).prop('checked'));
    },
    handlePermissionChange: function () {
        var parentDiv = $(this).closest('div');
        if (!$(this).prop('checked')) {
            parentDiv.find('input[name=selectAll]').prop('checked', false);
        } else {
            if (parentDiv.find('.permission:checked').length == parentDiv.find('.permission').length) {
                parentDiv.find('input[name=selectAll]').prop('checked', true);
            }
        }
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

            // 定义所有权限的名称
            var permissionNames = [
                "admin_index", "account_index", "account_set", "account_ops", "account_role", "account_role_set", "account_role_ops",
                "card_index", "card_set", "card_ops", "card_cat", "card_cat_set", "card_cat_ops",
                "member_index", "member_set", "member_ops", "member_comment", "member_comment_set", "member_comment_ops",
                "finance_index", "finance_account", "stat_index", "stat_card", "stat_member", "stat_share", "sys_index"
            ];

            // 收集所有权限的值
            var permissions = permissionNames.map(function (name) {
                return $(".wrap_account_role_set input[name=" + name + "]:checked").val();
            }).filter(function (value) {
                return value; // 过滤掉空值
            });

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
                permissions_id: permissions,
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
    setDefaultSelectedPermissions: function () {
        selectedPermissions.forEach(function (permissionId) {
            var checkbox = document.querySelector('input[class="permission"][value="' + permissionId + '"]');
            if (checkbox) {
                checkbox.checked = true;
            }
        });
    }
};

$(document).ready(function () {
    account_role_set_ops.init();
});