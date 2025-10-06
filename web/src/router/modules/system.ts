import { $t } from "@/plugins/i18n";
import { system } from "@/router/enums";

export default {
  path: "/system",
  redirect: "/system/user",
  meta: {
    icon: "ri:settings-3-line",
    title: $t("menus.pureSystem"),
    rank: system
  },
  children: [
    {
      path: "/system/user",
      name: "SystemUser",
      component: () => import("@/views/system/user/index.vue"),
      meta: {
        title: $t("menus.pureUser")
      }
    },
    {
      path: "/system/role",
      name: "SystemRole",
      component: () => import("@/views/system/role/index.vue"),
      meta: {
        title: $t("menus.pureRole")
      }
    },
    {
      path: "/system/menu",
      name: "SystemMenu",
      component: () => import("@/views/system/menu/index.vue"),
      meta: {
        title: $t("menus.pureMenuManagement")
      }
    },
    {
      path: "/system/dept",
      name: "SystemDept",
      component: () => import("@/views/system/dept/index.vue"),
      meta: {
        title: $t("menus.pureDept")
      }
    },
    {
      path: "/system/test-user",
      name: "TestUser",
      component: () => import("@/views/testuser/index.vue"),
      meta: {
        title: "测试用户管理"
      }
    }
  ]
} satisfies RouteConfigsTable;
