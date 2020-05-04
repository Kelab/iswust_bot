import { defineConfig } from 'umi';

export default defineConfig({
  layout: {
    name: 'Nonebot',
  },
  nodeModulesTransform: {
    type: 'none',
  },
  cssModulesTypescriptLoader: {},
  antd: {
    compact: true,
  },
  routes: [{ path: '/', component: '@/pages/index' }],
});
