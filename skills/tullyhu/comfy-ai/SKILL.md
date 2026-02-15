# ComfyAI 技能（适用于 Clawdbot）

## 描述
该技能与本地 ComfyUI 实例（地址：http://192.168.31.7:8000）集成，支持将文本转换为图像（功能：txt2img），以及使用上传的参考图像对图像进行编辑（功能：img2img）。所使用的工作流程文件为：`~/clawd/skills/comfy-ai/image_flux2_klein_image_edit_4b_distilled.json`。

## 功能特性
- ✅ 文本转图像：仅根据文本提示生成图像
- ✅ 图像转图像：使用文本提示和参考图像对上传的图像进行编辑
- ✅ 生成后的图像会直接作为媒体附件返回到聊天界面

## 使用要求
- ComfyUI 必须运行在 `http://192.168.31.7:8000` 上
- 工作流程文件必须位于 `~/clawd/skills/comfy-ai/image_flux2_klein_image_edit_4b_distilled.json`
- 系统需安装 `curl`、`jq` 和 `python3`（macOS 上默认已安装）

## 使用示例
- “生成一只戴着太阳镜的赛博朋克风格的猫”
- “使用参考图像 [upload_handbag_white.png]，并对图像进行编辑，添加霓虹光效果和 logo”

## 工作原理
- **仅文本转换**：使用工作流程中提供的空白潜在表示（latent）和文本提示来生成图像
- **图像编辑**：系统会自动检测上传的图像，将其复制到 `~/clawd/skills/comfy-ai/input/` 目录，然后触发 `img2img` 脚本进行编辑
- 生成的图像会被保存在 `~/clawd/skills/comfy-ai/output/` 目录中，并作为媒体附件返回
- 该技能基于工作流程中指定的 Flux2-Klein-4B 模型（包含 VAE 和 CLIP 技术）来实现图像处理

## 安全提示
所有处理操作均在本地完成，数据不会离开用户的设备。