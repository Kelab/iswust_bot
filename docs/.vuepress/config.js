module.exports = {
  host: "localhost",
  title: "小科 - 基于自然语言处理的 QQ 教务机器人",
  description: "基于自然语言处理的 QQ 教务机器人",
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
          collapsable: true,
          children: [""]
        },
        {
          title: "教务相关",
          collapsable: false,
          children: [
            "bind",
            "course_schedule",
            "credit",
            "ecard",
            "score",
            "subscribe"
          ]
        },
        {
          title: "效率相关",
          collapsable: false,
          children: ["remind", "code_runner", "rss"]
        },
        {
          title: "其他",
          collapsable: false,
          children: ["hitokoto"]
        }
      ]
    }
  }
};
