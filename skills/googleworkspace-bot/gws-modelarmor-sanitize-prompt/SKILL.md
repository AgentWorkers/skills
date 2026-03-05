---
name: gws-modelarmor-sanitize-prompt
version: 1.0.0
description: "**Google Model Armor：** 通过 Model Armor 模板对用户输入进行清洗（即去除潜在的恶意内容或无关信息）。"
metadata:
  openclaw:
    category: "security"
    requires:
      bins: ["gws"]
    cliHelp: "gws modelarmor +sanitize-prompt --help"
---
# modelarmor + sanitize-prompt

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解认证、全局标志和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

通过 Model Armor 模板对用户输入进行清理（即去除潜在的安全风险）

## 使用方法

```bash
gws modelarmor +sanitize-prompt --template <NAME>
```

## 标志参数

| 标志 | 是否必需 | 默认值 | 说明 |
|------|---------|---------|-------------|
| `--template` | ✓ | — | 完整的模板资源路径（格式：projects/PROJECT/locations/LOCATION/templates/TEMPLATE） |
| `--text` | — | — | 需要清理的文本内容 |
| `--json` | — | — | 完整的 JSON 请求体（会覆盖 `--text` 的设置） |

## 示例

```bash
gws modelarmor +sanitize-prompt --template projects/P/locations/L/templates/T --text 'user input'
echo 'prompt' | gws modelarmor +sanitize-prompt --template ...
```

## 提示：

- 如果未指定 `--text` 或 `--json`，程序将从标准输入（stdin）读取内容。
- 为确保输出内容的安全性，建议使用 `+sanitize-response` 工具。

## 参考资料：

- [gws-shared](../gws-shared/SKILL.md) — 全局标志和认证相关设置
- [gws-modelarmor](../gws-modelarmor/SKILL.md) — 用于清理用户生成内容的安全性工具