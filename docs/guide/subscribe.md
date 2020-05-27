# 订阅

::: tip 提示
这部分可以在 **个人中心网页版** 操作哦~
:::

<panel-view title="聊天记录">
  <chat-message nickname="Artin" color="#3e484e">订阅</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">

你想订阅什么内容呢？（请输入序号，也可输入 \`取消、不\` 等语句取消）：  
r0. 教务处新闻  
r1. 教务处通知 创新创业教育  
r2. 教务处通知 学生学业  
<-- 此处省略 -->  
r10. 计科学院通知 教研动态  
s0. 有新成绩出来时提醒我  
s1. 有新考试出来提醒我  

  </chat-message>
  <chat-message nickname="Artin" color="#3e484e">r3</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">西南科技大学教务处 建设与改革 订阅成功~</chat-message>
    <center style="user-select:none;font-size:14px;color:#7f7f7f">某时某刻</center>
  <chat-message nickname="小科" avatar="/logo.jpg">

【西南科技大学教务处 建设与改革】有更新：  
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-  
标题：标题  
链接：<a>http://example.com</a>  
日期：2020-XX-XX XX:XX:XX  

  </chat-message>
</panel-view>


- __plugin_name:__ 订阅
- __plugin_short_description:__ 订阅 通知/成绩/考试 等，命令： subscribe
- __plugin_usage:__ 
  - 添加订阅：
    - 订阅
    - 添加订阅
    - 新建订阅
    - subscribe  
然后会提示输入序号，你也可以直接在后面加上序号，如：
    - 订阅 1
  - 查看订阅：
    - 查看订阅
    - 订阅列表
    - subscribe show

  - 移除订阅：
    - 移除订阅
    - 取消订阅
    - 停止订阅
    - 删除订阅
    - subscribe rm
    然后会提示输入序号，你也可以直接在后面加上序号，如：
      - 移除订阅 1
      - 移除订阅 all
