this.Urls = (function () {
    "use strict";
    var data = {
        "urls": [["account_change_password", [["accounts/password/change/", []]]], ["account_confirm_email", [["accounts/confirm-email/%(key)s/", ["key"]]]], ["account_email", [["accounts/email/", []]]], ["account_email_verification_sent", [["accounts/confirm-email/", []]]], ["account_inactive", [["accounts/inactive/", []]]], ["account_login", [["accounts/login/", []]]], ["account_logout", [["accounts/logout/", []]]], ["account_reset_password", [["accounts/password/reset/", []]]], ["account_reset_password_done", [["accounts/password/reset/done/", []]]], ["account_reset_password_from_key", [["accounts/password/reset/key/%(uidb36)s-%(key)s/", ["uidb36", "key"]]]], ["account_reset_password_from_key_done", [["accounts/password/reset/key/done/", []]]], ["account_set_password", [["accounts/password/set/", []]]], ["account_signup", [["accounts/signup/", []]]], ["api:article-detail", [["api/blogs/%(id)s/", ["id"]]]], ["api:article-list", [["api/blogs/", []]]], ["admin:app_list", [["dashboard/%(app_label)s/", ["app_label"]]]], ["admin:auth_group_add", [["dashboard/auth/group/add/", []]]], ["admin:auth_group_autocomplete", [["dashboard/auth/group/autocomplete/", []]]], ["admin:auth_group_change", [["dashboard/auth/group/%(object_id)s/change/", ["object_id"]]]], ["admin:auth_group_changelist", [["dashboard/auth/group/", []]]], ["admin:auth_group_delete", [["dashboard/auth/group/%(object_id)s/delete/", ["object_id"]]]], ["admin:auth_group_history", [["dashboard/auth/group/%(object_id)s/history/", ["object_id"]]]], ["admin:auth_user_password_change", [["dashboard/users/user/%(id)s/password/", ["id"]]]], ["admin:password_change", [["dashboard/password_change/", []]]], ["admin:index", [["dashboard/", []]]], ["admin:jsi18n", [["dashboard/jsi18n/", []]]], ["admin:login", [["dashboard/login/", []]]], ["admin:logout", [["dashboard/logout/", []]]], ["admin:media:create-media-view", [["dashboard/media/create", []]]], ["admin:media:uploaded-media-complete-view", [["dashboard/media/upload/complete", []]]], ["admin:media:uploaded-media-view", [["dashboard/media/upload", []]]], ["admin:password_change_done", [["dashboard/password_change/done/", []]]], ["admin:profile", [["dashboard/profile/", []]]], ["admin:test-view", [["dashboard/test", []]]], ["admin:users_user_add", [["dashboard/users/user/add/", []]]], ["admin:users_user_autocomplete", [["dashboard/users/user/autocomplete/", []]]], ["admin:users_user_change", [["dashboard/users/user/%(object_id)s/change/", ["object_id"]]]], ["admin:users_user_changelist", [["dashboard/users/user/", []]]], ["admin:users_user_delete", [["dashboard/users/user/%(object_id)s/delete/", ["object_id"]]]], ["admin:users_user_history", [["dashboard/users/user/%(object_id)s/history/", ["object_id"]]]], ["admin:view_on_site", [["dashboard/r/%(content_type_id)s/%(object_id)s/", ["content_type_id", "object_id"]]]], ["admin:website_article_add", [["dashboard/website/article/add/", []]]], ["admin:website_article_autocomplete", [["dashboard/website/article/autocomplete/", []]]], ["admin:website_article_change", [["dashboard/website/article/%(object_id)s/change/", ["object_id"]]]], ["admin:website_article_changelist", [["dashboard/website/article/", []]]], ["admin:website_article_delete", [["dashboard/website/article/%(object_id)s/delete/", ["object_id"]]]], ["admin:website_article_history", [["dashboard/website/article/%(object_id)s/history/", ["object_id"]]]], ["admin:website_articletag_add", [["dashboard/website/articletag/add/", []]]], ["admin:website_articletag_autocomplete", [["dashboard/website/articletag/autocomplete/", []]]], ["admin:website_articletag_change", [["dashboard/website/articletag/%(object_id)s/change/", ["object_id"]]]], ["admin:website_articletag_changelist", [["dashboard/website/articletag/", []]]], ["admin:website_articletag_delete", [["dashboard/website/articletag/%(object_id)s/delete/", ["object_id"]]]], ["admin:website_articletag_history", [["dashboard/website/articletag/%(object_id)s/history/", ["object_id"]]]], ["admin:website_guide_add", [["dashboard/website/guide/add/", []]]], ["admin:website_guide_autocomplete", [["dashboard/website/guide/autocomplete/", []]]], ["admin:website_guide_change", [["dashboard/website/guide/%(object_id)s/change/", ["object_id"]]]], ["admin:website_guide_changelist", [["dashboard/website/guide/", []]]], ["admin:website_guide_delete", [["dashboard/website/guide/%(object_id)s/delete/", ["object_id"]]]], ["admin:website_guide_history", [["dashboard/website/guide/%(object_id)s/history/", ["object_id"]]]], ["admin:website_guidestep_add", [["dashboard/website/guidestep/add/", []]]], ["admin:website_guidestep_autocomplete", [["dashboard/website/guidestep/autocomplete/", []]]], ["admin:website_guidestep_change", [["dashboard/website/guidestep/%(object_id)s/change/", ["object_id"]]]], ["admin:website_guidestep_changelist", [["dashboard/website/guidestep/", []]]], ["admin:website_guidestep_delete", [["dashboard/website/guidestep/%(object_id)s/delete/", ["object_id"]]]], ["admin:website_guidestep_history", [["dashboard/website/guidestep/%(object_id)s/history/", ["object_id"]]]], ["django_summernote-editor", [["summernote/editor/%(id)s/", ["id"]]]], ["django_summernote-upload_attachment", [["summernote/upload_attachment/", []]]], ["djdt:render_panel", [["__debug__/render_panel/", []]]], ["djdt:sql_explain", [["__debug__/sql_explain/", []]]], ["djdt:sql_profile", [["__debug__/sql_profile/", []]]], ["djdt:sql_select", [["__debug__/sql_select/", []]]], ["djdt:template_source", [["__debug__/template_source/", []]]], ["socialaccount_connections", [["accounts/social/connections/", []]]], ["socialaccount_login_cancelled", [["accounts/social/login/cancelled/", []]]], ["socialaccount_login_error", [["accounts/social/login/error/", []]]], ["socialaccount_signup", [["accounts/social/signup/", []]]], ["website:about-us-view", [["about", []]]], ["website:article-detail-view", [["blog/%(pk)s", ["pk"]]]], ["website:article-list-view", [["blog", []]]], ["website:guide-detail-view", [["guides/%(pk)s", ["pk"]]]], ["website:guide-list-view", [["guides", []]]], ["website:home-view", [["", []]]]],
        "prefix": "/"
    };

    function factory(d) {
        var url_patterns = d.urls;
        var url_prefix = d.prefix;
        var Urls = {};
        var self_url_patterns = {};
        var _get_url = function (url_pattern) {
            return function () {
                var _arguments, index, url, url_arg, url_args, _i, _len, _ref, _ref_list, match_ref, provided_keys,
                    build_kwargs;
                _arguments = arguments;
                _ref_list = self_url_patterns[url_pattern];
                if (arguments.length == 1 && typeof (arguments[0]) == "object") {
                    var provided_keys_list = Object.keys(arguments[0]);
                    provided_keys = {};
                    for (_i = 0; _i < provided_keys_list.length; _i++)
                        provided_keys[provided_keys_list[_i]] = 1;
                    match_ref = function (ref) {
                        var _i;
                        if (ref[1].length != provided_keys_list.length)
                            return false;
                        for (_i = 0; _i < ref[1].length && ref[1][_i] in provided_keys; _i++) ;
                        return _i == ref[1].length;
                    };
                    build_kwargs = function (keys) {
                        return _arguments[0];
                    }
                } else {
                    match_ref = function (ref) {
                        return ref[1].length == _arguments.length;
                    };
                    build_kwargs = function (keys) {
                        var kwargs = {};
                        for (var i = 0; i < keys.length; i++) {
                            kwargs[keys[i]] = _arguments[i];
                        }
                        return kwargs;
                    }
                }
                for (_i = 0; _i < _ref_list.length && !match_ref(_ref_list[_i]); _i++) ;
                if (_i == _ref_list.length)
                    return null;
                _ref = _ref_list[_i];
                url = _ref[0], url_args = build_kwargs(_ref[1]);
                for (url_arg in url_args) {
                    var url_arg_value = url_args[url_arg];
                    if (url_arg_value === undefined || url_arg_value === null) {
                        url_arg_value = '';
                    } else {
                        url_arg_value = url_arg_value.toString();
                    }
                    url = url.replace("%(" + url_arg + ")s", url_arg_value);
                }
                return url_prefix + url;
            };
        };
        var name, pattern, url, _i, _len, _ref;
        for (_i = 0, _len = url_patterns.length; _i < _len; _i++) {
            _ref = url_patterns[_i], name = _ref[0], pattern = _ref[1];
            self_url_patterns[name] = pattern;
            url = _get_url(name);
            Urls[name.replace(/[-_]+(.)/g, function (_m, p1) {
                return p1.toUpperCase();
            })] = url;
            Urls[name.replace(/-/g, '_')] = url;
            Urls[name] = url;
        }
        return Urls;
    }

    return data ? factory(data) : factory;
})();
