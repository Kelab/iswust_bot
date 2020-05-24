module.exports = {
  title: "小科",
  description: "基于自然语言处理的高校教务 QQ 助手",
  markdown: {
    lineNumbers: true
  },
  head: [
    ["link", { rel: "icon", href: `/logo.png` }],
    ["meta", { name: "theme-color", content: "#ffffff" }],
    ["meta", { name: "msapplication-TileColor", content: "#00aba9" }]
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
          title: "指南",
          collapsable: false,
          children: [
            "",
            "installation",
            "getting-started",
            "whats-happened",
            "basic-configuration",
            "command",
            "nl-processor",
            "tuling",
            "notice-and-request",
            "cqhttp",
            "scheduler",
            "usage",
            "whats-next"
          ]
        }
      ]
    }
  }
};
