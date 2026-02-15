---
name: Gradio
description: 构建并部署具有适当状态管理、队列处理以及生产模式功能的机器学习演示接口。
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# Gradio 模式

## 接口（Interface）与组件块（Blocks）
- `gr.Interface` 适用于单功能演示；对于包含多个步骤、条件性用户界面或自定义布局的场景，请使用 `grBlocks`。
- 组件块提供了 `.click()`、`.change()`、`.submit()` 等事件处理函数，而接口仅支持单一功能。
- 将接口嵌入组件块中虽然可行，但可能导致状态混乱——每个应用程序应选择一种模式。

## 状态管理（State Management）
- `gr.State()` 创建会话级别的状态数据——用户刷新页面时状态会被重置。
- 状态值必须能够被序列化为 JSON 格式；否则 Gradio 会自动忽略这些值。请确保使用可序列化的自定义类。
- 要持久化状态变化，需要将状态值同时作为输入和输出传递给函数：`fn(state) -> state`。忽略输出会导致状态更新丢失。
- 全局变量可能在多个用户间共享，从而引发竞态条件——请始终使用 `gr.State()` 来存储用户特定的数据。

## 队列与并发（Queue and Concurrency）
- 如果未使用 `.queue()`，长时间运行的函数会阻塞其他用户的使用。请在调用 `.launch()` 之前先调用 `demo.queue()`。
- 设置 `concurrency_limit=1` 可限制函数的并发调用次数（适用于无法并行执行的 GPU 计算任务）。
- `max_size` 用于限制队列中的等待请求数量；否则在高负载下内存可能会无限增长。
- 使用 `yield` 的生成器函数可以实现数据流式传输，但它们会占用一个队列位置直到执行完毕。

## 文件处理（File Handling）
- 上传的文件是临时路径，请求结束后会被删除；如需保留文件内容，请自行复制。
- `gr.File(type="binary")` 返回字节数据，`type="filepath"` 返回文件路径字符串——类型不匹配会导致程序异常。
- 对于下载功能，应返回 `gr.File(value="path/to/file")`，而不是原始字节数据；组件会自动处理内容分发相关的头部信息。
- 文件上传默认限制为 200MB；可以通过 `launch()` 中的 `max_file_size` 参数进行调整。

## 组件使用注意事项（Component Usage）
- 如果 `gr.Dropdown(value=None)` 且 `allow_custom_value=False`，用户未输入任何内容时会引发错误——请设置默认值或使该字段可选。
- `gr.Image(type="pil")` 返回 PIL 图像对象，`type="numpy"` 返回 NumPy 数组，`type="filepath"` 返回文件路径——不匹配的输入会导致函数执行失败。
- `gr.Chatbot` 需要接收形如 `[(user, bot), ...]` 的元组列表作为输入；仅返回字符串会导致无法正常显示聊天内容。
- 即使将组件设置为 `visible=False`，它们仍会执行其功能——使用 `gr.update(interactive=False)` 可以禁用组件而不隐藏它们。

## 认证（Authentication）
- `auth=("user", "pass")` 是明文密码，不适合生产环境——请使用 `auth=auth_function` 并加入适当的身份验证逻辑。
- 认证机制适用于整个应用程序；除非使用自定义中间件，否则无法为特定路由或组件设置单独的认证机制。
- 即使启用了 `share=True`，认证信息仍可能被 Gradio 服务器暴露——对于敏感应用，请使用自己的安全传输通道。

## 部署（Deployment）
- 设置 `share=True` 可通过 Gradio 服务器生成一个有效期为 72 小时的公共 URL——仅适用于演示用途，不适合生产环境。
- 本地开发环境中的环境变量在 Hugging Face Spaces 中不可用——请使用 Spaces 的秘密设置或设置界面进行配置。
- 设置 `server_name="0.0.0.0"` 可接受外部连接；默认的 `127.0.0.1` 仅允许本地访问。
- 如果应用程序位于反向代理后端，请设置 `root_path="/subpath"`，否则资源文件和 API 路由可能会出问题。

## 事件与更新（Events and Updates）
- 使用 `gr.update(value=x, visible=True)` 可修改组件属性；仅返回值不会触发更新。
- 使用 `.then()` 连接多个事件以实现顺序操作；并行执行的 `.click()` 事件处理函数可能会导致竞争问题。
- `every=5` 表示函数每 5 秒执行一次；但这样会保持连接打开状态，请谨慎调整频率。
- 设置 `trigger_mode="once` 可防止用户重复点击同一按钮时触发多次操作。

## 性能优化（Performance）
- `cache_examples=True` 可在启动时预计算示例输出结果，加快演示速度，但会增加程序启动时间。
- 如果函数中加载大型模型，每次请求都会重新加载模型数据——建议将模型数据存储在全局变量中或使用 `gr.State` 进行初始化。
- `batch=True` 与 `max_batch_size=N` 可合并并发请求，提高 GPU 的处理效率。