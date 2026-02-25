---
name: openclaw-starter-kit
description: OpenClaw 入门者全套入门指南：从首次设置到安全强化，提供全程互动式指导。该指南会响应以下关键词：“初始设置”（initial settings）、“首次配置”（first setup）、“入门套件”（starter kit）、“系统集成”（onboarding）、“设置指南”（setup guide）、“开始使用”（get started）以及“帮助设置”（help with setup）。
---
# OpenClaw 入门套件 🚀

专为 OpenClaw 新用户准备的 **一站式入门指南**。通过交互式引导，系统会自动生成所有核心配置文件。

## 关键术语
- **初始设置** (Initial Setup)
- **启动套件** (Starter Kit)
- **安全设置** (Security Setup)
- **配置报告** (Configuration Report)
- **技能安装** (Skill Installation)
- **任务提醒** (Task Reminder)

## 执行流程

### 第一阶段：基础设置（交互式）

**步骤 1 — SOUL.md（代理设置）**
向用户提出 5 个问题：
1. “代理的名字叫什么？”
2. “使用什么语气？（随意/正式/亲切/专业）”
3. “主要职责是什么？（秘书/编程助手/学习伙伴/多用途）”
4. “有哪些禁止事项？”
5. “选择哪个代表图标？”

根据用户的回答，参考 `templates/soul-template.md` 生成 `SOUL.md` 文件，并在用户确认后保存。

**步骤 2 — USER.md（用户信息）**
收集以下信息：
- 名字
- 称呼
- 职业/兴趣爱好
- 时区（默认：Asia/Seoul）
- 特殊要求/偏好设置

参考 `templates/user-template.md` 生成相应的用户配置文件。

**步骤 3 — 内存结构设置**
系统会自动生成相关配置文件（代码示例见 **```
~/.openclaw/workspace/
├── MEMORY.md              ← 장기 기억 인덱스
├── memory/
│   ├── YYYY-MM-DD.md      ← 일일 로그 (첫 날 자동 생성)
│   ├── knowledge/          ← 학습 자료
│   ├── projects/           ← 프로젝트 기록
│   └── lessons/            ← 실수/교훈
```**），基于 `templates/memory-template.md` 模板。

**步骤 4 — HEARTBEAT.md（自动登录功能）**
在说明用途后，使用默认模板生成以下内容：
- 天气查询
- 任务提醒
- 可根据用户需求添加个性化内容

文件基于 `templates/heartbeat-template.md` 模板生成。

### 第二阶段：技能与工具配置

**步骤 5 — Brave Search API**
1. 提供注册 Brave Search API 的指南（免费，每月使用 2000 次）
2. 获取 API 密钥后，指导用户执行 `openclaw configure --section web` 命令进行配置
3. 确认配置是否正确。

**步骤 6 — 推荐技能安装**
根据不同用途，参考 `guides/skill-recommendations.md` 安装相应技能：
| 用途 | 技能名称 | 命令 |
|------|------|--------|
| 网页搜索 | Brave API | `openclaw skills install web` |
| 天气查询 | weather | `openclaw skills install weather` |
| 文本摘要 | summarize | `openclaw skills install summarize` |
| GitHub 信息 | github | `openclaw skills install github` |
| YouTube 字幕下载 | youtube-transcript | `openclaw skills install youtube-transcript` |

**步骤 7 — Cron 任务基础**
参考 `guides/cron-basics.md` 了解 Cron 任务的基本使用方法：
- 了解 Heartbeat 与 Cron 的区别
- 示例：设置“每天早上 9 点发送提醒”
- 提供配置指南。

### 第三阶段：安全强化

**步骤 8 — 安全设置（必读）**
参考 `guides/security-guide.md` 进行安全配置：
1. **API 密钥管理**
   - 绝不要将 API 密钥写入 `SOUL.md` 或 `USER.md`
   - 通过环境变量或 `openclaw configure` 进行管理
   - 将 `.env` 文件添加到 `.gitignore` 文件中
2. **外部行为控制**
   - 设置邮件/SNS 发送的审批机制
   - 使用 `openclaw configure --section security` 进行配置
   - 仅允许特定的号码或频道发送消息
3. **文件安全**
   - 使用 `trash` 替代 `rm` 删除文件（可恢复）
   - 保护敏感信息
   - 明确指定代理的访问权限
4. **频道安全**
   - 在 Telegram 中仅允许指定号码发送消息
   - 限制代理在群聊中的发言范围
   - 拒绝来自陌生人的消息
5. **网络安全**
   - 防止 API 密钥泄露
   - 注意在公共 WiFi 下使用仪表板
   - 定期运行 `openclaw health` 检查系统状态
6. **数据安全**
   - 遵守个人信息保护原则
   - 定期备份 `memory/` 目录
   - 在共享数据时隐藏敏感信息

### 第四阶段：总结

**步骤 9 — 生成配置报告**
系统会自动扫描当前配置状态并生成报告（代码示例见 **```
✅ 세팅 완료 리포트
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 설치된 스킬: [자동 감지]
🤖 에이전트: [이름] ([모델])
📡 채널: [연결된 채널]
🔍 웹 검색: [활성/비활성]
📂 워크스페이스: [경로]
📝 SOUL.md: [✅/❌]
👤 USER.md: [✅/❌]
🧠 MEMORY.md: [✅/❌]
💓 HEARTBEAT.md: [✅/❌]
🔒 보안: [allowlist 설정 여부]
⏰ 크론잡: [설정 수]

세팅 담당: [설정자 이름]
세팅 일자: [오늘 날짜]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```**）。

**步骤 10 — 高级功能指南**
参考 `guides/advanced-roadmap.md` 了解高级功能：
- 多频道连接
- 使用子代理
- 构建向量数据库（RAG）
- 自定义技能开发

### 故障排除
参考 `guides/troubleshooting.md` 解决常见问题：
- “Gateway 无法启动？” → 执行 `openclaw doctor`
- “机器人无响应？” → 检查 API 密钥和允许列表
- “技能安装失败？” → 确认 Node.js 版本

## 文件结构
文件结构如下（代码示例见 **```
openclaw-starter-kit/
├── SKILL.md
├── templates/
│   ├── soul-template.md
│   ├── user-template.md
│   ├── memory-template.md
│   ├── heartbeat-template.md
│   └── agents-template.md
├── guides/
│   ├── skill-recommendations.md
│   ├── cron-basics.md
│   ├── security-guide.md
│   ├── advanced-roadmap.md
│   └── troubleshooting.md
└── package.json
```**）：