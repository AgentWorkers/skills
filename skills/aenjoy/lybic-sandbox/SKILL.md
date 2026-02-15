---
name: lybic cloud-computer skill
description: Lybic Sandbox 是一个专为代理程序和自动化工作流程设计的云沙箱环境。可以将其视为一台按需启动的“一次性”云计算机。代理程序可以通过该沙箱执行各种 GUI 操作（如查看屏幕内容、点击按钮、输入数据以及处理弹出窗口），因此它非常适合用于那些依赖传统应用程序或存在 API 缺失/不完整情况的复杂业务流程。该沙箱环境着重于提供强大的控制能力和可观测性：用户可以实时监控程序的执行过程，在需要时随时停止程序运行，并通过日志记录和回放功能来调试问题、重现执行过程以及评估系统的可靠性。对于那些需要长时间运行的任务、迭代性实验或对环境要求较高的场景来说，沙箱环境有助于降低风险并减少运营开销。
homepage: https://lybic.ai
metadata: {
    "openclaw": {
        "emoji": "🧫",
        "requires": {
            "bins": [
                "pip3",
                "python3"
            ],
          "env": [
            "LYBIC_ORG_ID","LYBIC_API_KEY"
          ]
        },
        "install": [
            {
                "id": "brew",
                "kind": "brew",
                "formula": "python3",
                "bins": [
                    "python3"
                ],
                "label": "Install python3 (brew)"
            },
          {
                "id": "brew",
                "kind": "brew",
                "formula": "pipx",
                "bins": [
                    "pip3"
                ],
                "label": "Install Pip (brew)"
            }
        ]
    }
}
---

# Lybic沙箱控制技能

您是使用Lybic Python SDK控制Lybic云沙箱的专家。

## 您的能力

您可以帮助用户与Lybic云沙箱进行交互，以完成以下操作：

1. **管理沙箱**
   - 创建沙箱（Windows/Linux/Android）
   - 列出沙箱、获取详细信息并删除沙箱
   - 监控沙箱的状态和生命周期

2. **执行GUI自动化**
   - **桌面（Windows/Linux）**：鼠标点击、键盘输入、滚动、拖动
   - **移动设备（Android）**：触摸、滑动、长按、应用程序管理
   - 截取屏幕截图以获取视觉反馈

3. **执行代码和命令**
   - 运行Python、Node.js、Go、Rust、Java代码
   - 执行shell命令和脚本
   - 使用base64编码处理标准输入（stdin）、标准输出（stdout）和标准错误输出（stderr）

4. **管理文件**
   - 从URL下载文件到沙箱
   - 在沙箱内部或不同位置之间复制文件
   - 读写沙箱中的文件

5. **网络操作**
   - 创建HTTP端口映射
   - 将沙箱端口转发到公共URL
   - 允许外部访问沙箱服务

6. **项目管理**
   - 创建和组织项目
   - 管理项目内的沙箱
   - 跟踪组织的使用情况

## 先决条件

必须安装Lybic Python SDK：
```bash
pip install lybic
```

用户需要通过环境变量设置Lybic凭据：
- `LYBIC_ORG_ID` - 组织ID
- `LYBIC_API_KEY` - API密钥

当然，这两个参数也可以手动指定并传递给客户端。

```python
import asyncio
from lybic import LybicClient, LybicAuth

async def main():
    async with LybicClient(LybicAuth(
            org_id="your_org_id", # Lybic organization ID
            api_key="your_api_key"
         )) as client:
        # Your code here
        pass
```

## 代码规范

### 1. 始终使用async/await模式

```python
import asyncio
from lybic import LybicClient

async def main():
    async with LybicClient() as client:
        # Your code here
        pass

if __name__ == '__main__':
    asyncio.run(main())
```

### 2. 使用适当的错误处理

```python
try:
    result = await client.sandbox.create(name="test", shape="beijing-2c-4g-cpu-linux")
    print(f"Created: {result.id}")
except Exception as e:
    print(f"Error: {e}")
```

### 3. 处理基于base64的进程I/O操作

```python
import base64

# For stdin
code = "print('hello')"
stdin_b64 = base64.b64encode(code.encode()).decode()

# For stdout/stderr
result = await client.sandbox.execute_process(...)
output = base64.b64decode(result.stdoutBase64 or '').decode()
```

### 4. 在GUI操作中使用分数坐标

```python
# Recommended: Resolution-independent
action = {
    "type": "mouse:click",
    "x": {"type": "/", "numerator": 1, "denominator": 2},  # 50%
    "y": {"type": "/", "numerator": 1, "denominator": 2},  # 50%
    "button": 1
}

# Alternative: Absolute pixels (less portable)
action = {
    "type": "mouse:click",
    "x": {"type": "px", "value": 500},
    "y": {"type": "px", "value": 300},
    "button": 1
}
```

## 常见模式

### 模式1：创建沙箱并运行代码

```python
import asyncio
import base64
from lybic import LybicClient

async def run_code_in_sandbox():
    async with LybicClient() as client:
        # Create linux based code sandbox
        sandbox = await client.sandbox.create(
            name="code-runner",
            shape="beijing-2c-4g-cpu-linux"
        )
        
        # Execute code
        code = "print('Hello from sandbox')"
        result = await client.sandbox.execute_process(
            sandbox.id,
            executable="python3",
            stdinBase64=base64.b64encode(code.encode()).decode()
        )
        
        print(base64.b64decode(result.stdoutBase64).decode())
        
        # Cleanup
        await client.sandbox.delete(sandbox.id)

asyncio.run(run_code_in_sandbox())
```

### 模式2：带有截图的GUI自动化

```python
import asyncio
from lybic import LybicClient

async def automate_gui():
    async with LybicClient() as client:
        sandbox_id = "SBX-xxxx"
        
        # Take initial screenshot
        url, img, _ = await client.sandbox.get_screenshot(sandbox_id)
        img.show()
        
        # Click at center
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "mouse:click",
                "x": {"type": "/", "numerator": 1, "denominator": 2},
                "y": {"type": "/", "numerator": 1, "denominator": 2},
                "button": 1
            }
        )
        
        # Type text
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "keyboard:type",
                "content": "Hello!"
            }
        )
        
        # Press Enter
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "keyboard:hotkey",
                "keys": "Return"
            }
        )

asyncio.run(automate_gui())
```

### 模式3：下载文件并处理文件

```python
import asyncio
import base64
from lybic import LybicClient
from lybic.dto import FileCopyItem, HttpGetLocation, SandboxFileLocation

async def download_and_process():
    async with LybicClient() as client:
        sandbox_id = "SBX-xxxx"
        
        # Download file
        await client.sandbox.copy_files(
            sandbox_id,
            files=[
                FileCopyItem(
                    id="dataset",
                    src=HttpGetLocation(url="https://example.com/data.csv"),
                    dest=SandboxFileLocation(path="/tmp/data.csv")
                )
            ]
        )
        
        # Process with Python
        code = """
import pandas as pd
df = pd.read_csv('/tmp/data.csv')
print(df.describe())
"""
        result = await client.sandbox.execute_process(
            sandbox_id,
            executable="python3",
            stdinBase64=base64.b64encode(code.encode()).decode()
        )
        
        print(base64.b64decode(result.stdoutBase64).decode())

asyncio.run(download_and_process())
```

## 操作参考

### 鼠标操作（适用于计算机）

```python
# Click
{"type": "mouse:click", "x": {...}, "y": {...}, "button": 1}  # 1=left, 2=right

# Double-click
{"type": "mouse:doubleClick", "x": {...}, "y": {...}, "button": 1}

# Move
{"type": "mouse:move", "x": {...}, "y": {...}}

# Drag
{"type": "mouse:drag", "startX": {...}, "startY": {...}, "endX": {...}, "endY": {...}}

# Scroll
{"type": "mouse:scroll", "x": {...}, "y": {...}, "stepVertical": -5, "stepHorizontal": 0}
```

### 键盘操作（适用于计算机）

```python
# Type text
{"type": "keyboard:type", "content": "Hello, World!"}

# Hotkey
{"type": "keyboard:hotkey", "keys": "ctrl+c"}  # Copy
{"type": "keyboard:hotkey", "keys": "Return"}  # Enter
{"type": "keyboard:hotkey", "keys": "ctrl+shift+s"}  # Save as
```

### 触摸操作（适用于移动设备）

```python
# Tap
{"type": "touch:tap", "x": {...}, "y": {...}}

# Long press
{"type": "touch:longPress", "x": {...}, "y": {...}, "duration": 2000}

# Swipe
{"type": "touch:swipe", "x": {...}, "y": {...}, "direction": "up", "distance": {...}}

# Android buttons
{"type": "android:back"}
{"type": "android:home"}
```

### 应用程序管理（适用于移动设备）

```python
# Start app
{"type": "os:startApp", "packageName": "com.android.chrome"}
{"type": "os:startAppByName", "name": "Chrome"}

# Close app
{"type": "os:closeApp", "packageName": "com.android.chrome"}
{"type": "os:closeAppByName", "name": "Chrome"}

# List apps
{"type": "os:listApps"}
```

### 常见操作

```python
# Screenshot
{"type": "screenshot"}

# Wait
{"type": "wait", "duration": 3000}  # milliseconds

# Task status
{"type": "finished", "message": "Task completed"}
{"type": "failed", "message": "Error occurred"}
```

## 最佳实践

1. **使用分数坐标**：在不同屏幕分辨率下更具便携性
2. **截取屏幕截图**：帮助验证操作前后的GUI状态
3. **处理错误**：始终将API调用封装在try-except块中
4. **清理资源**：完成后删除沙箱以避免产生费用
5. **对I/O进行base64编码**：记得使用base64编码处理标准输入和输出
6. **检查退出代码**：使用`exitCode`来验证进程是否成功（0 = 成功）

## 沙箱类型

Lybic在创建沙箱时会通过`shape`参数确定云沙箱的操作系统类型：

- Windows: beijing-2c-4g-cpu
- Linux: beijing-2c-4g-cpu-linux
- Android: acep-shenzhen-enhanced 或 acep-wenzhou-common-pro

## 故障排除

1. **沙箱未准备好**：创建后请稍等片刻，使用`get()`检查状态
2. **操作失败**：确认坐标在屏幕范围内
3. **进程超时**：长时间运行的进程需要特殊处理（请参阅文档）
4. **文件未找到**：在访问之前确保路径存在于沙箱中
5. **导入错误**：确认包已预先安装，或使用`pip3 install`进行安装

## 何时使用此技能

当用户需要以下操作时，请使用此技能：
- 在隔离的云环境中运行代码
- 自动化GUI应用程序（桌面或移动设备）
- 在沙箱中测试Web服务
- 在干净的环境中处理数据
- 远程交互应用程序
- 执行浏览器自动化
- 在Android设备上测试移动应用程序

## 文档

有关详细的API参考，请参阅：
- [Python SDK文档](https://docs.lybic.cn/en/sdk/python)
- [Action Space文档](https://docs.lybic.cn/en/sandbox/action)
- [代码执行文档](https://docs.lybic.cn/en/sandbox/code)

## 注意事项

- 在运行代码之前，请始终检查凭据是否已设置
- 清晰地解释代码的功能
- 提供完整的示例代码
- 优雅地处理错误
- 在适当的时候清理资源（删除沙箱）
- 截取屏幕截图以验证GUI操作的结果
- 一致地使用async/await模式