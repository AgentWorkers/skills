---
name: stremio-cast
description: 使用 CATT 和 Playwright 在 Stremio Web 中搜索内容，并将其传输到 Chromecast 设备上。该功能允许您直接在电视上通过 Stremio 播放电影和电视剧。
---

# Stremio Cast

此技能允许Manus自动化Stremio的网页界面，以查找本地的流媒体链接，并将其传输到Chromecast设备上。

## 先决条件

为了使此技能正常工作，环境需要满足以下条件：
1. **Stremio Service** 需要在本地运行，并监听`11470`端口。
2. **Playwright** 已安装，用于浏览器自动化。
3. **CATT (Cast All The Things)** 已通过pip安装，用于实现流媒体传输功能。

## 工作流程

该技能执行以下步骤：
1. 打开Stremio的网页界面（`app.strem.io`）。
2. 搜索用户请求的电影或剧集名称。
3. 选择第一个结果以及可用的最佳流媒体链接。
4. 拦截Stremio本地服务器（`127.0.0.1:11470`）生成的流媒体URL。
5. 使用`catt`工具将此URL发送到指定的Chromecast设备。

## 使用方法

当用户请求“在Chromecast上播放[电影/剧集]”或“在电视上观看[剧集名称]”时，应调用此技能。

### 参数
- `query`：要搜索的电影或剧集名称。
- `device`：（可选）Chromecast设备的名称。默认值为“Living Room”。

### 命令示例
```bash
python3 scripts/stremio_cast.py "The Matrix" "Quarto"
```

## 重要说明
- **会话保持**：Stremio的流媒体服务器可能要求浏览器页面保持打开状态，以便继续下载文件。虽然脚本在开始流媒体传输后会关闭浏览器，但如果流媒体传输提前中断，这一设置可以进行调整。
- **CSS选择器**：Stremio网页界面的选择器可能会发生变化。如果技能在点击元素时失败，请检查`scripts/stremio_cast.py`中的选择器是否仍然有效。