const {
  override,
  fixBabelImports,
  addLessLoader,
  useEslintRc,
  addBundleVisualizer,
  useBabelRc,
  addWebpackExternals,
} = require('customize-cra');

module.exports = override(
  fixBabelImports('import', {
    libraryName: 'antd-mobile',
    libraryDirectory: 'es',
    style: true,
  }),
  addLessLoader({
    javascriptEnabled: true,
  }),
  useEslintRc('.eslintrc'),
  useBabelRc('.babelrc')
);
