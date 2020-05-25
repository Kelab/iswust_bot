module.exports = {
  host: "localhost",
  title: "小科",
  description: "基于自然语言处理的高校教务 QQ 助手",
  markdown: {
    lineNumbers: true
  },
  plugins: [
    [
      "@vuepress/register-components",
      {
        componentDir: "components"
      }
    ]
  ],
  head: [
    ["link", { rel: "icon", href: `/logo.png` }],
    ["meta", { name: "theme-color", content: "#ffffff" }]
  ],
  themeConfig: {
    repo: "BudyLab/iswust_bot",
    docsDir: "docs",
    editLinks: true,
    editLinkText: "在 GitHub 上编辑此页",
    lastUpdated: "上次更新",
    activeHeaderLinks: false,
    nav: [{ text: "帮助", link: "/guide/" }],
    sidebar: {
      "/guide/": [
        {
          title: "帮助",
          collapsable: false,
          children: [
            "",
            "bind",
            "code_runner",
            "course_schedule",
            "credit",
            "ecard",
            "hitokoto",
            "remind",
            "rss",
            "score",
            "subscribe"
          ]
        }
      ]
    }
  }
};
