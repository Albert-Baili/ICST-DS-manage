import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* Router Modules */
/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'           
 *     the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: '主页',
        meta: { title: '主页', icon: 'dashboard', affix: true }
      }
    ]
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: 'Profile', icon: 'user', noCache: true }
      }
    ]
  },
  
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  // {
  //   path: '/certmanage',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '/certmanage',
  //       component: () => import('@/views/certmanage/index'),
  //       name: 'certmanage',
  //       meta: { title: '证书管理', icon: 'icon', noCache: true }
  //     }
  //   ]
  // },
  {
    path: '/assetManage',
    component: Layout,
    meta: {
      title: '数据资产管理',
      icon: 'chart'
    },
    children: [
      {
        path: '/assetManage/authority/',
        component: () => import('@/views/assetManage/authority/index'),
        name: 'authority',
        meta: { title: '资产权限管理', icon: 'icon', noCache: true }
      },
      {
        path: '/assetManage/map/',
        component: () => import('@/views/assetManage/map/index'),
        name: 'map',
        meta: { title: '资产地图目录', icon: 'icon', noCache: true }
      },
      {
        path: '/assetManage/backup/',
        component: () => import('@/views/assetManage/backup/index'),
        name: 'backup',
        meta: { title: '资产备份恢复', icon: 'icon', noCache: true }
      }
    ]
  },
  {
    path: '/DataQuality',
    component: Layout,
    meta: {
      title: '数据隐私保护',
      icon: 'chart'
    },
    children: [
      {
        path: '/DataQuality/desensi/',
        component: () => import('@/views/DataQuality/desensi/index'),
        name: 'DataQuality',
        meta: { title: '数据识别', icon: 'icon', noCache: true }
      },
      {
        path: '/DataQuality/quality/',
        component: () => import('@/views/DataQuality/quality/index'),
        name: 'DataQuality',
        meta: { title: '数据治理', icon: 'icon', noCache: true }
      }
    ]
  },
  {
    path: '/riskMonitor',
    component: Layout,
    meta: {
      title: '数据风险监测',
      icon: 'chart'
    },
    children: [
      {
        path: '/riskMonitor/log',
        component: () => import('@/views/riskMonitor/log/index'),
        name: 'log',
        meta: { title: '日志监控审计', icon: 'message', noCache: true }
      },
      {
        path: '/riskMonitor/trans',
        component: () => import('@/views/riskMonitor/trans/index'),
        name: 'trans',
        meta: { title: '数据传输加密', icon: 'icon', noCache: true}
      },
      {
        path: '/riskMonitor/access',
        component: () => import('@/views/riskMonitor/access/index'),
        name: 'access',
        meta: { title: '访问控制管理', icon: 'icon', noCache: true}
      }
    ]
  },
  // {
  //   path: '/permission',
  //   component: Layout,
  //   redirect: '/permission/page',
  //   alwaysShow: true, // will always show the root menu
  //   name: 'Permission',
  //   meta: {
  //     title: 'Permission',
  //     icon: 'lock',
  //     roles: ['admin', 'editor'] // you can set roles in root nav
  //   },
  //   children: [
  //     {
  //       path: 'page',
  //       component: () => import('@/views/permission/page'),
  //       name: 'PagePermission',
  //       meta: {
  //         title: 'Page Permission',
  //         roles: ['admin'] // or you can only set roles in sub nav
  //       }
  //     },
  //     {
  //       path: 'directive',
  //       component: () => import('@/views/permission/directive'),
  //       name: 'DirectivePermission',
  //       meta: {
  //         title: 'Directive Permission'
  //         // if do not set roles, means: this page does not require permission
  //       }
  //     },
  //     {
  //       path: 'role',
  //       component: () => import('@/views/permission/role'),
  //       name: 'RolePermission',
  //       meta: {
  //         title: 'Role Permission',
  //         roles: ['admin']
  //       }
  //     }
  //   ]
  // },

  {
    path: '/icon',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/views/icons/index'),
        name: 'Icons',
        meta: { title: 'Icons', icon: 'icon', noCache: true }
      }
    ]
  },

  /** when your routing map is too long, you can split it into small modules **/
  // componentsRouter,
  // chartsRouter,

  // tableRouter,

  

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'hash',
  // mode: 'browserHistory',
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
