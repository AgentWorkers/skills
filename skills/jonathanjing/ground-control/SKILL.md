---
name: ground-control
description: OpenClaw的升级后验证系统：该系统定义了一个模型/定时任务/通道的基准文件（ground truth file），并包含了一个五阶段的自动化验证流程（配置完整性检查、API密钥的有效性验证、定时任务的正确性验证、会话功能的测试以及通道的活跃性检查）。此外，系统还具备自动修复配置和定时任务偏差的功能。
version: "0.2.2"
metadata:
  author: JonathanJing
  tags: [ops, verification, upgrade, config, cron, health]
  license: MIT
  credentials:
    mode: user-declared
    source: MODEL_GROUND_TRUTH.md → non_llm_providers[].env_var
    note: >
      This skill reads env vars that the USER declares in their MODEL_GROUND_TRUTH.md file.
      The set of env vars is not known at publish time — it depends on which providers
      the user configures. Common examples: BRAVE_API_KEY, NOTION_TOKEN.
      Credentials are only sent to HTTPS endpoints whose hostname exactly matches
      the user-declared allowed_domain. See SKILL.md Permissions section for full policy.
---
# 地面控制（Ground Control）

**OpenClaw升级后的验证功能**：确保系统在每次升级后仍能正常运行。

## 权限与要求

执行此功能需要具备以下OpenClaw权限：
- **`gateway config.get`**：读取当前配置（所有阶段）
- **`gateway config.patch`**：自动修复配置偏差（仅限第1阶段）
- **`cron list` / `cron update`**：验证并自动修复定时任务（第3阶段）
- **`sessions_spawn`**：生成用于测试的会话（第2、4、5阶段）
- **`message send`**：发送消息以检测通道是否正常运行，并生成汇总报告（第5阶段）

**自动修复机制**：在第1和第3阶段，系统会自动修复配置和定时任务，使其与`GROUND_TRUTH`中的设定保持一致。可以使用`--dry-run`选项禁用自动修复功能，仅执行报告生成操作。

**环境变量**：第2阶段的测试会涉及非LLM（Large Language Model）提供者的相关配置（例如Brave、Notion等）。安全策略如下：
- 仅会读取`MODEL_GROUND_TRUTH.md`中明确列出的环境变量（即`non_llm_providers[]`数组中的变量）。
- 凭据仅会发送到主机名与`allowed_domain`字段完全匹配的HTTPS端点。
- 在每次执行curl请求之前，系统会验证端点地址的合法性；如果地址不匹配，则跳过该请求并生成错误报告。
- 该功能不会枚举、导出或记录环境变量的值。
- 如果`GROUND_TRUTH`文件中不存在`non_llm_providers`部分，则会完全跳过与非LLM提供者相关的检查。

## 使用场景**

- 在执行`openclaw update`或`npm install -g openclaw@latest`后
- 当怀疑配置发生异常（如模型变更、定时任务故障或通道无法正常使用）时
- 通过`/verify`命令定期进行系统健康检查

## 设置步骤**

1. 将`templates/MODEL_GROUND_TRUTH.md`文件复制到工作区的根目录。
2. 根据实际情况填写配置信息（包括模型、定时任务和通道设置）。
3. 将`GROUND_TRUTH`的同步规则添加到`AGENTS.md`文件中（详见README文件）。
4. 运行`/verify`命令进行测试。

## 相关文件**

- `templates/MODEL_GROUND_TRUTH.md`：地面真实值模板（复制到工作区根目录）
- `scripts/post-upgrade-verify.md`：用于执行五阶段验证的代理脚本
- `scripts/UPGRADE_SOP.md`：升级标准操作流程