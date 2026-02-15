---
name: solax-summary-fetch
description: 使用 npm 包 `solax-cloud-api` 从 Solax Cloud API 获取逆变器的汇总数据。当用户提供了（或已配置了）Solax tokenId 和逆变器序列号（sn）时，可以使用此方法将当前的/汇总的能源数据以 JSON 格式（类型为 SolaxSummary）返回，以便用于仪表板或自动化系统。
---

# solax-summary-fetch

用于以 JSON 格式获取 Solax 逆变器的摘要信息。

## 设置（一次性操作）

本技能依赖于 Node.js 和 npm 包 `solax-cloud-api`。

在技能文件夹内安装所需的依赖项：

```bash
cd /home/openclaw/.openclaw/workspace/skills/solax-summary-fetch/scripts
npm install
```

（我们使用 `npm install` 而不是 `npm ci`，因为本技能不包含锁文件。）

## 输入参数

您需要提供以下信息：
- `tokenId`（Solax Cloud API 的令牌 ID）
- `sn`（逆变器的序列号）

### 建议：将参数设置为环境变量

建议在运行时设置这些环境变量（这样可以避免将敏感信息泄露到 shell 历史记录中）：
- `SOLAX_TOKENID`
- `SOLAX_SN`

**请勿** 将凭据硬编码到技能文件中。

### 替代方案：通过 CLI 参数传递

您也可以通过以下命令行参数传递这些值：
- `--tokenId <tokenId>`
- `--sn <serial>`

## 命令格式

```bash
cd /home/openclaw/.openclaw/workspace/skills/solax-summary-fetch/scripts
node fetch_summary.mjs --tokenId "$SOLAX_TOKENID" --sn "$SOLAX_SN"
```

## 输出结果

- 将一个 JSON 对象输出到标准输出（stdout）。
- 该 JSON 对象符合 `solax-cloud-api` 提供的 **SolaxSummary** 接口规范（详见 `references/solax-summary.d.ts`）。
- 在内部实现中（solax-cloud-api v0.2.0）：首先调用 `getAPIData()`，然后通过 `SolaxCloudAPI.toSummary()` 进行转换。

## 安全注意事项

- 在确认 `tokenId` 已正确设置后，切勿将其打印或记录到日志中（应对其进行屏蔽）。
- 如果 API 调用失败，返回一个包含 `ok`: false` 和简短错误信息的 JSON 对象。