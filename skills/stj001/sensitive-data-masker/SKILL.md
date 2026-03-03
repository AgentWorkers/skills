---
name: sensitive-data-masker
description: 智能的敏感数据检测与屏蔽功能。结合使用 Microsoft Presidio 和 SQLite 实现个人身份信息（PII）的自动脱敏处理，并支持数据的本地恢复。
homepage: https://gitee.com/subline/onepeace/tree/develop/src/skills/sensitive-data-masker
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "events": ["message:received"],
        "requires": { 
          "bins": ["python3"],
          "python_packages": ["presidio-analyzer", "presidio-anonymizer", "spacy"]
        },
        "install": [
          {
            "id": "pip",
            "kind": "pip",
            "package": "presidio-analyzer presidio-anonymizer",
            "label": "Install Microsoft Presidio"
          },
          {
            "id": "spacy",
            "kind": "pip",
            "package": "spacy",
            "label": "Install spaCy NLP"
          },
          {
            "id": "spacy-model",
            "kind": "command",
            "command": "python3 -m spacy download zh_core_web_sm",
            "label": "Download Chinese NLP model"
          }
        ]
      }
  }
---
# 敏感数据掩码器

使用 Microsoft Presidio 结合 SQLite 和 LRU 缓存实现智能的敏感数据检测与掩码处理。

## 特点

- ✅ **智能检测** - 基于 Microsoft Presidio（自然语言处理 + 规则）
- ✅ **快速存储** - 使用 SQLite 和 LRU 缓存
- ✅ **本地恢复** - 7 天的临时映射表
- ✅ **自动清理** - 过期条目会自动删除
- ✅ **100% 本地处理** - 无需外部 API
- ✅ **OpenClaw 插件** - 收到消息时自动进行掩码处理

## 工作原理

```
User Message
    ↓
Channel Plugin (Feishu/Telegram/etc)
    ↓
OpenClaw Gateway (message:received)
    ↓
Sensitive Data Masker Hook ← Intercept here
    ↓
Presidio Detection (NLP + Rules)
    ↓
SQLite + Cache Store Mapping
    ↓
Masked Message
    ↓
Send to LLM API (Safe)
    ↓
Restore Before Task Execution
    ↓
Execute with Original Data
```

## 检测类型

| 类型 | 示例 | 掩码后的形式 |
|------|----------|-----------|
| **密码** | `password=MySecret123` | `[PASSWORD:xxx]` |
| **API 密钥** | `sk-abcdefghijklmnop` | `[API_KEY:xxx]` |
| **令牌** | `token=xyz123` | `[TOKEN:xxx]` |
| **秘密信息** | `secret=abc+/==` | `[SECRET:xxx]` |
| **私钥** | `BEGIN RSA PRIVATE KEY` | `[PRIVATE_KEY:xxx]` |
| **数据库连接信息** | `mongodb://user:pass@host` | `[DB_CONNECTION:xxx]` |
| **电子邮件地址** | `user@example.com` | `[EMAIL_ADDRESS:xxx]` |
| **电话号码** | `13800138000` | `[PHONE_NUMBER:xxx]` |
| **信用卡号** | `4111111111111111` | `[CREDIT_CARD:xxx]` |
| **人员姓名** | John Doe | `[PERSON:xxx]` |
| **地址** | 123 Main St | `[LOCATION:xxx]` |
| **URL** | `https://example.com` | `[URL:xxx]` |

## 安装

```bash
# Install dependencies
pip install presidio-analyzer presidio-anonymizer
python3 -m spacy download zh_core_web_sm

# Enable Hook
openclaw hooks enable sensitive-data-masker

# Verify
openclaw hooks check
```

## 使用示例

### 用户发送数据：
```
My password is MySecret123, email is user@example.com
```

### 数据被掩码后发送给 API：
```
My password is [PASSWORD:f2ae1ea6], email is [EMAIL_ADDRESS:96770696]
```

### 数据存储（有效期 7 天）：
```json
{
  "f2ae1ea6": "password=MySecret123",
  "96770696": "user@example.com"
}
```

### 本地数据恢复（用于任务执行）：
```
My password is MySecret123, email is user@example.com
```

## 配置

**配置文件**: `~/.openclaw/data/sensitive-masker/config.json`

```json
{
  "enabled": true,
  "ttl_days": 7,
  "cache_size": 1000,
  "auto_cleanup": true,
  "cleanup_interval_hours": 1,
  "log_enabled": true,
  "encrypt_storage": false,
  "presidio": {
    "language": "zh",
    "entities": ["PHONE_NUMBER", "EMAIL_ADDRESS", ...],
    "custom_patterns": true
  }
}
```

## 管理命令

```bash
# Test masking
python3 sensitive-masker.py test "my password=123"

# View statistics
python3 sensitive-masker.py stats

# Cleanup expired
python3 sensitive-masker.py cleanup

# Clear all mappings
python3 sensitive-masker.py clear
```

## 性能

| 操作 | 延迟时间 |
|-----------|---------|
| 热查询（缓存） | < 0.1ms |
| 冷查询（SQLite） | ~0.5ms |
| 写入操作 | < 2ms |
| 最大记录数 | 100,000+ |

**缓存命中率**：通常超过 90%

## 安全特性

- ✅ 文件权限设置：600（仅允许所有者读写）
- ✅ SQLite 事务安全机制
- ✅ 自动过期清理功能
- ✅ LRU 缓存淘汰策略
- **仅使用本地存储**
- **可选的静态数据加密**

## 架构

### 组件

1. **PresidioDetector** - 与 Microsoft Presidio 的集成模块
2. **SensitiveMappingStore** - 负责数据存储和掩码处理的 SQLite + LRU 缓存
3. **ChannelSensitiveMasker** - 主要的掩码处理逻辑模块
4. **OpenClaw Hook** - 用于与 OpenClaw 系统的集成

### 数据库模式

```sql
CREATE TABLE mappings (
    mask_id TEXT PRIMARY KEY,
    original TEXT NOT NULL,
    data_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    usage_count INTEGER DEFAULT 0
);

CREATE INDEX idx_expires_at ON mappings(expires_at);
CREATE INDEX idx_data_type ON mappings(data_type);
```

## 相关文件

```
sensitive-data-masker/
├── SKILL.md                    # This file (English)
├── SKILL.md                    # Chinese version
├── sensitive-masker.py         # Core script
├── handler.js                  # OpenClaw Hook
├── masker-wrapper.py           # Python wrapper
├── DESIGN.md                   # Design document
├── README.md                   # User guide
├── RESEARCH-EXISTING-SOLUTIONS.md  # Market research
└── _meta.json                  # Metadata
```

## 版本历史

### v1.0.0 (2026-03-03)
- 首次发布
- 集成 Microsoft Presidio
- 使用 SQLite 和 LRU 缓存
- 支持 OpenClaw 插件
- 实现 7 天的过期时间限制
- 自动清理过期数据

## 代码仓库

**源代码**: https://gitee.com/subline/onepeace/tree/develop/src/skills/sensitive-data-masker

**许可证**: MIT

**作者**: TK

**问题反馈**: https://gitee.com/subline/onepeace/issues

## 致谢

- **Microsoft Presidio**: https://github.com/microsoft/presidio
- **spaCy**: https://spacy.io/
- **OpenClaw**: https://github.com/openclaw/openclaw

## 相关技能

- `ssh-batch-manager` - 批量 SSH 密钥管理工具
- `healthcheck` - 安全性加固与审计工具
- `skill-creator` - 用于创建新技能的工具