import { defineConfig } from 'umi';

export default defineConfig({
  layout: {
    name: 'Nonebot',
  },
  nodeModulesTransform: {
    type: 'none',
  },
  cssModulesTypescriptLoader: {},
  esbuild: {},
  antd: {
    compact: true,
  },
  ignoreMomentLocale: true,
  routes: [{ path: '/', component: '@/pages/index' }],
});
