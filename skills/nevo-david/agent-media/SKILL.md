---
name: agent-media
description: 使用 `agent-media` CLI 通过终端进行 AI 生成的UGC（用户生成内容）视频制作。
homepage: https://github.com/gitroomhq/agent-media
metadata: {"clawdbot":{"emoji":"🌎","requires":{"bins":[],"env":[]}}}
---
### npm 发布：  
https://www.npmjs.com/package/agent-media-cli  
### agent-media CLI 的 GitHub 仓库：  
https://github.com/gitroomhq/agent-media  
### 官方网站：  
https://agent-media.ai  

#### agent-media — 人工智能生成的UGC视频与媒体内容  

使用 `agent-media` CLI，您可以从终端直接生成完整的用户生成内容（UGC）视频和SaaS产品评测视频。  

---

#### 强制性规则（每个命令执行前请务必阅读）  

**您必须遵守所有这些规则。违反任何规则都会导致视频无法正常播放或观看效果不佳。**  

### 规则 1：**始终使用 `--actor` 参数**  
每个UGC视频都必须包含 `--actor <slug>` 参数。如果没有指定演员，视频将只有静态图像和旁白，没有人物出镜。如果用户未指定演员，请让他们选择一个，或者默认使用 `sofia` 或 `naomi` 等常见角色。运行 `agent-media actor list` 可以查看可用角色列表。  

### 规则 2：**严格控制字数**  
自然语言的朗读速度约为每秒2.5个单词。脚本的字数必须符合以下时长要求：  
- **5秒视频** → 最多12个单词  
- **10秒视频** → 最多25个单词  
- **15秒视频** → 最多37个单词  
如果用户提供的脚本字数过多，您必须重新编写以符合时长要求。字数过多的脚本会导致朗读效果不自然或失去同步效果。切勿提交超出字数限制的脚本。  

### 规则 3：**SaaS评测视频必须包含截图**  
对于任何SaaS产品评测视频，您必须通过 `--broll --broll-images` 参数提供1-3张产品截图。没有截图的话，观众将无法了解产品的实际使用情况（只能看到说话者的画面）。  
`--broll-images` 支持 **HTTP/HTTPS链接** 和 **本地文件路径**（本地文件会自动上传）。系统会根据文件名自动将图片与视频中的场景匹配：  
- 示例：`--broll-images ./dashboard.png,./calendar-view.png`（本地文件）  
- `--broll-images https://example.com/pricing-page.png,https://example.com/editor.png`（URL链接）  
- 两者混合使用也可以。  

### 规则 4：**SaaS评测视频必须包含产品名称**  
请用户提供产品名称。脚本中必须包含产品名称，以便在字幕中显示。  

### 规则 5：**始终使用 `--sync` 参数**  
执行命令时务必添加 `--sync` 参数，以确保命令完成并获取输出视频的URL。  

### 规则 6：**为截图文件起描述性名称**  
截图文件名应具有描述性，以便AI能够正确匹配到相应的场景：  
- **示例**：`dashboard.png`（仪表盘截图）、`calendar-view.png`（日历界面截图）、`post-editor.png`（编辑器界面截图）  

---

#### 先决条件  
**必须先安装并登录 `agent-media` CLI：**  
使用 `agent-media whoami` 命令进行验证。如果未登录，请运行 `agent-media login` 并按照提示完成身份验证。  

#### UGC流程（核心功能）  
`agent-media` 可将脚本转换为包含AI配音、背景画面、动画字幕的完整视频，只需一个命令即可完成整个制作流程。  

### 基本UGC功能（代码示例）  

---

#### 带背景画面的UGC功能（代码示例）  

---

#### UGC相关选项  

| 选项 | 说明 | 示例 |
|------|-------------|---------|
| `--actor <slug>` | 选择用于配音的演员角色 | `--actor sofia` |
| `--persona <slug>` | 自定义人物角色（克隆声音+面部模型） | `--persona brand-voice` |
| `--face-url <url>` | 人脸照片的URL或本地文件路径 | `--face-url ./photo.png` |
| `--voice <name>` | 语音合成引擎 | `--voice nova` |
| `--tone <name>` | 语音语调（活力、平静、自信、戏剧性） | `--tone energetic` |
| `--style <name>` | 字幕样式（默认：hormozi） | `--style bold` |
| `--duration <s>` | 视频时长（5秒、10秒或15秒） | `--duration 10` |
| `--aspect <ratio>` | 屏幕比例（9:16、16:9、1:1） | `--aspect 16:9` |
| `--music <genre>` | 背景音乐类型（轻松、活力、正式、戏剧性、欢快） | `--music chill` |
| `--cta <text>` | 结尾页的呼叫行动文本 | `--cta "了解更多"` |
| `--broll` | 启用背景画面功能 | `--broll` |
| `--broll-images <urls>` | 背景画面的URL列表（用逗号分隔） | `--broll-images url1,url2` |
| `--template <slug>` | 脚本模板 | `--template saas-review` |
| `-g, --generate-script <prompt>` | 根据描述自动生成脚本 | `-g "yoga mat product"` |
| `--product-url <url>` | 用于生成脚本的产品链接 | `--product-url https://...` |
| `--s, --sync` | 等待命令完成并获取输出URL | `--sync` |

#### 脚本模板  
以下是几种常用的脚本模板：  
- **monologue**：直接面向镜头的独白  
- **testimonial**：问题→解决方案→结果→呼叫行动  
- **product-review**：产品介绍→使用体验→评价→呼叫行动  
- **problem-solution**：问题→痛点→解决方案→呼叫行动  
- **saas-review**：产品使用流程→评价→呼叫行动  
- **before-after**：使用前后的对比  
- **listicle**：多个小贴士→呼叫行动  
- **product-demo**：产品演示→总结→呼叫行动  

#### 字幕样式  
可选的字幕样式：  
- **hormozi**（黄色高亮效果，默认样式）  
- **minimal**（简洁风格）  
- **bold**（霓虹蓝风格）  
- **karaoke**（绿色流行风格）  
- **clean**（白色背景）  
- **tiktok**（简洁风格）  
- **neon**（鲜艳风格）  

#### SaaS评测视频  
生成完整的SaaS产品评测视频。**必须满足以下四个条件：**  
1. 脚本中包含产品名称（以便在字幕中显示）  
2. 使用 `--actor` 参数指定配音演员  
3. 通过 `--broll --broll-images` 提供1-3张产品截图  
4. 脚本字数符合时长要求（每秒2.5个单词）  

#### 操作步骤（请严格按照以下步骤执行）：  
1. 获取产品名称（如用户未提供，请询问）。  
2. 获取1-3张产品截图（用户提供URL时直接使用；否则访问产品网站提取截图）。  
3. 选择配音演员（默认使用 `naomi` 或 `sofia`）。  
4. 编写脚本（10秒视频最多25个单词，15秒视频最多37个单词，务必提及产品名称）。  
5. 使用所有必要的参数运行命令：  

---

#### 其他选项说明：  

| 选项 | 说明 | 示例 |
|------|-------------|---------|
| `--cta <text>` | 结尾页的呼叫行动文本 | `--cta "立即尝试"` |
| `-d, --duration <s>` | 视频时长（5秒、10秒或15秒） | `--duration 10` |
| `-g, --generate-script <prompt>` | 根据描述自动生成脚本 | `-g "瑜伽垫产品"` |
| `-s, --sync` | 等待命令完成并获取输出URL | `--sync` |

#### 人物角色管理  
您可以保存不同角色的语音和面部数据，以便在多个视频中重复使用。  

#### 为视频添加字幕  

---

#### 定价方案  
| 订阅计划 | 价格 | 每月信用点数 | 可制作的10秒视频数量 |
|------|-------|-----------------|-------------|
| Creator | $39/月 | 2,500信用点 | 约3个视频 |
| Pro | $69/月 | 5,000信用点 | 约6个视频 |
| Pro Plus | $129/月 | 10,000信用点 | 约12个视频 |
| 每10秒视频约需要800信用点。也可选择按需购买的信用点包。使用 `agent-media credits` 命令查看剩余信用点数。 |

#### 任务管理  

#### 账户信息  

---

#### 在执行任何UGC相关命令前请检查以下内容：  
- 是否指定了配音演员（`--actor` 参数）  
- 脚本字数是否符合时长要求  
- 是否添加了 `--sync` 参数  
- 对于SaaS评测视频，是否使用了 `--broll --broll-images` 以及1-3张产品截图  
- 脚本中是否包含了产品名称  
- 是否有足够的信用点数（使用 `agent-media credits` 命令查看余额）