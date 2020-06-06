import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  cssModulesTypescriptLoader: {},
  esbuild: {},
  dynamicImport: {
    loading: '@/components/Loading',
  },
  ignoreMomentLocale: true,
  title: '小科',
  routes: [
    {
      path: '/',
      component: '@/pages/index',
      routes: [
        { path: '/login', component: '@/pages/Login', title: 'Login' },
        { path: '/user', component: '@/pages/UserCenter', title: 'UserCenter' },
      ],
    },
  ],
  define: {
    API_URL: process.env['API_URL'],
  },
});
