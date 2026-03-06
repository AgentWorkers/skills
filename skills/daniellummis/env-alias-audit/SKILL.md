---
name: env-alias-audit
description: 在部署之前，审核 `.env` 文件中的别名组，检查是否存在缺失的必要配置项、冲突的值以及规范密钥（canonical-key）的不一致情况。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# 环境变量别名审计

使用此技能可以在运行时出现故障之前发现环境变量别名的不一致性问题。

## 该技能的功能：
- 从 `.env` 格式的文件中解析环境变量
- 评估规范的关键字及其对应的别名组合（包括内置的默认值或自定义的别名规则）
- 标记缺少所需别名组合的情况
- 检测同一别名组合中存在冲突的值
- 在没有规范关键字的情况下，报告仅使用别名的情况

## 输入参数：
可选参数：
- `ENV_FILE` （默认值：`.env`）
- `ALIAS_spec_FILE` （默认值：内置的别名规则文件）
- `REQUIRED_groups` （用逗号分隔的必须解析的关键字）
- `AUDIT_MODE` （`report` 或 `strict`，默认值：`strict`）

## 使用方法：
- 使用内置的别名规则：
  ```bash
ENV_FILE=.env \
REQUIRED_GROUPS=DATABASE_URL,STRIPE_API_KEY \
bash skills/env-alias-audit/scripts/audit-env-aliases.sh
```

- 使用自定义的别名规则：
  ```bash
ENV_FILE=.env.production \
ALIAS_SPEC_FILE=skills/env-alias-audit/fixtures/alias-spec.sample \
AUDIT_MODE=report \
bash skills/env-alias-audit/scripts/audit-env-aliases.sh
```

- 对测试用例进行审计：
  ```bash
ENV_FILE=skills/env-alias-audit/fixtures/.env.conflict \
REQUIRED_GROUPS=DATABASE_URL,STRIPE_API_KEY \
bash skills/env-alias-audit/scripts/audit-env-aliases.sh
```

## 别名规则文件的格式：
`ALIAS_spec_FILE` 每行包含一个别名组合：

```text
CANONICAL_KEY=ALIAS_ONE,ALIAS_TWO
```

- 注释和空行会被忽略
- 规范关键字始终是检查的一部分

## 输出结果：
- 如果没有发现严格意义上的错误，程序将以 `0` 退出
- 如果输入无效、缺少所需别名组合或存在冲突的别名值，程序将以 `1` 退出
- 程序会输出每个别名组合的状态（`OK`、`WARN`、`FAIL`）以及总结信息