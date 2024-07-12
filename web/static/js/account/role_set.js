;
const permissions = [
    {
        category: '仪表盘权限',
        subcategories: [
            {
                subcategory: '仪表盘',
                permissions: [
                    {name: 'admin_index', label: '查询', value: '1'}
                ]
            }
        ]
    },
    {
        category: '账户管理权限',
        subcategories: [
            {
                subcategory: '账户列表',
                permissions: [
                    {name: 'account_index', label: '查询', value: '2'},
                    {name: 'account_set', label: '新增/更新', value: '3'},
                    {name: 'account_ops', label: '删除', value: '4'}
                ]
            },
            {
                subcategory: '角色管理',
                permissions: [
                    {name: 'account_role', label: '查询', value: '5'},
                    {name: 'account_role_set', label: '新增/更新', value: '6'},
                    {name: 'account_role_ops', label: '删除', value: '7'}
                ]
            },
            {
                subcategory: '权限管理',
                permissions: [
                    {name: 'account_permission_index', label: '查询', value: '27'},
                    {name: 'account_permission_set', label: '新增/更新', value: '28'},
                    {name: 'account_permission_ops', label: '删除', value: '29'}
                ]
            },
            {
                subcategory: '信息编辑',
                permissions: [
                    {name: 'edit', label: '更新', value: '31'},
                ]
            },
            {
                subcategory: '修改密码',
                permissions: [
                    {name: 'reset_pwd', label: '更新', value: '32'},
                ]
            }
        ]
    },
    {
        category: '卡券管理权限',
        subcategories: [
            {
                subcategory: '卡券列表',
                permissions: [
                    {name: 'card_index', label: '查询', value: '8'},
                    {name: 'card_set', label: '新增/更新', value: '9'},
                    {name: 'card_ops', label: '删除', value: '10'}
                ]
            },
            {
                subcategory: '卡券分类',
                permissions: [
                    {name: 'card_cat', label: '查询', value: '11'},
                    {name: 'card_cat_set', label: '新增/更新', value: '12'},
                    {name: 'card_cat_ops', label: '删除', value: '13'}
                ]
            }
        ]
    },
    {
        category: '会员管理权限',
        subcategories: [
            {
                subcategory: '会员列表',
                permissions: [
                    {name: 'member_index', label: '查询', value: '14'},
                    {name: 'member_set', label: '新增/更新', value: '15'},
                    {name: 'member_ops', label: '删除', value: '16'}
                ]
            },
            {
                subcategory: '会员评论',
                permissions: [
                    {name: 'member_comment', label: '查询', value: '17'},
                    {name: 'member_comment_set', label: '新增/更新', value: '18'},
                    {name: 'member_comment_ops', label: '删除', value: '19'}
                ]
            }
        ]
    },
    {
        category: '财务管理权限',
        subcategories: [
            {
                subcategory: '订单列表',
                permissions: [
                    {name: 'finance_index', label: '查询', value: '20'}
                ]
            },
            {
                subcategory: '财务流水',
                permissions: [
                    {name: 'finance_account', label: '查询', value: '21'}
                ]
            }
        ]
    },
    {
        category: '统计管理权限',
        subcategories: [
            {
                subcategory: '财务统计',
                permissions: [
                    {name: 'stat_index', label: '查询', value: '22'}
                ]
            },
            {
                subcategory: '售卖统计',
                permissions: [
                    {name: 'stat_card', label: '查询', value: '23'}
                ]
            },
            {
                subcategory: '会员消费统计',
                permissions: [
                    {name: 'stat_member', label: '查询', value: '24'}
                ]
            },
            {
                subcategory: '分享统计',
                permissions: [
                    {name: 'stat_share', label: '更新', value: '25'}
                ]
            }
        ]
    },
    {
        category: '系统管理权限',
        subcategories: [
            {
                subcategory: '用户行为日志',
                permissions: [
                    {name: 'sys_index', label: '查询', value: '26'}
                ]
            },
            {
                subcategory: '系统配置信息',
                permissions: [
                    {name: 'setting_set', label: '更新', value: '33'}
                ]
            }
        ]
    }
];

var account_role_set_ops = {
    init: function () {
        this.permissionsHtml();
        this.eventBind();
        this.bindEvents();
        this.setDefaultSelectedPermissions();
    },
    permissionsHtml: function () {
        permissions.forEach(permission => {
            let categoryHtml = `
            <div class="form-group">
                <label class="col-lg-2 control-label">${permission.category}:</label>
                <div class="col-lg-10">
        `;
            permission.subcategories.forEach(sub => {
                categoryHtml += `
                <div class="permissions-body">
                    <label class="control-label"><i>${sub.subcategory}:</i></label>
                    <div class="container mt-3">
                        <label class="checkbox-inline">
                            <input name="selectAll" type="checkbox" value=""> 全选
                        </label>
            `;
                sub.permissions.forEach(perm => {
                    categoryHtml += `
                    <label class="checkbox-inline">
                        <input name="${perm.name}" class="permission" type="checkbox" value="${perm.value}"> ${perm.label}
                    </label>
                `;
                });
                categoryHtml += `</div></div>`;
            });
            categoryHtml += `</div></div><div class="hr-line-dashed"></div>`;
            $('#permissions-container').append(categoryHtml);
        });
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

            // 函数用于提取所有的 name 字段
            function extractPermissionNames(data) {
                let names = [];
                data.forEach(item => {
                    if (item.subcategories) {
                        item.subcategories.forEach(subcat => {
                            if (subcat.permissions) {
                                subcat.permissions.forEach(permission => {
                                    names.push(permission.name);
                                });
                            }
                        });
                    }
                });
                return names;
            }
            var permissionNames = extractPermissionNames(permissions);

            // 收集所有权限的值
            var permissions_id = permissionNames.map(function (name) {
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
                permissions_id: permissions_id,
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
    // 复选框默认选中
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