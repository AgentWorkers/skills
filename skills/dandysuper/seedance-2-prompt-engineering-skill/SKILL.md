# Seedance 2.0 JiMeng 技能（OpenClaw / ClawHub）

## 目的  
使用多模态参考资料（图像/视频/音频/文本）为 **Seedance 2.0** 和 **Seedance 2.0 Fast** 创建高控制性的英文提示。  
该技能适用于：  
- 从初步构思到生成可用的提示的整个过程  
- 模式选择：**仅使用首帧/尾帧** 或 **使用所有参考资料**  
- `@asset` 映射（每个图像/视频/音频的控制内容）  
- 视频片段时长规划（4-15秒）及时间线安排  
- 视频片段扩展/续接提示  
- 角色替换及定向编辑提示  
- 根据参考视频复制摄像机动作和语言表达  

---

## 核心规则  
1. 必须首先声明所使用的模式。  
2. 必须包含明确的 **资产映射** 部分。  
3. 使用带有时间标记的节奏提示，每个片段包含一个主要动作。  
4. 保持提示的简洁性和可操控性（避免使用模糊的、仅具有诗意的表述）。  
5. 当用户需要清晰、精确的输出时，应添加相应的限制条件。  

---

## 平台限制（Seedance 2.0）  
- 输入文件类型（图像+视频+音频）：**最多12个文件**  
- 图像格式：jpeg/png/webp/bmp/tiff/gif，**最多9张**，每张文件大小不超过30MB  
- 视频格式：mp4/mov，**最多3个**，总时长不超过2-15秒，总文件大小不超过50MB  
- 音频格式：mp3/wav，**最多3个**，总时长不超过15秒，总文件大小不超过15MB  
- 生成时长：**4-15秒**  
- 平台政策可能限制使用真实的人脸参考资料。  

---

## 输出格式（默认格式）  
1. **使用的模式**  
2. **资产映射**  
3. **最终生成的提示内容**  
4. **需要遵守的限制条件**  
5. **生成设置**  

示例模板：  
```text
Mode: All-Reference
Assets Mapping:
- @image1: first frame / identity anchor
- @video1: camera language + motion rhythm
- @audio1: optional soundtrack pacing

Final Prompt:
[ratio], [duration], [style].
0-3s: [action + camera].
3-7s: [action + transition].
7-10s: [reveal/climax + end frame].
Preserve identity and scene continuity. Use physically plausible motion and coherent lighting.

Negative Constraints:
no watermark, no logo, no subtitles, no on-screen text.

Generation Settings:
Duration: 10s
Aspect Ratio: 9:16
```  

---

## 特殊情况  
### A) 视频片段扩展  
明确说明：`将 @video1 的时长延长 X 秒`。  
生成的时长应等于新增片段的时长，而非最终视频的总时长。  

### B) 角色替换  
将基础动作/摄像机动作绑定到 `@video1`，将替换后的角色形象绑定到 `@image1`，并要求严格保持动作和时序的一致性。  

### C) 节奏同步  
使用 `@video`/`@audio` 中的节奏参考资料，并根据时间范围锁定各个片段的节奏。  

---

## 该技能相关的文件  
- `SKILL.md` — 主要技能逻辑文件  
- `SKILL.sh` — 用于本地快速测试的辅助脚本  
- `scripts/setup_seedance_prompt_workspace.sh` — 帮助搭建工作区的脚本  
- `references/recipes.md` — 可直接使用的提示模板  
- `references/modes-and-recipes.md` — 模式与控制方式的详细说明