---
name: glm-image
description: 使用 GLM-Image API 生成图像。当用户希望根据文本提示生成、创建或绘制图像时，可以使用该 API。该 API 会在收到如下请求时被触发：`generate an image of...`、`create a picture of...`、`draw...` 或任何与图像生成相关的请求。
---
# GLM-图像生成器

使用GLM-Image API根据文本提示生成图像。

> **版权说明：** 基于ViffyGwaanl开发的[glm-image](https://github.com/ViffyGwaanl/glm-image)，采用MIT许可证。

## 使用方法

当用户提供图像生成提示时：

1. 使用相应的提示运行生成脚本。
2. 默认尺寸为1088x1920（高清竖屏图像）。
3. 图像会自动保存到`output/`文件夹中。
4. 默认情况下不添加水印。
5. 以Markdown格式返回图像的URL。

## 生成图像

```bash
python3 scripts/generate.py "<prompt>"
```

### 参数选项

- `--size`：图像尺寸（默认：1088x1920）。有效范围：512-2048像素，必须是32的倍数。
- `--output`：自定义输出路径（默认：`output/`）。
- `--quality`：图像质量，可选“hd”或“standard”（默认：hd）。
- `--watermark`：是否添加水印（默认：不添加）。

### 可用的尺寸

- 1088x1920（默认，高清竖屏）
- 1920x1088（高清横屏）
- 1280x1280（正方形）
- 1568x1056, 1056x1568
- 1472x1088, 1088x1472
- 1728x960, 960x1728

## 输出格式

生成成功后，会显示以下内容：

1. 本地文件路径：`output/<timestamp>_<prompt>.png`
2. Markdown格式的图像链接：`![<prompt>](<url>)`

## 配置

请在`TOOLS.md`文件中设置`GLM_API_KEY`，或将其作为环境变量。切勿在技能文件中直接硬编码。

`TOOLS.md`中必须包含的条目：
- **GLM_API_KEY**：您的BigModel API密钥（https://open.bigmodel.cn）

该脚本还会从`config.json`或`.env`文件中读取配置信息（作为备用方案）。

## 执行代理

此技能由OpenClaw主代理会话执行。`generate.py`脚本通过`exec`工具以shell命令的形式运行，不会创建子代理。

## 成功标准

图像生成成功的前提条件包括：
1. 脚本以0代码退出。
2. 图像文件保存到`output/`目录中。
3. 向用户显示Markdown格式的图像链接。

## 失败情况

- API密钥无效。
- 不支持的尺寸。
- 网络超时（120秒）。
- API配额超出。

## 特殊情况处理：

- 尺寸无效：尺寸必须在512-2048像素之间，并且必须是32的倍数；否则脚本会因API错误而失败。
- 提示过长：提示内容会被截断为30个字符（实际生成的图像将使用完整的提示内容）。
- 网络超时：API超时时间为120秒，下载超时时间为60秒；超时后尝试重新生成一次。
- API密钥缺失：脚本会输出错误信息并显示搜索位置。
- 提示中包含中文字符：支持中文字符，文件名会自动进行清洗处理。

## 所需条件

- 需要设置`GLM_API_KEY`环境变量或`config.json`文件中的`api_key`。