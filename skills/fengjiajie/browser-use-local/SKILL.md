---
name: browser-use-local
description: 当您需要通过 `browser-use` CLI 或 Python 代码在该 OpenClaw 容器/主机中实现浏览器自动化操作时，请使用此功能：打开页面、点击/输入内容、截图、提取 HTML 或链接；或者使用自定义的 `base_url` 运行与 OpenAI 兼容的 LLM（例如 Moonshot/Kimi）。此外，该功能还用于调试 `browser-use` 会话（例如会话状态为空、页面加载超时），以及通过截图或 HTML 中的 `data:image` 标签提取登录 QR 码。
---

# browser-use（本地）操作手册

## 本环境中的默认约束

- 在这里，优先使用 **browser-use**（CLI/Python）而非 OpenClaw 的 `browser` 工具；如果系统中没有支持的浏览器，OpenClaw 的 `browser` 可能会失败。
- 使用 **持久化会话** 来执行多步骤操作：`--session <名称>`。

## 快速的 CLI 工作流程（无需代理）

1) 打开目标页面

```bash
browser-use --session demo open https://example.com
```

2) 检查页面内容（在某些加载较慢或包含大量 JavaScript 的页面上，`state` 变量可能返回 0 个元素）

```bash
browser-use --session demo --json state | jq '.data | {url,title,elements:(.elements|length)}'
```

3) 截取屏幕截图（始终有效；是最基本的调试方法）

```bash
browser-use --session demo screenshot /home/node/.openclaw/workspace/page.png
```

4) 通过 HTML 提取链接信息（即使 `state` 为空时也能正常工作）

```bash
browser-use --session demo --json get html > /tmp/page_html.json
python3 - <<'PY'
import json,re
html=json.load(open('/tmp/page_html.json')).get('data',{}).get('html','')
urls=set(re.findall(r"https?://[^\s\"'<>]+", html))
for u in sorted([u for u in urls if any(k in u for k in ['demo','login','console','qr','qrcode'])])[:200]:
    print(u)
PY
```

5) 使用 JavaScript 进行轻量级的 DOM 查询（当 `state` 为空时非常有用）

```bash
browser-use --session demo --json eval "location.href"
browser-use --session demo --json eval "document.title"
```

## 使用与 OpenAI 兼容的 LLM（Moonshot/Kimi）的代理工作流程

当 CLI 命令需要使用浏览器访问云服务，或者你需要严格控制 LLM 的参数时，建议使用 Python 来运行代理。

### 最简单的 Kimi 使用示例

创建一个 `.env` 文件（或导出环境变量），内容如下：

- `OPENAI_API_KEY=...`
- `OPENAI_BASE_URL=https://api.moonshot.cn/v1`

然后运行打包好的脚本：

```bash
source /home/node/.openclaw/workspace/.venv-browser-use/bin/activate
python /home/node/.openclaw/workspace/skills/browser-use-local/scripts/run_agent_kimi.py
```

**在实际使用 Kimi/Moonshot 时需要注意的问题及解决方法**：

- 对于 `kimi-k2.5`，`temperature` 参数必须设置为 `1`。
- 对于 `kimi-k2.5`，`frequency Penalty` 参数必须设置为 `0`。
- Moonshot 可能会拒绝使用严格的 JSON 架构进行数据输出。请启用以下选项：
  - `remove_defaults_from_schema=True`
  - `remove_min_items_from_schema=True`

如果遇到 400 错误，提示 “response_format.json_schema ... keyword 'default' is not allowed” 或 “min_items unsupported”，请首先检查这两个参数是否设置正确。

## QR 码提取（登录/演示页面）

### 推荐的操作顺序

1) 截取页面的屏幕截图，并裁剪出可能的 QR 码区域（速度快且可靠性高）。
2) 如果 HTML 中包含 `data:image/png;base64,...` 格式的代码，提取并解码该图像。

### 裁剪 QR 码候选区域

使用 `scripts/crop_candidates.py` 从截图中生成多个可能的 QR 码裁剪区域。

```bash
source /home/node/.openclaw/workspace/.venv-browser-use/bin/activate
python skills/browser-use-local/scripts/crop_candidates.py \
  --in /home/node/.openclaw/workspace/login.png \
  --outdir /home/node/.openclaw/workspace/qr_crops
```

### 从 HTML 中提取嵌入的 Base64 图像

```bash
source /home/node/.openclaw/workspace/.venv-browser-use/bin/activate
browser-use --session demo --json get html > /tmp/page_html.json
python skills/browser-use-local/scripts/extract_data_images.py \
  --in /tmp/page_html.json \
  --outdir /home/node/.openclaw/workspace/data_imgs
```

## 故障排除

- 如果 `state` 变量显示 `elements: 0`，可以使用 `get html` 方法结合正则表达式来查找元素，同时结合屏幕截图进行辅助判断；也可以使用 `eval` 方法来查询 DOM 结构。
- 关于页面加载超时的警告：通常无关紧要，可以依赖屏幕截图和 HTML 内容进行判断。
- CLI 参数的顺序：全局参数必须放在子命令之前：
  - ✅ 正确的顺序是：`browser-use --browser chromium --json open https://...`
  - 错误的顺序是：`browser-use open https://... --browser chromium`