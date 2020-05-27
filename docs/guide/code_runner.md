# 运行代码

<Terminal :content="[
  { content: [{ text: 'plugin_name: ', class: 'input' }, '运行代码'] },
  { content: [{ text: 'command: ', class: 'input' }, ' run'] },
]" static></Terminal>

<panel-view title="聊天记录">
  <chat-message nickname="Artin" color="#3e484e">run python<br/>print("Hello 小科")
</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">正在运行，请稍等……</chat-message>
  <chat-message nickname="小科" avatar="/logo.jpg">stdout:<br/>Hello 小科</chat-message>
</panel-view>

- __plugin_name:__ 运行代码
- __plugin_short_description:__ 命令: run
- __plugin_usage:__
  - 运行代码可以输入以下命令，然后根据提示输入即可：
    - code_runner
    - run
    - 执行代码
    - 运行
    - 运行代码

  你也可以直接在后面加上相关内容，如：
  
    ```py
    run python
    print(1234)
    ```
