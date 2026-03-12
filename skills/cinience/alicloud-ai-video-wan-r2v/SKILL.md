---
name: alicloud-ai-video-wan-r2v
description: 使用 Alibaba Cloud Model Studio 的 Wan R2V 模型（wan2.6-r2v-flash、wan2.6-r2v）生成基于参考内容的视频。这些模型适用于从参考视频/图像素材创建多镜头视频、保持角色风格的一致性，或记录视频请求/响应流程。
version: 1.0.0
---
**类别：提供者**  
# Model Studio Wan R2V  

## 验证  
```bash
mkdir -p output/alicloud-ai-video-wan-r2v
python -m py_compile skills/ai/video/alicloud-ai-video-wan-r2v/scripts/prepare_r2v_request.py && echo "py_compile_ok" > output/alicloud-ai-video-wan-r2v/validate.txt
```  
通过验证的标准：命令以 0 代码退出，并且生成了 `output/alicloud-ai-video-wan-r2v/validate.txt` 文件。  

## 输出与证据  
- 将参考输入元数据、请求负载以及任务输出保存到 `output/alicloud-ai-video-wan-r2v/` 目录中。  
- 至少保留一个轮询结果的快照。  

使用 Wan R2V 生成视频参考文件；这与 i2v（将单张图片转换为视频）的功能不同。  

## 关键模型名称  
使用以下模型名称之一：  
- `wan2.6-r2v-flash`  
- `wan2.6-r2v`  

## 先决条件  
- 在虚拟环境中安装 SDK：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 在环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。  

## 规范化接口（video.generate_reference）  
### 请求  
- `prompt`（字符串，必填）  
- `reference_video`（字符串 | 字节，必填）  
- `reference_image`（字符串 | 字节，可选）  
- `duration`（数字，可选）  
- `fps`（数字，可选）  
- `size`（字符串，可选）  
- `seed`（整数，可选）  

### 响应  
- `video_url`（字符串）  
- `task_id`（字符串，异步请求时返回）  
- `request_id`（字符串）  

## 异步处理  
- 对于生产环境中的请求，建议使用异步提交方式。  
- 以 15-20 秒的间隔轮询任务结果。  
- 当返回 `SUCCEEDED` 或终端故障状态时，停止轮询。  

## 本地辅助脚本  
准备规范化的请求 JSON 数据，并验证响应格式：  
```bash
.venv/bin/python skills/ai/video/alicloud-ai-video-wan-r2v/scripts/prepare_r2v_request.py \
  --prompt "Generate a short montage with consistent character style" \
  --reference-video "https://example.com/reference.mp4"
```  

## 输出位置  
- 默认输出路径：`output/alicloud-ai-video-wan-r2v/videos/`  
- 可通过 `OUTPUT_DIR` 变量覆盖默认输出目录。  

## 工作流程  
1) 确认用户的操作意图、地区、相关标识符，以及操作是只读还是修改操作。  
2) 首先运行一个最小的只读查询，以验证连接性和权限。  
3) 使用明确的参数和受限的范围执行目标操作。  
4) 验证结果并保存输出文件及证据文件。  

## 参考资料  
- `references/sources.md`