---
name: testflight-seat-monitor
description: 通过智能应用查询和后台批量检查功能，实时监控可用的 TestFlight 测试版名额。当有名额空出时，系统会自动发出提醒。
metadata: {"clawdbot":{"emoji":"🎯","os":["darwin","linux"]}}
---
# TestFlight 座位监控工具

该工具通过智能的应用程序名称查询和静默的批量检查功能，帮助用户实时监控 TestFlight 的测试版名额情况。只有当有新的名额空出时，才会发出警报。

## 功能概述

- **查询 TestFlight 代码**：利用社区数据将代码转换为应用程序名称  
- **检查单个 URL**：立即获取该测试版的可用状态  
- **批量监控**：支持状态跟踪（默认为静默模式）  
- **仅在状态发生变化时发送警报**（例如：从“未可用”变为“可用”）  
- **可配置的监控间隔**（建议设置为 30 分钟至 3 小时）

## 开发背景

TestFlight 的测试版名额通常很快就被抢光。该工具具备以下优势：  
- 可同时监控多个测试版的名额情况  
- 除非状态发生变化，否则不会发出任何警报  
- 使用易于理解的应用程序名称（而非难以理解的代码）  
- 能够持续跟踪各测试版的状态变化  

## 安装方法

```bash
clawhub install testflight-monitor
```

或从 GitHub 克隆代码：  
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/jon-xo/testflight-monitor-skill.git testflight-monitor
cd testflight-monitor
```

## 初始设置

⚠️ **重要提示：** `config/batch-config.json` 文件是用户自定义的配置文件，不包含默认设置。  

### 1. 初始化配置（仅一次）  
```bash
cp config/batch-config.example.json config/batch-config.json
```

### 2. 添加 TestFlight 的 URL  
```bash
./testflight-monitor.sh add https://testflight.apple.com/join/YOUR_CODE_HERE
./testflight-monitor.sh add https://testflight.apple.com/join/ANOTHER_CODE
./testflight-monitor.sh list
```

### 3. 验证工具是否正常工作  
```bash
./testflight-monitor.sh batch
# Output: SILENT: No status changes detected. (or alert if available)
```

## 快速入门  

```bash
# Every hour check
openclaw cron add \
  --name "TestFlight Monitor" \
  --every 60m \
  --target isolated \
  --message "Run TestFlight batch check: ~/.openclaw/workspace/skills/testflight-monitor/testflight-monitor.sh batch. If output contains 'SILENT', reply NO_REPLY. Otherwise announce the findings."
```

### 4. 设置自动化监控（可选，使用 cron 任务）  
```bash
# Check every hour, silent unless slots open
openclaw cron add \
  --name "TestFlight Monitor" \
  --every 60m \
  --target isolated \
  --message "Run: ~/.openclaw/workspace/skills/testflight-monitor/testflight-monitor.sh batch. If output contains 'SILENT', reply NO_REPLY. Otherwise announce the findings."
```

## 命令行接口（CLI）命令  

### 核心命令  

**lookup** `<code>`  
根据 TestFlight 代码查询对应的应用程序名称  
```bash
./testflight-monitor.sh lookup BnjD4BEf
# Output: OpenClaw iOS
```

**check** `<url>`  
检查单个 TestFlight URL 的可用性  
```bash
./testflight-monitor.sh check https://testflight.apple.com/join/BnjD4BEf
# Output: Status: full | App: OpenClaw iOS
```

**batch**  
检查所有配置的 URL（状态发生变化时才会输出结果）  
```bash
./testflight-monitor.sh batch
# Output: SILENT: No status changes detected.
# Or: 🎉 **OpenClaw iOS** beta now has open slots! https://...
```

### 配置命令  

**list**  
显示所有被监控的 URL 及其对应的应用程序名称  
```bash
./testflight-monitor.sh list
```

**add** `<url>`  
将某个 URL 添加到批量监控列表中  
```bash
./testflight-monitor.sh add https://testflight.apple.com/join/Sq8bYSnJ
```

**remove** `<url>`  
从批量监控列表中移除某个 URL  
```bash
./testflight-monitor.sh remove https://testflight.apple.com/join/Sq8bYSnJ
```

**config**  
显示当前的批量监控配置（以 JSON 格式）  
```bash
./testflight-monitor.sh config
```

**state**  
显示每个测试版的当前状态（最后一次获取的状态）  
```bash
./testflight-monitor.sh state
```

### 维护命令  

**update-lookup**  
从 [awesome-testflight-link](https://github.com/pluwen/awesome-testflight-link) 更新查询数据  
```bash
./testflight-monitor.sh update-lookup
# Run weekly to keep app names current
```

## 架构概述  
```
testflight-monitor/
├── testflight-monitor.sh       # Main CLI (entry point)
├── lib/                         # Modular components
│   ├── lookup.sh               # Code → app name resolver
│   ├── check-single.sh         # Single URL checker
│   └── check-batch.sh          # Batch checker (silent mode)
├── config/                      # Configuration & state
│   ├── testflight-codes.json  # Community lookup table (~859 apps)
│   ├── custom-codes.json      # User overrides (private betas)
│   ├── batch-config.json      # Monitoring configuration
│   └── batch-state.json       # State tracking
├── tools/                       # Utilities
│   └── update-lookup.sh       # Refresh lookup table
└── SKILL.md                     # This file
```

## 配置文件  

### batch-config.json  
用户自定义的监控列表。该文件不包含默认设置，需在初始设置时手动创建。  
示例结构：  
```json
{
  "links": [
    "https://testflight.apple.com/join/YOUR_CODE_1",
    "https://testflight.apple.com/join/YOUR_CODE_2"
  ],
  "interval_minutes": 60
}
```

**通过 CLI 进行管理：**  
```bash
./testflight-monitor.sh add <url>
./testflight-monitor.sh remove <url>
./testflight-monitor.sh list
```

**或直接编辑 `config/batch-config.json` 文件**  

### custom-codes.json  
用于添加社区列表中未包含的私有测试版名额：  
```json
{
  "BnjD4BEf": "OpenClaw iOS",
  "YOUR_CODE": "Your App Name"
}
```

## 默认设置为静默模式  

批量监控工具仅在状态发生变化时才会输出结果：  
- **从“未可用”变为“可用”**：会发出警报  
- **从“可用”变为“已占用”**：保持静默  
- **从“可用”变为“已占用”**：保持静默（表示您已经申请了该名额，或错过了申请机会）  
这种设计既避免了不必要的通知干扰，又能确保您及时获取信息。  

## 数据来源  

- **查询数据源**：[awesome-testflight-link](https://github.com/pluwen/awesome-testflight-link)  
  一个由社区维护的、包含 800 多个公开 TestFlight 测试版的列表  
  通过 `update-lookup` 命令定期更新  
  建议每周更新一次  

- **自定义代码**：用户可以在 `config/custom-codes.json` 中添加未包含在社区列表中的私有测试版名额  
  这些测试版的优先级高于社区列表中的测试版  

## 所需依赖库/工具  

- `curl`：用于获取 TestFlight 页面内容  
- `jq`：用于处理 JSON 数据  
- `bash`：用于脚本编写（适用于 macOS/Linux 系统）  

## 使用示例  

### 监控 OpenClaw iOS 测试版名额  
```bash
cd ~/.openclaw/workspace/skills/testflight-monitor
./testflight-monitor.sh add https://testflight.apple.com/join/BnjD4BEf
./testflight-monitor.sh batch
```

### 同时检查多个测试版名额  
```bash
./testflight-monitor.sh add https://testflight.apple.com/join/Sq8bYSnJ  # Duolingo
./testflight-monitor.sh add https://testflight.apple.com/join/b9jMyOWt  # Reddit
./testflight-monitor.sh list
```

### 手动检查测试版状态  
```bash
./testflight-monitor.sh check https://testflight.apple.com/join/BnjD4BEf
```

## 贡献方式  

- **GitHub 仓库**：[https://github.com/jon-xo/testflight-monitor-skill**  
  可提交问题或请求新功能  
- **Pull Request**：欢迎提出改进建议  

## 许可证  

本工具采用 MIT 许可证，请参阅 `LICENSE` 文件。  

## 致谢  

- 该工具专为 [OpenClaw](https://openclaw.ai) 开发  
- 数据查询功能基于 [awesome-testflight-link](https://github.com/pluwen/awesome-testflight-link)  
- 开发灵感来源于用户希望在不接收过多通知的情况下及时获取测试版名额的需求  

## 版本历史  

**1.0.0**（2026-02-11）  
- 首次发布  
- 整合了查询、单个检查及批量监控功能  
- 默认采用静默模式  
- 支持通过 CLI 进行配置  
- 集成了社区维护的查询数据源  

---

（注：由于提供的 SKILL.md 文件内容较长，部分代码块（如 ````bash
clawhub install testflight-monitor
````）在实际翻译中可能被省略或简化。在实际应用中，这些代码块应包含具体的实现细节。）