# ⏰ 提醒

<panel-view title="自然语言创建提醒">
  <chat-message nickname="Artin" color="#3e484e">今晚八点半提醒我跑步</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">
  
好哦！我会在2020-05-27 20:30:00准时叫你跑步~

提醒创建成功：  
\> 提醒时间：2020-05-27 20:30:00  
\> 内容：跑步  

  </chat-message>

  <center style="user-select:none;font-size:14px;color:#7f7f7f">20:30:00</center>

  <window-jitte  nickname="小科" />
  <chat-message nickname="小科" avatar="/logo.jpg">
  
提醒通知：  
你定下的提醒时间已经到啦！快跑步吧！

  </chat-message>
</panel-view>

<panel-view title="交互式多轮创建提醒">
  <chat-message nickname="Artin" color="#3e484e">新建提醒</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">你想让我提醒什么内容呢？语句命令都可，输入 `取消、不` 等来取消</chat-message>
  <chat-message nickname="Artin" color="#3e484e">今天课表</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">你希望我在每天的什么时候给你提醒呢？</chat-message>
  <chat-message nickname="Artin" color="#3e484e">早上七点半</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">添加提醒成功啦，下次提醒时间 2020-05-28 07:30</chat-message>
</panel-view>

- __plugin_name:__ ⏰ 提醒
- __plugin_short_description:__ [原 push]命令：remind
- __plugin_usage:__
  - 新建提醒输入：
    - remind
    - 提醒
    - 添加提醒
    - 新增提醒
    - 新建提醒

  - 查看提醒可以输入：
    - remind.show
    - 查看提醒
    - 我的提醒
    - 提醒列表

  - 删除提醒：
    - remind.rm
    - 取消提醒
    - 停止提醒
    - 关闭提醒
    - 删除提醒
