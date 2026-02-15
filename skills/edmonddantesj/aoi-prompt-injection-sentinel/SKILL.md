# AOI提示注入检测器（AOI Prompt Injection Detector）

S-DNA: `AOI-2026-0215-SDNA-PG01`

## 功能简介
这是一个轻量级、**公开安全**的提示注入检测工具，用于分析输入文本，并输出以下结果：
- **严重程度**（0–4）
- **处理方式**（允许/记录/警告/阻止）
- **违规原因**及匹配的规则ID

## 该工具不支持的功能
- 无Webhook功能
- 无外部调用
- 无自动发布功能
- 不处理任何敏感信息（如密码等）

## 使用方法
### 分析文本（作为参数输入）
```bash
node skill.js analyze --text="..."
```

### 分析标准输入（stdin）
```bash
echo "..." | node skill.js analyze --stdin=true
```

## 输出方式
输出结果以JSON格式显示到标准输出（stdout）。

## 发布管理（公开透明）
我们免费发布这些检测工具，并持续对其进行优化。每次发布都必须通过我们的安全审核流程，并附有可审计的变更日志。我们不会发布任何会降低安全性的更新或导致许可信息模糊的版本。如果检测到多次违规行为，将会逐步采取限制措施（从警告开始，最终可能导致工具暂停发布或被归档）。

## 技术支持
- 问题/漏洞/请求：https://github.com/edmonddantesj/aoi-skills/issues
- 请在提交问题时注明工具的名称：`aoi-prompt-injection-sentinel`

## 相关链接
- ClawHub：https://clawhub.com/skills/aoi-prompt-injection-sentinel

## 许可证
该工具基于MIT许可证开发（原始代码来自AOI项目）。