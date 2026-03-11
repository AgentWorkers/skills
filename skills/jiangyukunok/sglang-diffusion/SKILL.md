---
name: sglang-diffusion
description: "**使用本地的 SGLang-Diffusion 服务器生成图像（支持 FLUX、Stable Diffusion、Qwen-Image 等引擎）**  
**适用场景：** 当用户需要使用本地运行的 SGLang-Diffusion 实例来生成、创建或渲染图像时。  
**不适用场景：** 不适用于基于云的图像生成服务（请使用 openai-image-gen 或 nano-banana-pro）。  
**前提条件：** 必须确保 SGLang-Diffusion 服务器已正常运行。"
homepage: https://github.com/sgl-project/sglang
metadata:
 {
   "openclaw":
     {
       "emoji": "🎨",
       "requires": { "bins": ["python3"] },
     },
 }
---

# 使用 SGLang-Diffusion 生成图像


通过本地的 SGLang-Diffusion 服务器及其兼容 OpenAI 的 API 来生成图像。


## 先决条件


- SGLang-Diffusion 服务器正在运行（默认地址：`http://127.0.0.1:30000`）
- 如果服务器是以 `--api-key` 参数启动的，请设置环境变量 `SGLANG_DIFFUSION_API_KEY`


## 生成图像


```bash
python3 {baseDir}/scripts/generate.py --prompt "a futuristic cityscape at sunset"
```


## 有用的参数


```bash
python3 {baseDir}/scripts/generate.py --prompt "portrait of a cat" --size 512x512
python3 {baseDir}/scripts/generate.py --prompt "abstract art" --negative-prompt "blurry, low quality"
python3 {baseDir}/scripts/generate.py --prompt "landscape" --steps 30 --guidance-scale 7.5 --seed 42
python3 {baseDir}/scripts/generate.py --prompt "photo" --server http://192.168.1.100:30000 --out ./my-image.png
```


## API 密钥（可选）


仅当 SGLang-Diffusion 服务器是以 `--api-key` 参数启动时才需要使用此参数。
可以通过设置环境变量 `SGLANG_DIFFUSION_API_KEY` 或直接在命令行中传递 `--api-key` 来使用 API 密钥：


```bash
python3 {baseDir}/scripts/generate.py --prompt "hello" --api-key sk-my-key
```


或者可以在 `~/.openclaw/openclaw.json` 文件中进行配置：


```json5
{
 skills: {
   "sglang-diffusion": {
     env: { SGLANG_DIFFUSION_API_KEY: "sk-my-key" },
   },
 },
}
```


## 注意事项


- 该脚本会输出一条 `MEDIA:` 信息，以便 OpenClaw 可以在支持的聊天平台上自动加载生成的图像。
- 输出文件默认为带有时间戳的 PNG 格式，保存在 `/tmp/` 目录下。
- 请勿直接读取生成的图像文件，只需提供其保存路径即可。