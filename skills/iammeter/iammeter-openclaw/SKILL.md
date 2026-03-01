---
name: iammeter
description: "通过 iammeter API 查询和导出设备/站点数据（基于 https://www.iammeter.comswaggeruiswagger.json）：支持的功能包括：列出所有站点/设备信息、获取实时或历史能耗数据、导出数据为 CSV 格式文件，以及执行电力分析或离线数据分析操作。"
metadata: {"openclaw": {"primaryEnv": "IAMMETER_TOKEN", "requires": {"env": ["IAMMETER_TOKEN"]}}}
---
# iammeter 技能（Node.js）

这是一个基于官方 Swagger 规范的 iammeter API 的 Node.js 客户端和命令行工具（CLI）。

**功能：**
- 令牌会自动加载：首先从 `IAMMETER_TOKEN` 环境变量中加载，如果没有找到，则从 `~/.openclaw/openclaw.json` 文件中的 `skills.entries.iammeter.apiKey` 中加载。
- 列出用户站点（sitelist）
- 获取所有电表的最新数据（metersdata）
- 获取单个电表的最新上传数据（meterdata/meterdata2）
- 查询站点能耗历史记录（energyhistory）并导出为 CSV 文件
- 进行电力分析（poweranalysis）或离线分析（offlineanalysis）

**配置：**
- **选项 A（OpenClaw/Clawhub）：** 在 Skills UI 中设置令牌。该令牌会存储在 `~/.openclaw/openclaw.json` 文件的 `skills.entries.iammeter.apiKey` 中，并在运行时作为 `IAMMETER_TOKEN` 环境变量注入。
- **选项 B（本地测试）：** 在运行程序前，需要设置 `IAMMETER_TOKEN=<your_token>`。

**文件结构：**
- `references/api.md` —— 从 Swagger 文档中总结的 API 端点参考信息
- `scripts/iammeter_client.js` —— 包含常用 API 调用的 Node.js 客户端代码
- `scripts/cli.js` —— 包含命令行工具（用于执行 sitelist、meters、meter、history、poweranalysis、offlineanalysis 等操作）
- `package.json` —— 项目依赖项（axios、yargs）

**使用方法（本地测试）：**
1. 安装依赖项：
   ```
   cd ~/.openclaw/workspace/skills/iammeter
   npm install
   ```
2. 运行命令：
   ```
   node scripts/cli.js sitelist
   node scripts/cli.js meters
   node scripts/cli.js meter <device_sn>
   node scripts/cli.js history <placeId> 2026-02-01 2026-02-25 --out out.csv
   ```

**注意事项：**
- 部分 API 端点有严格的请求速率限制（详情请参阅 `references/api.md`）。
- 请勿将真实的令牌提交到公共仓库中。

**致谢：**
- API 端点和字段数据来源于：https://www.iammeter.comswaggeruiswagger.json

**关于 IAMMETER：**
IAMMETER 是一家能源监控解决方案提供商，提供基于 Wi-Fi 的单相和三相智能电表，支持多种开放通信协议，包括 Modbus/TCP、MQTT、HTTP/HTTPS API、TCP 和本地推送（Local Push）协议。这些开放接口使得 IAMMETER 设备能够轻松集成到 OpenHAB 及其他开源平台中。

**了解更多关于支持的协议和 API：**
- 设备通信协议：https://www.iammeter.com/newsshow/blog-fw-features
- IAMMETER 云 API：https://www.iammeter.com/docs/system-api
- 更多信息请参见：[高级用户生态系统图](https://iammeterglobal.oss-accelerate.aliyuncs.com/img/advanced-user-ecosystem.png)

---

（翻译说明：）
1. 保持技术术语的准确性，如 OpenClaw、ClawHub、API、CLI 等。
2. 代码示例、命令和 URL 保持原样。
3. 仅翻译代码块中的注释，这些注释具有解释性。
4. 结构和组织与原文保持一致。
5. 所有占位符（如 `___CODE_BLOCK_0___`）均按原样保留。