# OpenClaw 配置验证工具

**ID**: `openclaw-config-validator`  
**版本**: 1.0.0  
**OpenClaw 版本**: 2026.2.1+  

这是一个用于 OpenClaw 的全面配置验证和管理工具，提供权威的配置规范文档、验证工具以及最佳实践指南。

---

## 概述  

该工具帮助 OpenClaw 代理和用户：  
- 理解完整的 OpenClaw 配置规范  
- 根据官方 JSON 规范验证配置  
- 遵循安全的配置管理实践  
- 预防常见的配置错误  

---

## 功能  

### 📚 完整的规范参考  
- 文档中包含了 **22 个顶级配置节点**  
- 使用 OpenClaw 2026.2.1 的官方 JSON 规范  
- 每个节点都标明了 **风险等级**（🟢 低风险 🟡 中等 🔴 高风险）  
- 包含字段类型、默认值及示例  

### ✅ 验证工具  
- `get-schema.sh`：从运行时配置中提取配置规范  
- `schema-validate.sh`：根据规范验证配置  
- 提供提交前的检查列表以防止错误  

### 🛡️ 安全特性  
- **禁用字段列表**：明确指出不能添加的字段  
- **修改前检查流程**：7 步安全操作流程  
- **回滚机制**：出现问题时可以恢复配置  
- **错误排查**：提供常见问题的解决方案  

---

## 快速入门  

### 1. 验证当前配置  
```bash
./scripts/schema-validate.sh
```  

### 2. 提取运行时配置规范  
```bash
./scripts/get-schema.sh
```  

### 3. 阅读规范参考  
```bash
cat reference/SCHEMA.md
```  

---

## 文件结构  
```
openclaw-config-validator/
├── SKILL.md                          # This file
├── reference/
│   ├── SCHEMA.md                     # Authoritative schema reference (v2)
│   ├── openclaw-official-schema.json # Official JSON Schema from OpenClaw
│   └── AGENT_PROMPT.md              # Configuration management guide
└── scripts/
    ├── get-schema.sh                # Runtime schema extractor
    └── schema-validate.sh           # Configuration validator
```  

---

## 配置安全规则  

### ✅ 必须执行的操作  
- 在进行任何修改之前，请先阅读 `SCHEMA.md`  
- 备份配置文件：`cp ~/.openclaw/openclaw.json ~/.openclaw.json.backup.$(date +%s)`  
- 使用 `jq` 进行修改，切勿直接编辑文件  
- 修改前后运行 `openclaw doctor` 命令  
- 先在非生产环境中进行测试  

### ❌ 禁止的操作  
- 不要在 `SCHEMA.md` 中创建新的顶级配置节点  
- 不要添加不存在的字段（如 `web.braveApiKey`）  
- 不要修改 `gateway` 节点（该节点为只读属性）  
- 请务必执行备份操作  
- 不要随意猜测字段的名称或格式  

---

## 规范亮点  

### OpenClaw 2026.2.1 的新功能  
| 节点 | 功能 | 状态 |  
|------|---------|--------|  
| `logging` | 日志配置 | ✅ 已记录在文档中 |  
| `talk` | 语音模式（macOS/iOS/Android） | ✅ 已记录在文档中 |  
| `audio` | 音频/TTS/语音唤醒 | ✅ 已记录在文档中 |  
| `bindings` | 多代理路由 | ✅ 已记录在文档中 |  
| `diagnostics` | OpenTelemetry 集成 | ✅ 已记录在文档中 |  
| `update` | 自动更新设置 | ✅ 已记录在文档中 |  

### 风险等级  
| 风险等级 | 受影响的节点 | 需要采取的措施 |  
|-------|-------|-----------------|  
| 🟢 低风险 | 大多数节点 | 保持常规谨慎操作 |  
| 🟡 中等风险 | `channels` | 修改前请备份配置 |  
| 🔴 高风险 | `gateway` | 该节点为只读节点，禁止修改 |  

---

## 验证方法  

### 使用 `schema-validate.sh`  
```bash
# Basic validation
./scripts/schema-validate.sh

# Detailed report
./scripts/schema-validate.sh --verbose

# Generate report file
./scripts/schema-validate.sh --report
```  

### （可选）使用 Ajv 进行验证  
```bash
# Install ajv-cli
npm install -g ajv-cli

# Validate with official schema
ajv validate -s reference/openclaw-official-schema.json \
  -d ~/.openclaw/openclaw.json
```  

---

## 故障排查  

### 配置验证失败  
```bash
# 1. Check specific errors
openclaw doctor

# 2. Restore from backup
cp ~/.openclaw/openclaw.json.backup.* ~/.openclaw/openclaw.json

# 3. Restart gateway (if needed)
openclaw gateway restart
```  

### Gateway 无法启动  
```bash
# Check config syntax
jq '.' ~/.openclaw/openclaw.json

# If invalid, restore default
mv ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.broken
# Then re-run: openclaw onboard
```  

---

## 参考资源  
- **官方文档**: https://docs.openclaw.ai/gateway/configuration  
- **OpenClaw 仓库**: https://github.com/openclaw/openclaw  
- **OpenClaw Discord 频道**: https://discord.gg/clawd  

---

## 更新记录  

### v1.0.0 (2026-02-04)  
- 初始版本发布  
- 完整记录了 OpenClaw 2026.2.1 的配置规范  
- 集成了官方 JSON 规范  
- 提供了验证脚本  
- 添加了安全指南和检查列表  

---

## 许可证  
MIT 许可证——详情请参阅 OpenClaw 项目文档。  

---

**“规范是界限，而非许可。请明确了解这些界限。”**  
*由 Galatea 创作 🜁*