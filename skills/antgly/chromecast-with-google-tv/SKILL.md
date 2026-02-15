---
name: chromecast-with-google-tv
description: 通过ADB将YouTube视频、Tubi TV的剧集以及其他视频流媒体应用程序中的剧集投屏到支持Android TV的Chromecast设备上（支持Chromecast 4K，但是否支持Google TV Streamer尚不清楚）。
metadata: {"openclaw":{"os":["darwin","linux"],"requires":{"bins":["adb","scrcpy","uv","yt-api"]},"install":[{"id":"brew-adb","kind":"brew","cask":"android-platform-tools","bins":["adb"],"label":"Install adb (android-platform-tools)"},{"id":"brew-scrcpy","kind":"brew","formula":"scrcpy","bins":["scrcpy"],"label":"Install scrcpy"},{"id":"brew-uv","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv"},{"id":"go-yt-api","kind":"go","module":"github.com/nerveband/youtube-api-cli/cmd/yt-api@latest","bins":["yt-api"],"label":"Install yt-api (go)"}]}}
---

# 通过 Google TV 控制 Chromecast

当您需要将 YouTube 或 Tubi 视频内容投射到 Chromecast 上、播放或暂停 Chromecast 上的媒体播放、检查 Chromecast 是否在线、通过全局搜索在其他流媒体应用中查找剧集内容，或者首次配对 Chromecast 设备时，请使用此技能。

## 设置

此技能依赖于 `uv`、`adb`、`yt-api` 和 `scrcpy` 这些工具，并将这些工具添加到系统的 `PATH` 环境变量中。无需创建虚拟环境（venv）。

- 确保 `uv`、`adb`、`yt-api` 和 `scrcpy` 已经添加到系统的 `PATH` 中。
- 使用 `./run` 作为 `uv run google_tv_skill.py` 命令的便捷入口。

### 首次配对

在使用此技能之前，您需要将 Chromecast 与 ADB 无线调试功能进行配对：

1. 在 Chromecast 的设置中启用开发者选项（Settings > System > About > 点击 “Android TV OS build” 7 次）。
2. 在开发者选项中启用 USB 调试和无线调试功能。
3. 使用 `pair` 命令按照屏幕上显示的配对代码进行配对：
   - `./run pair --show-instructions`：显示详细的配对步骤。
   - `./run pair --pairing-ip <IP> --pairing-port <PORT> --pairing-code <CODE>`：执行配对操作。

配对成功后，您可以使用无线调试屏幕上显示的连接端口来执行其他所有命令。

## 功能

此技能通过 CLI 提供了对 Google TV 设备的基本控制功能，支持以下子命令：

- `pair`：使用无线调试功能与 Chromecast 配对（首次使用时使用）。
- `status`：显示 ADB 设备的连接状态。
- `play <query_or_id_or_url>`：通过 YouTube、Tubi 或全局搜索来播放内容。
- `pause`：暂停媒体播放。
- `resume`：恢复媒体播放。

### 使用示例

```bash
./run pair --show-instructions
./run pair --pairing-ip 192.168.1.100 --pairing-port 12345 --pairing-code 123456
./run status --device 192.168.4.64 --port 5555
./run play "7m714Ls29ZA" --device 192.168.4.64 --port 5555
./run play "family guy" --app hulu --season 3 --episode 4 --device 192.168.4.64 --port 5555
./run pause --device 192.168.4.64 --port 5555
```

### 设备选择与环境变量覆盖

- 您可以通过 CLI 参数 `--device` 和 `--port` 指定设备。
- 或者，您也可以通过设置环境变量 `CHROMECAST_HOST` 和 `CHROMECAST_PORT` 来覆盖默认值。
- 如果只提供了 `--device` 或 `--port`，脚本会使用缓存中的信息；否则会报错。
- 脚本会将最后一次成功的连接信息（IP 和端口）保存到 `skill` 文件夹中的 `.last_device.json` 文件中。如果没有提供设备信息，脚本会尝试通过 ADB 的 mDNS 服务发现功能来自动选择设备。
- **重要提示**：此技能不会进行任何端口扫描或探测操作，只会尝试连接到指定的端口或缓存中的端口。

### YouTube 的处理方式

- 如果提供了 YouTube 视频 ID 或 URL，脚本会通过 ADB 操作直接在 YouTube 应用中播放该视频。
- 如果 ID 解析失败，脚本会报告错误。
- 您可以通过 `YOUTUBE_PACKAGE` 环境变量来指定 YouTube 应用的包名（默认值为 `com.google.android.youtube.tv`）。

### Tubi 的处理方式

- 如果提供了 Tubi 的 HTTPS URL，脚本会通过 ADB 操作在 Tubi 应用中播放该视频。
- 如果需要使用 Tubi 的官方 HTTPS URL，脚本会通过网络搜索来获取该 URL 并使用它。
- 您可以通过 `TUBI_PACKAGE` 环境变量来指定 Tubi 应用的包名（默认值为 `com.tubitv`）。

### 非 YouTube/Tubi 内容的全局搜索方式

- 如果 YouTube 或 Tubi 的方式无法使用，并且您指定了其他流媒体服务（如 Hulu、Max、Disney+），脚本会使用 Google TV 的全局搜索功能。
- 使用 `--app`、`--season` 和 `--episode` 参数来指定目标服务。
- 确保 `scrcpy` 已经安装并添加到系统的 `PATH` 中。
- 此过程会启动 `android.search.action.GLOBAL_SEARCH` 功能，等待系列概览界面出现，选择相应的季数和剧集，然后选择 “在 <app> 中打开”。
- 注意：脚本不处理 Hulu 的特定配置选项。

### 暂停/恢复播放

```bash
./run pause
./run resume
```

### 依赖项

- 该脚本仅使用 Python 标准库，无需安装额外的 pip 包。
- 脚本通过 `uv` 来运行，以避免 PEP 668 规范对系统包的要求。
- 脚本要求 `adb`、`scrcpy`、`uv` 和 `yt-api` 已经安装并添加到系统的 `PATH` 中。

### 缓存与默认设置

- 脚本会将最后一次成功的连接信息（IP 和端口）保存到 `skill` 文件夹中的 `.last_device.json` 文件中。
- 脚本不会尝试扫描端口，这样可以保持行为的稳定性，并避免与 Google 的 ADB 端口轮换策略发生冲突。

### 故障排除

- 如果 `adb connect` 失败，可以手动在主机上运行 `adb connect IP:PORT` 命令来检查当前端口是否可用。
- 如果在交互式模式下运行时 `adb connect` 失败，脚本会提示您输入新的端口，并在连接成功后更新 `.last_device.json` 文件。
- **配对后连接失败**：如果连接失败，请检查 Chromecast 是否仍然启用了无线调试功能；如果设备已重启或无线调试功能被关闭，可能需要重新配对。交互式界面会提供重试或重新配对的选项。
- 可以使用 `./run pair --show-instructions` 命令查看详细的配对步骤。

### 实现说明

- 该技能的 CLI 代码位于 `google_tv_skill.py` 文件中。它通过 `subprocess` 调用 `adb`、`scrcpy` 和 `yt-api`，并使用一个内部的全局搜索辅助函数来实现播放功能。
- 对于 Tubi URL 的处理，脚本会通过 `web_search` 功能来获取 Tubi 的官方页面地址，并将其传递给相应的应用程序。