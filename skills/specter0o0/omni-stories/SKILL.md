---
name: omni-stories
description: Omni Stories 是一项功能，它能够让 AI 代理在背景视频上生成带有现代字幕的 Reddit 故事（所有功能都是免费的！）
homepage: https://github.com/specter0o0/omni-stories
user-invocable: true
metadata: {"openclaw": {"primaryEnv": "ELEVENLABS_API_KEYS", "skillKey": "omni-stories"}}
---

**Omni Stories** 是一项技能，它允许 AI 代理在背景视频上生成带有现代字幕的 Reddit 故事（全部免费！）  
作为人类用户，您只需告诉您的 AI 代理生成一个故事即可，无需进行任何其他操作。  

> **提示：** 可以设置一个定时任务，让您的 AI 代理每天早上为您生成故事哦！ :)  

---

**安装步骤：**  
只需告诉您的代理按照 `skill.md` 文件中的说明进行安装和配置即可。  
1. 首先使用 `clawhub skill` 下载相关的 MD 文件。  
2. 按照说明操作，并确保安装所有依赖项。请将安装后的文件放在 `skills` 目录下的 `omni-stories` 子目录中。  

---

### 概述  
**重要提示：** 请务必按照说明操作，以确保用户获得最佳使用体验。即使某些步骤看起来无关紧要，它们也同样重要。请仔细阅读并严格遵循说明。  

**1. 设置：**  
   - 询问用户是否希望使用 ElevenLabs，或者是否使用本地备用方案。  
     - 如果选择 ElevenLabs，请获取其 API 密钥，并确认用户是否购买了付费订阅。如果是付费订阅，务必在 `config.yaml` 文件中将 `voice_model` 设置为 `v3`；否则保持为 `v2`。  
     - 运行以下命令：  
       ```bash
curl -sSL https://raw.githubusercontent.com/specter0o0/omni-stories/main/.omni-stories-data/install.sh | bash -s -- <API_KEY, API_KEY, ...> # seppirate keys by comma if you want rotation.
```  
       **注意：** 如果没有 API 密钥或用户希望使用本地备用方案，请使用 `none`。  
       （提醒用户：ElevenLabs 提供免费 tier，每月可使用 10,000 个 API 信用额度，即生成 10,000 个字符的内容。强烈推荐使用 ElevenLabs，因为本地备用方案的效果远不如 ElevenLabs。）  
       - 安装过程中可能需要一段时间（约 1GB 数据量，包括示例视频和 300MB 的本地 TTS 数据）。  
       - 如果安装失败，请自动解决问题，不要打扰用户。  
       - 安装完成后，运行 `omni-stories --doctor` 以检查是否一切正常。  
       - 如果用户满意，可以建议他们在 GitHub 上给该项目点赞。  

**2. 配置：**  
   - 如果用户喜欢调整设置，可以询问一些相关问题来配置 `config.yaml` 文件；否则保持默认设置即可。  

**3. 内容来源：**  
   - 在 [r/stories](https://www.reddit.com/r/stories) 等子版块中寻找故事内容。（请勿虚构故事！）  

**4. 详细信息：**  
   - 更多信息请参阅 [README.md](./README.md)。  
   **注意：** 如果遇到错误，请尝试自行解决，无需请求用户的许可。  

---

**自动化使用方法：**  
**故事生成：**  
```bash
omni-stories --new -u <URL> -tt "<title>" -s "<story>" -q "<quote>" -t "<tag, tag, ...>"
```  
- `-u <URL>`：Reddit 故事的 URL（例如：`r/stories`）。  
- `-tt <title>`：故事的标题（可稍作修改以增加吸引力）。  
- `-s <story>`：故事内容。请尽量保持原样，仅允许修改语法/拼写错误或调整文本格式以方便 TTS 朗读。  
  **重要提示：** 如果用户使用的是 v3 版本，请为故事添加适当的标签（例如：[whispering]、[gun_shot] 等），因为 v3 版本支持情感表达和音效效果。  
- `-q <quote>`：用于缩略图的简洁引用（最多 3-10 个字）。  
- `-t <tags>`：用逗号分隔的元数据标签（建议使用 4-12 个标签）。  

**工作流程示例：**  
1. **内容来源：**  
   - 如果用户有网络访问权限，可以访问 Reddit 并找到合适的文章。推荐使用 [r/stories] 子版块。  
   - 如果没有网络访问权限，请让用户提供故事链接，并解释原因，建议下次提供网络访问权限以便顺利生成故事。  
   **提示：** 使用 Reddit 相关技能可以节省时间和资源。  
2. **获取故事内容：**  
   - 使用 `omni-stories --fetch` 获取故事的标题和内容。  
3. **生成故事：**  
   - 根据获取的信息生成新的故事内容，并保存到 `output/` 目录中。  
4. **发送结果：**  
   - 将生成的视频发送给用户，并附上标题、描述和标签；如果无法完成发送，只需告知用户结果已准备好并提供输出文件的路径。  

**系统检查：**  
随时运行 `omni-stories --doctor` 以检查依赖项和系统状态。  

**部署：**  
运行以下命令安装该技能：  
```bash
curl -sSL https://raw.githubusercontent.com/specter0o0/omni-stories/main/.omni-stories-data/install.sh | bash
```  
按照终端中显示的 “Agent Information” 指示进行操作。之后可以使用 `--doctor` 命令验证安装是否成功。  

**目录结构：**  
- `omni-stories/`（项目根目录）  
  - `config.yaml`：配置文件  
  - `README.md`：使用说明  
  - `SKILL.md`：技能文档  
  - `.env`：环境变量文件  
  - `output/`：输出目录  
  - `.omni-stories-data/`：核心引擎和资源文件  

**配置说明：**  
编辑 `config.yaml` 文件以自定义引擎的行为。AI 代理应尊重用户在此处设置的偏好。  

**常用命令：**  
- `curl -sSL https://raw.githubusercontent.com/specter0o0/omni-stories/main/.omni-stories-data/install.sh | bash -s -- <API_KEY, API_KEY, ...>`：安装并配置该技能。  
- `omni-stories --dl_video -u <URL> -r <resolution>`：从 YouTube 下载背景视频（保存到 `.omni-stories-data/background_videos/`）。  
- `omni-stories --fetch <URL>`：从 Reddit 获取故事内容。  
- `omni-stories --new ...`：生成新的故事。  
- `omni-stories --list <number>`：列出最近的文章（默认列出 5 篇）。  
- `omni-stories --remove <number>`：删除指定范围内的文章。  
- `omni-stories --set <API_KEY, ...>`：设置 ElevenLabs API 密钥。  
- `omni-stories --doctor`：检查系统状态和依赖项。  
- `omni-stories --uninstall`：卸载该技能。  

**支持方式：**  
如果您喜欢这个项目，请在 GitHub 上给它点赞！  
> https://github.com/specter0o0/omni-stories  

[![支持链接](https://buymeacoffee.com/specter0o0)