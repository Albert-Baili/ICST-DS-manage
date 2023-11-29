/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const nestedRouter = {
  path: '/nested',
  component: Layout,
  redirect: '/nested/menu1/menu1-1',
  name: 'Nested',
  meta: {
    title: '隧道管理',
    icon: 'nested'
  },
  children: [
    {
      path: 'newtunnel',
      name: 'newtunnel',
      component: () => import('@/views/nested/newtunnel/index'),
      meta: { title: '新建隧道' }
    },
    {
      path: 'tunnelList',
      name: 'tunnelList',
      component: () => import('@/views/nested/tunnelList/index'),
      meta: { title: '隧道列表' }
    }
  ]
}

export default nestedRouter
