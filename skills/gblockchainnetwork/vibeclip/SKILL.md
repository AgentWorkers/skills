---
**名称：vibeclip**  
**描述：** 从旋律音频、图片以及用户提供的提示生成AI音乐视频。使用本地部署的Ollama（llama3.2:1b/phi3:mini）生成场景描述，通过FFmpeg实现视频的变形、缩放以及波形同步处理。该应用基于Node.js和Express框架开发，支持部署在VPS上（端口：3000）。演示方式：执行 `cd video-app` 后运行 `node index.js`。支持通过信用点数或ETH进行SaaS付费。  

**元数据：**  
```json
openclaw:  
  requires:  
    bins: [node, ollama, ffmpeg]  
  install:  
    - id: ollama-models  
      kind: exec  
      command: ollama pull llama3.2:1b phi3:mini  
```

## **使用方法：**  
发送POST请求到 `/generate` 端点，提供以下参数：  
- `audio`：音频文件路径  
- `photo`：图片文件路径  
- `prompt`：视频制作的提示或描述  

**收入模式：**  
- API使用免费。  
- 支持通过ETH向开发者钱包支付费用。