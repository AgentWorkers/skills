---
name: google-tv
description: 通过ADB（Android Debug Bridge）播放YouTube或Tubi上的内容；对于其他流媒体应用，则回退到Google TV的全球搜索功能。
metadata: {"openclaw":{"os":["darwin","linux"],"requires":{"bins":["adb","uv"]},"install":[{"id":"brew-adb","kind":"brew","cask":"android-platform-tools","bins":["adb"],"label":"Install adb (android-platform-tools)"},{"id":"brew-uv","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv"}]}}
---

# 通过 Google TV 控制 Chromecast

当您需要将 YouTube 或 Tubi 视频内容投射到 Chromecast 上、播放或暂停 Chromecast 上的媒体播放、检查 Chromecast 是否在线，或通过全局搜索来在其他流媒体应用中播放剧集内容时，请使用此技能。

## 设置

此技能依赖于 `uv` 和 `adb`，并确保它们已添加到系统的 `PATH` 环境变量中。无需创建虚拟环境（`venv`）。

- 确保 `uv` 和 `adb` 可以通过 `PATH` 访问。
- 使用 `./run` 命令作为 `uv run google_tv_skill.py` 的便捷入口。

## 功能

此技能通过 ADB 提供了一组简单的命令行接口（CLI）来控制 Google TV 设备，支持以下功能：

- `status`：显示 ADB 设备的连接状态。
- `play <query_or_id_or_url>`：通过 YouTube、Tubi 或全局搜索来播放内容。
- `pause`：暂停媒体播放。
- `resume`：恢复媒体播放。

### 使用示例

```bash
./run status --device 192.168.4.64 --port 5555
./run play "7m714Ls29ZA" --device 192.168.4.64 --port 5555
./run play "family guy" --app hulu --season 3 --episode 4 --device 192.168.4.64 --port 5555
./run pause --device 192.168.4.64 --port 5555
```

### 设备选择与环境变量覆盖

- 您可以通过 CLI 参数 `--device` 和 `--port` 指定设备。
- 或者，您可以通过设置环境变量 `CHROMECAST_HOST` 和 `CHROMECAST_PORT` 来覆盖默认值。
- 如果仅提供了 `--device` 或 `--port`，脚本会使用缓存中的设备信息；否则会报错。
- 脚本会将最后一次成功连接的设备信息（IP 和端口）保存到 `skill` 文件夹中的 `.last_device.json` 文件中。如果没有提供设备信息，脚本会尝试通过 ADB 的 mDNS 服务发现功能来自动选择设备。
- **重要提示**：此技能不会主动扫描或探测端口，只会尝试连接到指定的端口或缓存中的端口。

### YouTube 的处理方式

- 如果提供了 YouTube 视频 ID 或 URL，脚本会通过 ADB 指令直接在 YouTube 应用中播放视频。
- 脚本会使用 `yt-api`（如果已安装并添加到 `PATH`）来解析视频 ID。如果解析失败，会报告错误。
- 您可以通过 `YOUTUBE_PACKAGE` 环境变量来指定 YouTube 应用的包名（默认为 `com.google.android.youtube.tv`）。

### Tubi 的处理方式

- 如果提供了 Tubi 的 URL，脚本会通过 ADB 发送一个 VIEW 指令来播放该视频（仅在 Tubi 应用内生效）。
- 如果需要使用 Tubi 的官方网址，助手可以通过网络搜索来获取该网址并传递给脚本。
- 您可以通过 `TUBI_PACKAGE` 环境变量来指定 Tubi 应用的包名（默认为 `com.tubitv`）。

### 非 YouTube/Tubi 内容的全局搜索方式

- 如果 YouTube/Tubi 的方法不可用，并且您指定了其他流媒体服务（如 `hulu`、`max`、`disney+`），脚本会使用 Google TV 的全局搜索功能。
- 使用 `--app`、`--season` 和 `--episode` 参数来指定要搜索的内容。
- 脚本会启动 `android.search.action.GLOBAL_SEARCH` 功能，显示剧集列表，选择相应的季数和剧集，然后提示用户“在 <app> 中打开”。

### 暂停/恢复播放

```bash
./run pause
./run resume
```

### 依赖项

- 该脚本仅使用 Python 标准库，无需安装额外的第三方包（如 pip）。
- 脚本通过 `uv` 来执行操作，以符合 PEP 668 的要求。
- 脚本要求 `adb`、`uv` 和 `yt-api` 已安装并添加到系统的 `PATH` 环境变量中。

### 缓存机制

- 脚本会将最后一次成功连接的设备信息（IP 和端口）保存到 `skill` 文件夹中的 `.last_device.json` 文件中。
- 脚本不会主动扫描端口，以确保行为的稳定性并避免与 Google 的 ADB 端口策略冲突。

### 故障排除

- 如果 `adb connect` 失败，可以手动运行 `adb connect IP:PORT` 来检查当前连接的端口。
- 如果在交互式模式下运行时 `adb connect` 被拒绝，脚本会提示您输入新的端口，并在连接成功后更新 `.last_device.json` 文件。

## 实现细节

- 此技能的 CLI 代码位于 `google_tv_skill.py` 文件中。它通过 `subprocess` 调用 `adb` 和 `yt-api`，并使用内部的全局搜索功能来实现其他功能。
- 对于 Tubi 的 URL，助手可以通过网络搜索来获取正确的页面地址并传递给脚本。