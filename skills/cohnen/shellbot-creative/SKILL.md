---
name: shellbot-creative
version: 1.0.0
description: 这是一个功能强大的创意内容生成系统，支持图像/视频制作、图像编辑、动态场景制作、配音以及视频剪辑等工作。该系统整合了 Freepik、fal.ai、Nano Banana 2（Gemini 3.1 Flash Image Preview）和 Remotion 等工具，能够用于制作讲解视频、产品营销视频、社交媒体广告以及可重复使用的资源库。当用户需要创建或编辑视觉素材、生成视频片段、制作旁白/音乐，或根据简短需求制作出精美的最终视频时，该系统能够提供强大的支持。
allowed-tools: Bash(curl *api.freepik.com*), Bash(curl *queue.fal.run*), Bash(curl *api.fal.ai*), Bash(curl *fal.run*), Bash(jq *), Bash(mkdir *), Bash(infsh *), Bash(node *), Bash(npx *), Bash(npm *), Bash(ffmpeg *), Bash(python3 scripts/*), Read, Write
argument-hint: "<command> [provider_or_model] [--param value]"
metadata: {"openclaw":{"emoji":"🎬","primaryEnv":"FREEPIK_API_KEY","providerEnv":["FREEPIK_API_KEY","FAL_KEY","INFERENCE_API_KEY"],"homepage":"https://docs.openclaw.ai/tools/skills"}}
---
# shellbot-creative

通过智能地链接多个服务提供商，生成高端创意内容：

1. 生成可重复使用的素材（Nano Banana 2 / Freepik / fal）
2. 创建动态场景（Freepik Kling / fal 提供的视频模型）
3. 添加语音和音乐（Freepik ElevenLabs 语音服务或 fal 的语音合成功能）
4. 在 Remotion 中进行整合和后期处理

请将此技能作为生产协调工具使用，而非单独的独立操作。

## 参数

- **命令:** `$0` (`plan` | `asset` | `edit` | `video` | `voice` | `music` | `remotion` | `pipeline` | `status` | `sample`)
- **参数 1:** `$1` （服务提供商、模型或工作流程类型）
- **参数 2+:** `$2`, `$3`, 等
- **所有参数:** `$ARGUMENTS`

## 认证和提供商检查

支持以下服务提供商的认证：

- `FREEPIK_API_KEY`：用于 Freepik API
- `FAL_KEY`：用于 fal.ai API
- `INFERENCE_API_KEY`（或 `infsh login`）：通过 inference.sh 使用 Nano Banana 2

在任何生成操作之前：

```bash
[ -n "$FREEPIK_API_KEY" ] && echo "Freepik ready"
[ -n "$FAL_KEY" ] && echo "fal ready"
command -v infsh >/dev/null && echo "infsh available"
```

如果请求的服务提供商未通过认证，系统将自动切换到其他可用提供商，并明确告知用户切换原因。

## 服务提供商推荐（基于经验的选择）

- **创意素材生成/多图像一致性:** Nano Banana 2
- **逼真的产品图片、海报、排版、图像优化/编辑:** Freepik
- **快速模型探索或特定需求的 fal 服务:** fal.ai
- **最终视频剪辑、过渡效果、字幕、音频混音:** Remotion

详细模型选择请参考 `references/provider-matrix.md`。

## 命令行为

### `$0 = plan`

将用户需求转化为制作脚本和镜头列表。

```bash
python3 scripts/creative_brief_to_storyboard.py \
  --brief "Launch video for a new fitness app aimed at busy professionals" \
  --format product-marketing \
  --duration 45 \
  --aspect-ratio 16:9 \
  --out storyboard.json
```

然后生成服务提供商和模型的推荐方案：

```bash
python3 scripts/creative_provider_router.py \
  --goal full-video \
  --priority quality \
  --needs-consistency true \
  --needs-typography true
```

### `$0 = asset`

为场景生成静态素材。

- **Nano Banana 2 默认方案（保证一致性及编辑效果）:**
```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "Premium SaaS dashboard on a laptop, soft studio light",
  "aspect_ratio": "16:9",
  "num_images": 4,
  "resolution": "2K"
}'
```

- **Freepik 高保真产品图片（Mystic）:**
```bash
curl -s -X POST "https://api.freepik.com/v1/ai/mystic" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Studio product shot of matte black earbuds on reflective surface","resolution":"2k","styling":{"style":"photo"}}'
```

- **fal 快速概念设计（Flux）:**
```bash
curl -s -X POST "https://queue.fal.run/fal-ai/flux-2" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Cyberpunk storefront, rainy night","image_size":"landscape_16_9"}'
```

### `$0 = edit`

在动画制作前进行图像编辑、放大处理和背景处理。

- 对于需要确定性制作流程的情况，优先使用 Freepik 的编辑服务。
- 当需要基于多次参考的迭代编辑时，优先使用 Nano Banana 2。
- 最终交付时使用 Freepik 的图像放大工具。

编辑流程的详细信息请参考 `references/workflow-recipes.md`。

### `$0 = video`

根据提示或关键帧生成动态场景。

- 高级多镜头视频的默认选择：`kling-v3-omni-pro`（Freepik）
- 当 Freepik 的相关服务不可用时，使用 `fal-ai/kling-video/v2/image-to-video`（fal）

所有场景输出文件请保存在结构化的项目文件夹中：

```bash
mkdir -p ./creative-output/{assets,scenes,audio,final,manifests}
```

### `$0 = voice`

生成旁白。

- 默认选择：Freepik ElevenLabs 语音服务
- 如果用户仅需要 fal 服务，备用方案：fal 的文本转语音功能

使用根据制作脚本生成的简洁旁白内容。

### `$0 = music`

生成背景音乐，并确保音量适中，以便与旁白协调。

- 默认选择：Freepik 的音乐生成服务
- 音乐时长需与制作脚本中的时长相匹配（10-240 秒）

### `$0 = remotion`

使用整合后的素材、生成的片段、字幕和音频混音来制作最终视频。

```bash
npx create-video@latest creative-video
cd creative-video
```

根据制作脚本生成 Remotion 所需的文件结构：

```bash
python3 ../scripts/remotion_manifest_from_storyboard.py \
  --storyboard ../storyboard.json \
  --fps 30 \
  --voiceover-url "https://example.com/voice.mp3" \
  --music-url "https://example.com/music.mp3" \
  --out ./src/creative-manifest.json
```

然后使用 `assets/remotion/ProductMarketingTemplate.tsx` 作为基础模板进行视频剪辑。

### `$0 = pipeline`

执行端到端的制作流程：

1. 根据用户需求制定制作计划 (`plan`)
2. 为每个场景生成所需素材 (`asset`)
3. 编辑和优化选定的素材 (`edit`)
4. 为关键场景生成视频 (`video`)
5. 添加语音和音乐 (`voice` + `music`)
6. 使用 Remotion 进行最终剪辑和渲染 (`remotion`)

如果用户需要产品宣传或解释性视频，此命令路径为默认选择。

### `$0 = status`

检查 Freepik/fal 请求的异步任务状态，并提供以下信息：

- 当前状态
- 如果有队列任务，则显示排队位置
- 失败步骤的诊断信息
- 下一步操作建议

### `$0 = sample`

从 `references/samples.md` 中加载可立即执行的工作流程示例。

## “优秀”创意内容的质量标准

始终遵循以下标准：

- 清晰的叙事结构：引子 -> 价值点 -> 证据 -> 行动号召（CTA）
- 场景间的视觉一致性（相同的产品、调色板、风格）
- 语音和音乐的平衡（优先保证语音的清晰度）
- 字幕和屏幕文字需适应移动设备的显示区域
- 在最终渲染前获得品牌方的明确批准

## 制作工作流程规范

- 除非用户另有要求，否则解释性视频和产品演示视频采用 16:9 的比例
- 短片/抖音风格的视频采用 9:16 的比例
- 为关键场景生成 2-4 个不同的版本，然后进行优化
- 确保源素材可重复使用（背景干净、尽可能采用分层设计）
- 在进行修改时，先编辑提示或场景时间安排，再重新生成所有内容

## 本技能包含的本地资源

- `scripts/creative_brief_to_storyboard.py`：将用户需求转化为制作脚本
- `scripts/creative_provider_router.py`：根据需求选择合适的服务提供商和模型
- `scripts/remotion_manifest_from_storyboard.py`：将制作脚本转换为 Remotion 可用的文件结构
- `scripts/run_full_dry_run.py`：执行完整的本地预测试，输出制作脚本、服务提供商选择、文件结构和可执行的 API 计划
- `scripts/package_skill.sh`：将本技能打包成可发布的 `.tar.gz` 文件
- `scripts/install_skill.sh`：将本技能文件夹安装到 OpenClaw 的技能目录中
- `references/creative-guidelines.md`：创意质量的长期标准
- `references/provider-matrix.md`：服务提供商和模型选择指南
- `references/workflow-recipes.md`：常见成果的端到端制作流程
- `references/samples.md`：具体的命令使用示例
- `references/remotion-playbook.md`：Remotion 的特定剪辑指南
- `assets/remotion/ProductMarketingTemplate.tsx`：Remotion 的基础剪辑模板
- `assets/remotion/Root.tsx`：剪辑样本文件

## 参考资料

- OpenClaw 技能格式和文档结构：https://docs.openclaw.ai/tools/skills
- OpenClaw 命令使用方式 (`$0`, `$1`, `$ARGUMENTS`)：https://docs.openclaw.ai/tools/slash-commands
- OpenClaw 元数据配置：https://docs.openclaw.ai/tools/skills-config
- OpenClaw 技能创建指南：https://docs.openclaw.ai/tools/creating-skills