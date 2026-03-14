---
name: best-practice-skill-creator
description: 根据最佳实践视频或图像序列创建 OpenClaw 技能。这些方法可用于从视频中生成技能、从截图中创建技能、将教程转换为技能，以及构建自动化最佳实践流程。
user-invocable: true
metadata: {"openclaw":{"emoji":"🎓","requires":{"anyBins":["python3","python"]},"os":["darwin","linux","win32"],"primaryEnv":"MLLM_API_KEY"}}
---
# 最佳实践技能创建器（Best Practice Skill Creator）

这是一个能够根据最佳实践演示内容创建兼容 OpenClaw 的技能的工具。

## 功能介绍

您需要提供以下输入：
1. **视频文件**（格式：mp4、mov、avi、webm），这些文件展示了最佳实践的工作流程。
2. **图像序列**（格式：png、jpg、webp），包含每一步的操作截图。
3. **文本描述**，说明该任务的具体功能及其使用场景。

随后，该工具会使用多模态大型语言模型（GPT-5.4 或 Gemini 3.1 Pro Preview）来：
- 逐帧分析视频/图像内容。
- 提取详细的操作步骤。
- 识别所使用的工具、命令及操作模式。
- 生成一个完全兼容 OpenClaw 的技能文件。

## 使用方法

```bash
# From video + description
python3 best_practice_skill_creator/main.py \
  --input video.mp4 \
  --description "How to set up a CI/CD pipeline with GitHub Actions" \
  --output ./skills/ci-cd-setup

# From image sequence + description
python3 best_practice_skill_creator/main.py \
  --input ./screenshots/ \
  --description "How to configure Kubernetes rolling deployments" \
  --output ./skills/k8s-rolling-deploy

# Specify provider
python3 best_practice_skill_creator/main.py \
  --input video.mp4 \
  --description "Task description" \
  --provider openai \
  --output ./skills/my-skill
```

## 配置说明

请编辑 `best_practice_skill_creator/config.yaml` 文件，以配置您所使用的大型语言模型（MLLM）提供商、API 密钥以及具体模型：

- `MLLM_PROVIDER`：`openai` 或 `gemini`
- `MLLM_API_KEY`：您的 API 密钥
- `MLLM_BASE_URL`：自定义的 API 端点地址
- `MLLM_MODEL`：所选模型的标识符

## 输出结果

生成的技能文件将包含以下内容：
- `SKILL.md`：一个符合 OpenClaw 标准的技能文档，包含完整的前言和结构。
- 该技能文件可以直接通过 `clawhub publish` 命令发布，或保存在 `~/.openclaw/skills/` 目录中供直接使用。