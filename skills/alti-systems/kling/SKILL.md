# Kling 视频生成技能

使用 Kling 2.6（通过 Kie.ai）生成 AI 视频。

## 命令

```bash
# Generate video and wait for result
/root/clawd/skills/kling/kling.js generate "A gym owner high-fiving a member"

# Quick start (returns task ID immediately)
/root/clawd/skills/kling/kling.js quick "Professional fitness environment"

# Check status
/root/clawd/skills/kling/kling.js status <task_id>
```

## 参数

- **模型**: kling-2.6/text-to-video （默认值）
- **宽高比**: 16:9 （默认值）
- **时长**: 5 秒 （默认值）
- **负面提示**: 过滤掉模糊/低质量的视频

## 使用场景

- 用户生成内容（UGC）风格的营销视频
- 健身/健身推广视频
- LinkedIn 视频帖子
- 客户评价可视化内容
- 产品演示视频

## 注意事项

- 视频生成时间约为 1-5 分钟
- 结果中会包含视频的 URL
- API 密钥存储在 `.env` 文件中，名为 `KIE_API_KEY`