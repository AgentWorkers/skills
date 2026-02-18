---
name: short-url
description: 您可以通过 PicSee (picsee.io) 快速缩短网址并生成二维码。登录后，您还可以查看相关分析和使用记录。当用户请求“缩短网址”或“生成二维码”时，可以使用该服务。
---
# PicSee URL缩短器

通过 PicSee (picsee.io) 快速缩短长 URL 并生成 QR 码。登录后，您还可以查看分析数据和历史记录。

## 重要规则

- **始终使用 `profile: "openclaw"`**
- **每个快照都会生成新的引用（refs）**——请勿重复使用旧的引用
- **如果任何步骤失败，请从第一步重新开始**
- **在读取文件时，仅使用 `file_path` 参数**——不要传递 `path: ""`（空字符串会导致 EISDIR 错误）
- **QR 码是可选的**——除非用户明确要求，否则不要生成 QR 码（这样可以节省令牌）
- **使用虚拟环境生成 QR 码**——确保 `qrcode` 包始终可用，同时不会污染系统的 Python 环境

## 工作流程

核心技术：对链接进行 URL 编码，并将其添加到查询字符串中，PicSee 会自动缩短链接。只有当用户请求时才会生成 QR 码（以节省令牌）。

### 第一步：使用 URL 打开 PicSee

对长 URL 进行 URL 编码，然后将其添加到 `https://picsee.io/?url=` 中。

使用 `browser` 工具：

```
action: "open"
profile: "openclaw"
targetUrl: "https://picsee.io/?url=(URL-encoded long URL)"
```

**URL 编码示例：**
- 原始 URL：`https://example.com/path?a=1&b=2`
- 编码后的 URL：`https%3A%2F%2Fexample.com%2Fpath%3Fa%3D1%26b%3D2`
- 完整的 URL：`https://picsee.io/?url=https%3A%2F%2Fexample.com%2Fpath%3Fa%3D1%26b%3D2`

保存返回的 `targetId`——您将在后续步骤中需要它。

### 第二步：等待缩短完成

使用 `browser` 工具等待 3 秒：

```
action: "act"
profile: "openclaw"
targetId: "(targetId from Step 1)"
request:
  kind: "wait"
  timeMs: 3000
```

### 第三步：提取缩短后的 URL

获取快照并从页面内容中提取缩短后的 URL：

```
action: "snapshot"
profile: "openclaw"
targetId: "(targetId from Step 1)"
refs: "aria"
```

阅读快照文本并找到缩短后的 URL。PicSee 会在缩短完成后在页面上突出显示结果。请注意以下内容：
- 一个看起来像缩短 URL 的可点击链接
- 显示“shortened URL”或类似内容的文本，后面跟着一个链接
- 任何明显比原始输入更短的 URL

如果您在快照中找不到缩短后的 URL，请再等待 3 秒并重试。如果经过 2 次尝试后仍然找不到，请使用备用方法（见下文）。

### 第四步：回复缩短后的 URL 并询问是否需要 QR 码

仅回复缩短后的 URL。**默认情况下不要生成 QR 码**。

**回复时使用与用户原始请求相同的语言。** 例如（英文格式）：

```
Short URL: https://pse.is/xxxxx

Need QR code?
```

语言模型会根据需要自动将此内容翻译成用户的语言。

等待用户的回复。如果用户确认需要 QR 码，请进入第五步。

### 第五步（可选）：使用虚拟环境生成 QR 码

**仅当用户明确请求 QR 码时才运行此步骤**。

使用 Python 虚拟环境来确保 `qrcode` 包可用：

```bash
# Check if venv exists, create if not
if [ ! -d ~/openclaw_python_venv ]; then
  python3 -m venv ~/openclaw_python_venv
  source ~/openclaw_python_venv/bin/activate
  pip install qrcode pillow
else
  source ~/openclaw_python_venv/bin/activate
fi

# Generate QR code
python3 - <<'PY'
import qrcode
qr = qrcode.QRCode()
qr.add_data("THE_SHORT_URL_HERE")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("/tmp/picsee_qr.png")
print("QR code saved")
PY
```

生成 QR 码后，使用 `message` 工具发送 QR 码图片文件，文件路径为 `filePath: "/tmp/picsee_qr.png"`。

## 备用方法（当快速方法失败时）

如果第一步的 URL 参数方法无法自动缩短链接（页面仍显示主页），请使用手动操作：

1. 使用 `snapshot` 获取页面元素的引用（`refs: "aria"`）
2. 找到输入框（名为“網址貼這裡”的文本框）和按钮（`img "PicSee!"`）
3. 使用 `act type` 在输入框中输入 URL
4. 使用 `act click` 点击缩短按钮
5. 重新执行第二步到第四步以获取结果

## 常见错误处理

- **EISDIR 错误**：在读取文件时，不要传递 `path: ""`，仅使用 `file_path` 参数
- **未知的引用（ref）**：引用已过期，请重新运行快照以获取新的引用
- **找不到标签页（tab）**：页面已关闭，请从第一步重新开始
- **快照中看不到缩短后的 URL**：将等待时间增加到 5000 毫秒并重试
- **仍然找不到缩短后的 URL**：切换到备用方法
- **虚拟环境创建失败**：使用 `python3 --version` 检查 Python 版本（需要 3.3 或更高版本）