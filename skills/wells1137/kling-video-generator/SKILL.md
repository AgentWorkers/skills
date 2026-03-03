---
name: kling-video-generator
description: 使用 Kling 3.0 Omni 模型，可以从文本、图像或其他视频生成高质量的视频。该模型支持文本转视频、图像转视频、视频编辑、视频参考、多镜头视频生成以及音频同步功能。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - KLING_ACCESS_KEY
        - KLING_SECRET_KEY
      bins:
        - python3
    primaryEnv: KLING_ACCESS_KEY
    emoji: "🎬"
    homepage: https://github.com/wells1137/kling-video-generator
---
# Kling 3.0 全能视频生成器

该技能支持使用 Kling 3.0 Omni 模型生成和编辑视频。它提供了一种基于用户需求的结构化工作流程来构建 API 请求，确保符合模型复杂的参数限制。

## 参考文件

该技能包含以下参考文件：

- `references/api_reference.md` — **完整的官方 API 参数参考**，包括所有字段、类型、限制条件、互斥规则（R1–R10）、功能矩阵以及调用示例。**在构建任何 API 调用之前，请阅读此文件。**
- `references/prompt_guide.md` — Kling 3.0 Omni 的提示编写原则、官方公式、模板语法以及各种主要场景的示例。
- `scripts/kling_api.py` — 用于 JWT 验证、任务创建和轮询的 Python 实用程序类。

---

## 核心功能

- **文本转视频**：根据文本描述生成视频。
- **图片转视频**：使用描述性提示为静态图片添加动画效果。
- **视频转视频（编辑）**：根据提示修改现有视频（例如，更改主题或风格）。
- **视频转视频（参考）**：使用现有视频作为摄像机运动和风格的参考。
- **多镜头生成**：创建包含多个不同场景的视频。
- **音频生成**：生成带有同步音频的视频，包括语音和音效。

---

## 从用户需求到 API 调用的工作流程

要正确使用 Kling API，必须遵循以下决策工作流程来构建 API 请求数据。该流程分为两个主要阶段：**提示设计** 和 **参数构建**。

### 第一阶段：提示设计

在构建 API 请求之前，首先需要根据用户的需求设计提示。提示的质量是获得良好结果的最关键因素。

1. **查阅提示编写指南**：阅读 `/home/ubuntu/skills/kling-video-generator/references/prompt_guide.md`，以了解编写有效提示的核心原则、官方公式和示例。
2. **确定场景**：判断用户请求的是以下哪种场景：
    - 单镜头视频（从文本、图片或视频生成）
    - 多镜头视频（包含多个场景的故事板）
3. **编写提示**：
    - 对于 **单镜头视频**，按照指南中的公式编写一个详细的提示。
    - 对于 **多镜头视频**，为每个镜头/场景分别编写提示。
    - **使用模板语法**：如果用户提供了参考图片、元素或视频，必须在提示中使用 `<<<image_1>>>`、`<<<element_1>>>`、`<<<video_1>>>` 模板语法来明确引用它们。这是 Omni 模型的核心功能。

### 第二阶段：参数构建

提示准备好后，按照以下决策树构建最终的 API 请求数据。这样可以确保所有通过广泛测试发现的参数限制和相互依赖关系得到遵守。

```mermaid
graph TD
    A[Start] --> B{Multi-shot or Single-shot?};
    B -- Multi-shot --> C[Set `multi_shot: true`];
    B -- Single-shot --> D[Set `multi_shot: false`];

    C --> E{Set `shot_type: "customize"`};
    E --> F[Construct `multi_prompt` array from prompts];
    F --> G[Calculate total duration from `multi_prompt`];
    G --> H[Set top-level `duration`];
    H --> Z[Final Payload];

    D --> I{Video input provided?};
    I -- Yes --> J{Editing or Reference?};
    I -- No --> K[Text/Image-to-Video Path];

    J -- Editing --> L[Set `refer_type: "base"`];
    J -- Reference --> M[Set `refer_type: "feature"`];

    L --> N[Ignore `duration` parameter];
    M --> O[Set `aspect_ratio`];
    N --> P{Audio handling};
    O --> P;

    K --> Q{Audio handling};
    P --> R{Audio handling};

    subgraph R [Audio Handling]
        direction LR
        R1{Want audio output?} -- Yes --> R2[Set `sound: "on"`];
        R1 -- No --> R3[Set `sound: "off"`];
        R2 --> R4{Video input exists?};
        R4 -- Yes --> R5[ERROR: `sound:on` is incompatible with video input];
        R4 -- No --> R6[OK];
    end

    Q --> Z;
    R6 --> Z;
    R3 --> Z;
    R5 --> Stop([Stop/Error]);
```

#### 关键参数规则（来自测试）

以下并非详尽无遗的列表，仅总结了必须遵守的最重要的、不太明显的规则。如需完整指南，请参阅 `prompt_guide.md`。

| 参数 | 规则 |
| :--- | :--- |
| `refer_type` | **必须明确指定**。不要省略。默认值为 `base`，但这种设置并不可靠。编辑时使用 `base`，参考时使用 `feature`。 |
| `duration` | **在 `base` 模式下被忽略**。在 `customize` 模式下，其值必须等于 `multi_prompt` 的总时长。 |
| `sound` | **与 `video_list` 不兼容**。如果提供了参考视频，则不能设置为 `on`。 |
| `shot_type` | **在 `multi_shot: true` 且使用 Omni 模型时，必须设置为 `customize`。`intelligence` 参数不受支持。 |
| `multi_prompt` | **索引必须从 1 开始**。总时长必须与顶层 `duration` 一致。最多支持 6 个镜头。 |
| `aspect_ratio` | **在 `feature` 模式下是必需的**。 |
| `image_list` | 无视频输入时最多支持 7 张图片；有视频输入时最多支持 4 张图片。 |

---

## 执行

要执行视频生成任务，请使用提供的 Python 脚本，该脚本负责处理身份验证和轮询操作。

1. **设置环境变量**：确保 `KLING_ACCESS_KEY` 和 `KLING_SECRET_KEY` 已设置。
2. **构建请求数据**：按照上述工作流程创建用于 API 调用的 JSON 数据。
3. **运行脚本**：

    ```python
    from kling_api import KlingAPI

    # Get keys from environment
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    api = KlingAPI(access_key, secret_key)

    # Your constructed payload
    payload = {
        "model_name": "kling-v3-omni",
        # ... other parameters based on the workflow ...
    }

    # Create and poll the task
    task_response = api.create_omni_video_task(payload)
    if task_response and task_response.get("code") == 0:
        task_id = task_response.get("data", {}).get("task_id")
        print(f"Task created: {task_id}")
        result = api.poll_for_completion(task_id)
        if result:
            print("Final video URL:", result.get("videos", [{}])[0].get("url"))
    ```

这种结构化的方法确保了 Kling 3.0 Omni API 的所有细节和限制条件都能得到正确处理，从而减少错误并提高结果的预测性。