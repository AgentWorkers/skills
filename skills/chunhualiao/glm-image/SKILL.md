---
name: glm-image
description: 使用 GLM-Image API 生成图像。当用户希望根据文本提示生成、创建或绘制图像时，可以使用该 API。该 API 会在收到如下请求时被触发：`generate an image of...`、`create a picture of...`、`draw...` 或任何与图像生成相关的请求。
---
# GLM-图像生成器

使用GLM-Image API根据文本提示生成图像。

> **版权说明：** 基于ViffyGwaanl开发的[glm-image](https://github.com/ViffyGwaanl/glm-image)，采用MIT许可证。

## 设置

该功能支持两种提供者。**您只需选择其中一种即可。**

### 选项A — GLM（BigModel / Zhipu AI）

需要从[https://open.bigmodel.cn](https://open.bigmodel.cn)的“控制台”→“API密钥”获取`GLM_API_KEY`。

```bash
export GLM_API_KEY=your-key
# or add to ~/.openclaw/config.json: { "api_key": "your-key" }
# or add GLM_API_KEY=your-key to .env
```

### 选项B — OpenRouter

需要从[https://openrouter.ai](https://openrouter.ai)的“密钥”获取`OPENROUTER_API_KEY`。

```bash
export OPENROUTER_API_KEY=your-key
# or add to ~/.openclaw/config.json: { "openrouter_api_key": "your-key" }
# or add OPENROUTER_API_KEY=your-key to .env
```

默认的OpenRouter模型为`google/gemini-3-pro-image-preview`。其他可选模型包括：`openai/gpt-5-image-mini`、`openai/gpt-5-image`、`google/gemini-2.5-flash-image-preview`。完整模型列表请参见[https://openrouter.ai/collections/image-models](https://openrouter.ai/collections/image-models)。

**自动检测：** 如果同时提供了两种API密钥，将使用GLM。可以通过`--provider openrouter`进行手动切换。

## 使用方法

当用户请求生成图像时：

**步骤0 — 确保至少配置了一个API密钥**

运行以下命令：

```bash
python3 -c "
import os, json, pathlib
glm = bool(os.environ.get('GLM_API_KEY'))
orouter = bool(os.environ.get('OPENROUTER_API_KEY'))
if not glm and not orouter:
    for p in ['~/.openclaw/config.json', '~/.claude/config.json']:
        try:
            d = json.loads(pathlib.Path(p).expanduser().read_text())
            if d.get('api_key'): glm = True
            if d.get('openrouter_api_key'): orouter = True
        except: pass
keys = []
if glm: keys.append('GLM_API_KEY')
if orouter: keys.append('OPENROUTER_API_KEY')
print('FOUND: ' + ', '.join(keys) if keys else 'KEY_MISSING')
"
```

如果输出结果为`KEY MISSING`，请告知用户：

> “未配置API密钥。该功能支持两种提供者——您只需选择其中一种：
>
> **选项A — GLM（BigModel）：** 请在[https://open.bigmodel.cn](https://open.bigmodel.cn)的“控制台”→“API密钥”处获取密钥，然后执行以下操作：
> ```
> export GLM_API_KEY=your-key
> ```
>
> **选项B — OpenRouter：** 请在[https://openrouter.ai](https://openrouter.ai)的“密钥”处获取密钥，然后执行以下操作：
> ```
> export OPENROUTER_API_KEY=your-key
> ```
>
> 您也可以将密钥添加到`~/.openclaw/config.json`文件中：
> ```json
> { "api_key": "glm-key" }
> { "openrouter_api_key": "openrouter-key" }
> ```**

在用户确认已设置密钥之前，请勿继续操作。

**步骤1 — 询问语言（必选）**

在运行任何命令之前，请询问用户：

> “您的提示使用的是哪种语言？请选择：zh（中文）、en（英文）、ja（日文）、ko（韩文）、fr（法文）、de（德文）、es（西班牙文）。”

**注意：** 不要根据用户消息的语言或其他信号自动推断语言，也切勿默认使用任何语言。只有在用户明确指定语言代码后才能继续操作。

**步骤2 — 运行生成脚本**

```bash
python3 scripts/generate.py "<prompt>" --language <code>
```

必须提供`--language`参数。如果省略该参数，脚本将报错。

其他默认设置如下：
- 图像尺寸：1088x1920（竖屏高清）
- 输出路径：`output/`文件夹
- 无水印

**步骤3 — 显示结果**

显示Markdown格式的图像链接和本地文件路径。

## 生成图像

```bash
python3 scripts/generate.py "<prompt>" --language <zh|en|ja|ko|fr|de|es>
```

系统会自动根据可用的API密钥选择相应的提供者。如果需要手动指定提供者，请使用`--provider`参数：

```bash
# Force OpenRouter with a specific model
python3 scripts/generate.py "<prompt>" --language en --provider openrouter --model google/gemini-2.5-flash-image-preview

# Force GLM
python3 scripts/generate.py "<prompt>" --language zh --provider glm
```

### 可用参数：

- `--language`：**必选** 提示使用的语言。支持的语言包括：`zh`（中文）、`en`（英文）、`ja`（日文）、`ko`（韩文）、`fr`（法文）、`de`（德文）、`es`（西班牙文）
- `--provider`：`glm`或`openrouter`。如果两个密钥都存在，系统会自动选择GLM
- `--model`：OpenRouter模型的名称（默认为`google/gemini-3-pro-image-preview`）。对于GLM，此参数可忽略。详细信息请参见[https://openrouter.ai/collections/image-models](https://openrouter.ai/collections/image-models)
- `--size`：图像尺寸（仅适用于GLM）——默认值为1088x1920，有效范围为512-2048px，必须是32的倍数
- `--output`：输出目录（默认为`output/`）
- `--quality`：图像质量（仅适用于GLM）——可选值：“hd”或“standard”（默认为“hd”）
- `--watermark`：是否添加水印（仅适用于GLM）

### 语言选择规则：

- **必须明确询问用户的语言。**切勿根据用户消息的语言进行猜测。
- **切勿默认设置语言。**如果用户未指定语言，请再次询问。
- **严格按用户输入的内容显示。** 必须准确传递用户输入的语言代码（例如`zh`、`en`），不要进行任何格式转换。
- **原因：** GLM是一个基于中文的模型，提示语言会显著影响生成图像的质量和风格。

### 可用的图像尺寸：

- 1088x1920（默认，竖屏高清）
- 1920x1920（横屏高清）
- 1280x1280（正方形）
- 1568x1056、1056x1568
- 1472x1088、1088x1472
- 1728x960、960x1728

## 输出格式

生成成功后，会显示以下内容：
1. 本地文件路径：`output/<timestamp>_<prompt>.png`
2. Markdown格式的图像链接：`![<prompt>](<url>)`

## 执行者

该功能由OpenClaw主代理会话执行。`generate.py`脚本通过`exec`工具以shell命令的形式运行，不会生成子代理。

## 成功条件：

- 脚本以0代码退出
- 图像文件保存到`output/`目录
- 向用户显示Markdown格式的图像链接

**失败情况：**
- API密钥无效
- 不支持的图像尺寸
- 网络超时（120秒）
- API使用量超出限制

## 特殊情况处理：
- 图像尺寸无效：尺寸必须在512-2048px之间，且必须是32的倍数；否则脚本会因API错误而失败
- 提示内容过长：提示内容会被截断为30个字符（实际生成的图像会使用完整的提示内容）
- 网络超时：API请求超时120秒，文件下载超时60秒；超时后允许重试一次
- API密钥缺失：脚本会显示错误信息并列出可用的API密钥
- 提示中包含中文字符：支持中文字符，但文件名中的中文字符会被自动处理掉

## 所需条件：

- 已配置GLM API密钥（详见“设置”部分）
- 安装了Python 3及`requests`包（使用`pip install requests`命令安装）