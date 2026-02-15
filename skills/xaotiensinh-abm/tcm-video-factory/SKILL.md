---
name: tcm-video-factory
description: 使用 Perplexity API 自动化健康视频制作计划（包括主题研究、脚本编写、角色设计以及图像/视频素材的选取）。该流程基于 TCM Video Factory 的工作流程。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["node"],"env":["PERPLEXITY_API_KEY"]},"primaryEnv":"PERPLEXITY_API_KEY"}}
---

# TCM Video Factory

这是一个自动化的工作流程，用于生成完整的视频制作计划，包括剧本、角色设计以及AI生成的提示内容（使用Nano Banana/VEO3工具）。

## 使用方法

```bash
# Generate a plan for a specific topic
node skills/tcm-video-factory/index.mjs "Trà gừng mật ong"

# Generate a plan for a general theme (auto-research)
node skills/tcm-video-factory/index.mjs "Mẹo ngủ ngon"
```

## 输出结果

会在当前目录下生成一个名为`PLAN_[Timestamp].md`的文件，其中包含以下内容：
1. 选定的主题
2. 角色设计提示（采用Pixar 3D技术）
3. 由4个部分组成的剧本（总时长32秒）
4. 每个部分的图片提示（用于视频的开头和结尾）
5. VEO3视频制作所需的提示内容（包含唇形同步效果）