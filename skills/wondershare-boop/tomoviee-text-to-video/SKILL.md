---
name: tomoviee-text2video
description: 根据文本描述生成视频。支持720p/1080p分辨率，多种宽高比（16:9、9:16、4:3、3:4、1:1），以及4种不同的摄像机移动方式。生成的视频片段时长为5秒。适用于用户需要将文本转换为视频、根据提示创建视频，或生成具有特定摄像机移动效果的视频内容的情况。
---
# Tomoviee AI - 文生视频（Text-to-Video）

## 概述

该服务可以根据文本描述生成时长为5秒的视频，支持720p/1080p的分辨率、灵活的宽高比以及46种不同的摄像机移动效果。

**API**: `tm_text2video_b`

## 快速入门

### 认证

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python客户端示例

```python
from scripts.tomoviee_text2video_client import TomovieeText2VideoClient

client = TomovieeText2VideoClient("app_key", "app_secret")
```

## API使用方法

### 基本示例

```python
task_id = client.text_to_video(
    prompt="Golden retriever running through sunlit meadow, slow motion, cinematic",
    resolution="720p",
    aspect_ratio="16:9",
    camera_move_index=5
)

result = client.poll_until_complete(task_id)
import json
video_url = json.loads(result['result'])['video_path'][0]
```

### 参数

- `prompt`（必填）：文本描述（包括主题、动作、场景、摄像机位置和光线效果）
- `resolution`：`720p` 或 `1080p`（默认值：`720p`）
- `duration`：视频时长（以秒为单位，仅支持`5`秒）
- `aspect_ratio`：`16:9`、`9:16`、`4:3`、`3:4`、`1:1`
- `camera_move_index`：摄像机移动类型（1-46，可选）

## 异步工作流程

1. **创建任务**：通过API调用获取`task_id`。
2. **检查任务完成情况**：使用`poll_until_complete(task_id)`函数查询任务状态。
3. **提取结果**：解析返回的JSON数据以获取视频URL。

**状态代码**：
- 1 = 已排队
- 2 = 正在处理
- 3 = 成功（视频已生成）
- 4 = 失败
- 5 = 取消
- 6 = 超时

**生成时间**：每个5秒的视频大约需要1-5分钟。

## 摄像机移动效果

所有视频API都支持通过`camera_move_index`参数来设置46种不同的摄像机移动效果：
- 5 = 缓慢放大
- 12 = 向右平移
- 23 = 旋转/圆形移动
- None：自动选择摄像机移动方式

详细信息请参阅`references/camera_movements.md`。

## 提示工程（Prompt Engineering）

有效的提示能够显著提升视频生成的质量。

**提示格式**：`主题 + 动作 + 场景 + 摄像机位置 + 光线效果 + 氛围`

**示例**：
> “一辆红色法拉利在沿海公路上高速行驶，摄像机从侧面进行拍摄，夕阳时分，营造出电影般的震撼效果”

更多关于提示设计的指导，请参阅`references/prompt_guide.md`。

## 资源

### 脚本文件
- `tomoviee_text2video_client.py`：文本转视频API客户端
- `generate_auth_token.py`：认证令牌生成工具

### 参考文档
- `video_apis.md`：详细的视频API文档
- `camera_movements.md`：所有46种摄像机移动效果的说明
- `prompt_guide.md`：提示设计指南与最佳实践

## 外部资源

**🌐 网络路由说明：**
- **全球/海外用户**：请访问国际版本网站（`.ai`）。
- **中国大陆用户**：请访问国内版本网站（`.cn`），该版本提供更低的延迟和更符合中国用户需求的体验。

### 全球/海外（.AI）
- **开发者门户**：https://www.tomoviee.ai/developers.html
- **API文档**：https://www.tomoviee.ai/doc/
- **获取API凭证**：在开发者门户注册

### 中国大陆（.CN）
- **开发者门户**：https://www.tomoviee.cn/developers.html
- **API文档**：https://www.tomoviee.cn/doc/
- **获取API凭证**：在开发者门户注册