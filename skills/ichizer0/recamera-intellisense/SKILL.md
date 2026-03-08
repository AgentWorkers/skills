---
name: recamera-intellisense
description: >
  **reCamera** 的主要功能包括：  
  1. 注册新的摄像头设备；  
  2. 配置 AI 检测模型、规则或调度方案；  
  3. 监控并清除检测事件；  
  4. 获取事件快照；  
  5. 执行手动图像/视频捕获操作。  
  该工具通过本地 Python CLI 脚本进行交互，并使用 JSON 格式进行数据输入/输出。  
  **触发时机包括：**  
  - 摄像头接入系统时；  
  - 检测配置完成时；  
  - 定期检测任务执行时；  
  - 快照捕获需求发生时；  
  - 手动执行摄像头自动化操作时。
metadata: {
  "openclaw": {
    "emoji": "📷",
    "requires": {
      "bins":["python3"],
      "config_paths":["~/.recamera/devices.json"]
    }
  }
}
user-invocable: true
---
# reCamera 智能辅助工具

## 必备条件

- Python 3（无需安装外部包）
- 可访问的 reCamera HTTP API（默认端口为 80）
- 认证信息存储在 `~/.recamera/devices.json` 文件中（该文件会自动生成，并在技能元数据中指定）

## 安全注意事项

- **认证信息存储**：设备令牌保存在 `~/.recamera/devices.json` 文件中。请使用适当的权限（`chmod 600`）保护该文件，切勿在其中存储其他敏感信息。
- **明文传输**：与设备的通信默认使用 HTTP 协议（端口 80），数据（包括图像和令牌）以明文形式传输。在不可信的网络环境中，请为设备配置 HTTPS。
- **仅限可信网络使用**：该工具会定期查询设备并下载快照/图像文件。请确保仅在可信赖的网络环境中使用该工具。
- **设备专用令牌**：请为每个设备使用唯一的令牌（格式为 `sk_xxx`），切勿重复使用与云服务共享的令牌。
- **代码审查**：该工具的源代码位于 `scripts/` 目录下。在允许工具自动执行之前，请仔细审查代码以确保其行为符合您的预期。

## 脚本

所有脚本均位于 `{baseDir}/scripts` 目录下，它们接受一个 JSON 对象作为命令行参数（`detect_local_device` 和 `list_devices` 命令可省略此参数）：

- `device_manager.py`：用于添加/更新/删除/查询设备信息以及下载文件。
- `detection_manager.py`：负责模型管理、任务调度、规则设置以及事件处理和事件相关图像的获取。
- `capture_manager.py`：用于控制图像捕获的状态（开始/停止）以及单次图像的捕获。

**完整的 API 接口文档和命令行参数格式**：请参阅 [REFERENCE.md](REFERENCE.md)。

## 使用规则

1. 请始终传递完整的 JSON 数据；切勿使用交互式提示。
2. 请使用 `device_name`（推荐）或内联的 `device` 参数来指定设备。
3. 认证令牌格式：`sk_xxx`（可通过 Web 控制台 → 设备信息 → 连接设置 → HTTP/HTTPS 设置获取）。
- 如需按标签名称进行检测，请调用 `get_detection_models_info` 函数，将标签名称映射到对应的索引，然后在 `label_filter` 中使用该索引。
- 每 1–10 秒查询一次 `get_detection_events`；如需增量式获取数据，请传递 `start_unix_ms` 参数。
- 优先获取事件元数据；仅在需要时才下载图像。
- 命令行输出：成功时，输出结果会以 JSON 格式显示在标准输出（stdout）中（某些命令可能不会产生输出，请检查退出代码是否为 0）；失败时，错误信息会显示在标准错误输出（stderr）中，并提供具体的解决方法。

## 执行流程

对于涉及多个步骤的任务，请务必记录执行过程中的关键信息：

```text
reCamera Task Progress
- [ ] Resolve device (device_name or inline device)
- [ ] Validate JSON arguments
- [ ] Run CLI command
- [ ] If polling, checkpoint start_unix_ms
- [ ] Handle errors with one fix suggestion
```

## 命令行快速入门

从 `{baseDir}` 目录运行相关命令：

```bash
python3 scripts/device_manager.py add_device '{"name":"cam1","host":"192.168.1.100","token":"sk_xxxxxxxx"}'
python3 scripts/device_manager.py list_devices
python3 scripts/detection_manager.py get_detection_models_info '{"device_name":"cam1"}'
python3 scripts/detection_manager.py set_detection_model '{"device_name":"cam1","model_id":0}'
python3 scripts/detection_manager.py get_detection_events '{"device_name":"cam1"}'
python3 scripts/detection_manager.py clear_detection_events '{"device_name":"cam1"}'
python3 scripts/detection_manager.py fetch_detection_event_image '{"device_name":"cam1","snapshot_path":"/mnt/.../event.jpg","local_save_path":"./event.jpg"}'
python3 scripts/capture_manager.py capture_image '{"device_name":"cam1","local_save_path":"./capture.jpg"}'
```

## Python 自动化脚本（长时间运行的任务）

可以使用带有 `start_unix_ms` 参数的循环来实现增量式数据获取。

## 工作流程

### 添加设备

1. 使用设备主机名和令牌调用 `add_device` 函数。
2. 使用 `list_devices` 函数验证设备是否已成功添加。

### 按名称配置对象检测

1. 调用 `get_detection_models_info` 函数，将对象名称映射到对应的标签索引。
2. 使用 `set_detection_model` 函数设置检测模型。
3. 通过包含相应索引的 `label_filter` 参数设置检测规则。
4. 调用 `clear_detection_events` 函数以清除之前的检测结果。

### 监控事件

1. 每 1–10 秒查询一次 `get_detection_events` 函数。
2. 记录下一次查询的开始时间戳。
3. 仅在需要时通过 `fetch_detection_event_image` 函数下载图像。

### 按需获取快照

- **命令行**：使用 `capture_image` 函数，并指定 `local_save_path` 参数，返回结果（格式为 `{capture, saved_path, bytes}`）。
- **Python**：直接调用 `capture_image` 函数并将返回的图像数据保存到指定路径。
- **另一种方式**：也可以使用 `fetch_detection_event_image` 函数并指定 `local_save_path` 参数。

## 故障排除

| 错误现象 | 解决方法 |
|---|---|
| 出现 401/403 认证错误 | 请从 Web 控制台重新获取令牌。|
| 请求超时或连接失败 | 请检查设备主机地址、网络路径以及设备是否处于开启状态。|
| 任务调度被拒绝 | 请使用 `Day HH:MM:SS` 的格式设置调度时间。|
| 规则或事件数据为空 | 请确保规则和存储设置已正确配置；检查区域过滤条件；增加查询频率。|
| 下载图像失败 | 请使用最新的快照路径；部分数据可能已被替换。|
| 在 Python 模式下出现导入错误 | 请从 `{baseDir}` 目录运行脚本，并将 `./scripts` 添加到 `sys.path` 中。|