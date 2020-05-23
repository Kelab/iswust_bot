import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  cssModulesTypescriptLoader: {},
  esbuild: {},
  ignoreMomentLocale: true,
  title: 'Nonebot',
  routes: [
    { path: '/login', component: '@/pages/Login', title: 'Login' },
    { path: '/user', component: '@/pages/UserCenter', title: 'UserCenter' },
  ],
});
