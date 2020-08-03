module.exports = {
  host: "localhost",
  title: "小科 - QQ 教务机器人",
  description: "QQ 教务机器人",
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
    nav: [
      { text: "使用", link: "/guide/" },
      {
        text: "部署",
        link: "/deploy/"
      }
    ],
    sidebar: {
      "/guide/": [
        {
          title: "开始使用",
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
      ],
      "/deploy/": [
        {
          title: "总览",
          collapsable: false,
          children: ["", "update"]
        },
        {
          title: "配置项",
          collapsable: false,
          children: ["set-env", "set-qq"]
        }
      ]
    }
  }
};
