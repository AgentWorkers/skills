---
name: orgo-desktop-control
description: 使用 `orgo_client` Python SDK 来配置和管理 Orgo 云服务器。该 SDK 可用于启动远程桌面、自动化浏览器操作、远程执行 Bash/Python 脚本、与用户界面进行交互、管理文件以及控制流媒体服务。
compatibility: Requires internet access and ORGO_API_KEY.
metadata:
  author: custom
  version: "1.0.0"
---
# Orgo桌面控制技能（Python SDK）

该技能使用`orgo_client.py`来安全地创建和管理Orgo云服务器。

**务必使用SDK**，切勿手动构造HTTP请求。

---

# 适用场景

在用户需要以下操作时激活该技能：
- 启动远程桌面
- 自动化浏览器或用户界面操作
- 执行点击、拖拽、输入、滚动等操作
- 远程执行bash命令或Python脚本
- 截取屏幕截图
- 上传/导出文件
- 启动/停止/重启虚拟机环境
- 流式传输桌面输出
- 访问VNC登录凭据
- 创建用于操作虚拟机的代理程序

**注意：** 该技能不适用于仅用于本地运行的代码。

---

# 高级工作流程

1. 实例化客户端
2. 确保工作区存在
3. 创建新的虚拟机
4. 调用`wait_until_ready()`方法等待虚拟机准备就绪
5. 执行所需操作
6. 导出操作结果
7. 停止虚拟机

---

# 初始化

```python
from orgo_client import OrgoClient

client = OrgoClient(api_key=os.environ["ORGO_API_KEY"])
```

---

# 工作区管理

- **创建工作区**：```python
ws = client.create_workspace("browser-agent")
```
- **列出工作区**：```python
client.list_workspaces()
```
- **强制删除工作区**：```python
client.delete_workspace(ws.id, force=True)
```
**请勿在未经用户明确确认的情况下删除工作区。**

---

# 虚拟机生命周期管理

- **创建虚拟机**：```python
computer = client.create_computer(
    workspace_id=ws.id,
    name="agent-1",
    ram=4,
    cpu=2,
    wait_until_ready=True
)
```
- **手动等待虚拟机启动**：```python
computer.start()
computer.stop()
computer.restart()
```
- **启动/停止/重启虚拟机**：```python
computer.start()
computer.stop()
computer.restart()
```
- **删除虚拟机**（操作不可逆）：```python
computer.delete(force=True)
```
**虚拟机处于空闲状态时务必将其关闭。**

---

# 用户界面交互

- **点击**：```python
computer.click(100, 200)
```
- **右键点击**：```python
computer.right_click(100, 200)
```
- **双击**：```python
computer.double_click(100, 200)
```
- **拖拽**：```python
computer.drag(100, 200, 400, 500)
```
- **滚动**：```python
computer.scroll("down", amount=3)
```
- **输入文本**：```python
computer.type("Hello world")
```
- **按键盘键**：```python
computer.key("Enter")
computer.key("ctrl+c")
```
- **等待操作完成**：```python
computer.wait(2.0)
```

---

# 屏幕截图

- **截取屏幕截图**：```python
img_b64 = computer.screenshot()
```
- **将截图保存到文件**：```python
computer.save_screenshot("screen.png")
```

---

# 命令执行

- **执行bash命令**：```python
result = computer.run_bash("ls -la")
print(result.output)
```
- **执行Python脚本**：```python
result = computer.run_python("print('hi')")
```
**所有错误都会自动引发相应的OrgoError子类。**

---

# 数据流传输

- **开始数据流传输**：```python
computer.stream_start("my-rtmp-connection")
```
- **查看数据流状态**：```python
computer.stream_status()
```
- **停止数据流传输**：```python
computer.stream_stop()
```

---

# VNC连接

- **配置VNC连接**：```python
password = computer.vnc_password()
```

---

# 文件操作

- **上传文件到虚拟机**：```python
client.upload_file("local.txt", ws.id, computer_id=computer.id)
```
- **从虚拟机导出文件**：```python
file_record, url = computer.export_file("Desktop/output.txt")
```
- **列出虚拟机中的文件**：```python
computer.list_files(ws.id)
```
- **删除文件**：```python
client.delete_file(file_id)
```

---

# 错误处理

所有错误都会以特定的异常类型抛出：
- `OrgoAuthError`
- `OrgoForbiddenError`
- `OrgoNotFoundError`
- `Orgo.BadRequestError`
- `OrgoServerError`
- `OrgoTimeoutError`
- `OrgoConfirmationError`

**对于可能造成数据丢失的操作，请务必用户明确确认后再执行。**

## 推荐的自动化流程

对于涉及用户界面的操作：
1. 截取屏幕截图
2. 分析当前界面状态
3. 执行点击、输入或拖拽等操作
4. 等待操作完成
5. 再次截取屏幕截图
6. 重复上述步骤

**请注意：** 用户界面的状态可能会发生变化，因此不要依赖之前的截图结果。

---

# 提高效率的建议

- **尽量减少内存和CPU的使用**  
- 如果后续还需要继续操作，建议直接停止虚拟机而不是直接删除它  
- 使用`wait_until_ready()`方法代替手动轮询  
- 避免不必要的屏幕截图  
- 在可能的情况下，优先使用bash命令而非直接操作用户界面  

---

# 技能结束