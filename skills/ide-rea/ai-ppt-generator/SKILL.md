---
name: ai-ppt-generator
description: 百度提供的这款超棒的PPT格式生成工具！
metadata: { "openclaw": { "emoji": "📑", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 人工智能PPT生成
根据用户输入的主题或查询内容，生成高质量的PPT文件，并可将其下载到本地磁盘。

## 工作流程
1. 运行位于 `scripts/generate_ppt.py` 的Python脚本来生成PPT文件。

### generate_ppt
#### 使用示例
```bash
 python3 scripts/generate_ppt.py --query "经济总结报告ppt"
```