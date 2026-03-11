---
name: openclaw-safe-change-flow
description: 安全的 OpenClaw 配置变更工作流程：包括备份、最小限度的编辑操作、验证、健康检查以及回滚功能。首先在主实例上进行配置变更；次级实例为可选配置。
---
# OpenClaw 安全变更流程

**目标：**避免系统故障，确保具备回滚能力，并验证每一项变更。

默认情况下使用**单实例**模式；次级实例的检查是可选的。

---

## 范围

### 默认模式（推荐）：单实例
- 主配置文件：`~/.openclaw/openclaw.json`

### 可选模式（高级）：双实例
- 次级配置文件：`~/.openclaw-secondary/openclaw.json`（或您指定的路径）

如果您不需要高可用性验证，单实例模式就足够了。

---

## 必须遵循的单实例变更流程

1. **先进行备份**
   - 创建带时间戳的备份文件：`*.bak.safe-YYYYmmdd-HHMMSS`

2. **进行最小范围的修改**
   - 仅修改必要的配置项

3. **立即进行验证**
   - 运行命令：`openclaw status --deep`

4. **失败时自动回滚**
   - 恢复备份并重启服务

5. **确认服务是否正常运行**
   - 检查各个通道/接口是否能够正常响应

---

## 代理执行规范（默认行为）

安装此功能后，所有配置变更都将遵循以下默认规则：
- **默认的入口脚本**：通过 `safe-change.sh` 来执行配置变更
- **禁止直接修改配置后重启服务**
- **如果用户明确要求绕过此规则**：允许操作，但需提醒相关风险

**思维模式转变：**
- 以前：直接修改配置文件
- 现在：创建一个简单的修改脚本，然后通过 `safe-change.sh --main-script ./edit-main.sh` 来执行修改

---

## 可选的双实例增强功能

在单实例模式的基础上，您还可以验证次级实例的状态：
- 命令：`OPENCLAW_HOME=<secondary-home> openclaw gateway health --url <secondary-url> --token "$SECONDARY_TOKEN"`
- 如果任一实例的验证失败，立即回滚配置

仅在变更风险较高或需要高可用性验证的情况下使用此功能。

---

## 自动化脚本（v1.0.2及以上版本）

此功能包含 `safe-change.sh` 脚本，用于确保以下操作按顺序执行：
**备份 → 修改 → 验证 → 失败时回滚**

### 推荐使用：单实例模式

```bash
cat > ./edit-main.sh <<'SH'
#!/usr/bin/env bash
python3 edit_main.py
SH
chmod +x ./edit-main.sh

./safe-change.sh --main-script ./edit-main.sh
```

### 可选：双实例模式

```bash
cat > ./edit-main.sh <<'SH'
#!/usr/bin/env bash
python3 edit_main.py
SH
chmod +x ./edit-main.sh

cat > ./edit-secondary.sh <<'SH'
#!/usr/bin/env bash
python3 edit_secondary.py
SH
chmod +x ./edit-secondary.sh

export SECONDARY_TOKEN="<your-secondary-token>"
./safe-change.sh \
  --main-script ./edit-main.sh \
  --secondary-script ./edit-secondary.sh
```

启用次级实例验证时，请将 `SECONDARY_TOKEN` 设置为环境变量。

---

## 安全规则
- 绝不要将令牌或敏感信息硬编码到脚本中
- 在宣布变更成功之前必须完成验证
- 先恢复服务，再后续调查问题
- 在生产环境中始终保留最新的、已知正常的备份文件

---

## 手动快速操作模板（单实例模式）

```bash
TS=$(date +%Y%m%d-%H%M%S)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.safe-$TS

# ...apply minimal config edits...

openclaw status --deep
```

如果验证失败：
```bash
cp ~/.openclaw/openclaw.json.bak.safe-$TS ~/.openclaw/openclaw.json
openclaw gateway restart
```