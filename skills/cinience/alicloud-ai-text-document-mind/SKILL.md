---
name: alicloud-ai-text-document-mind
description: 通过 Node.js SDK 使用 Document Mind (DocMind) 提交文档解析任务并获取解析结果。该工具专为 Claude Code/Codex 的文档理解工作流程而设计。
---

**类别：提供者**  
# Document Mind (DocMind) — Node.js SDK  

使用 DocMind 通过异步任务提取文档的结构、文本和布局信息。  

## 先决条件  

- 安装 SDK：  
  - `npm install @alicloud/docmind-api20220711 @alicloud/tea-util @alicloud/credentials`  
- 通过标准的 Alibaba Cloud 环境变量提供认证信息：  
  - `ALICLOUD_ACCESS_KEY_ID`  
  - `ALICLOUD_ACCESS_KEY_SECRET`  
  - `ALICLOUD_REGION_ID`（可选，默认值；如果未设置，请选择最适合任务的地区或询问用户）  

## 快速入门（提交任务 + 轮询结果）  

```js
const Client = require('@alicloud/docmind-api20220711');
const Credential = require('@alicloud/credentials');
const Util = require('@alicloud/tea-util');

const cred = new Credential.default();
const regionId = process.env.ALICLOUD_REGION_ID || 'cn-hangzhou'; // Example default; choose/ask if unset.
const client = new Client.default({
  endpoint: `docmind-api.${regionId}.aliyuncs.com`,
  accessKeyId: cred.credential.accessKeyId,
  accessKeySecret: cred.credential.accessKeySecret,
  type: 'access_key',
  regionId,
});

async function submitByUrl(fileUrl, fileName) {
  const req = new Client.SubmitDocStructureJobRequest();
  req.fileUrl = fileUrl;
  req.fileName = fileName;
  const resp = await client.submitDocStructureJob(req);
  return resp.body.data.id;
}

async function pollResult(jobId) {
  const req = new Client.GetDocStructureResultRequest();
  req.id = jobId;
  const resp = await client.getDocStructureResult(req);
  return resp.body;
}

(async () => {
  const jobId = await submitByUrl('https://example.com/example.pdf', 'example.pdf');
  console.log('jobId:', jobId);

  // Poll every 10s until completed.
  for (;;) {
    const result = await pollResult(jobId);
    if (result.completed) {
      console.log(result.status, result.data || result.message);
      break;
    }
    await new Promise((r) => setTimeout(r, 10000));
  }
})();
```  

## 脚本快速入门示例  

```bash
DOCMIND_FILE_URL="https://example.com/example.pdf" \\
node skills/ai/text/alicloud-ai-text-document-mind/scripts/quickstart.js
```  

**环境变量：**  
- `DOCMIND_FILE_URL`  
- `DOCMIND_FILE_NAME`（可选）  
- `DOCMIND POLL_INTERVAL_MS`（可选，默认值：10000 毫秒）  
- `DOCMIND_MAX_POLLS`（可选，默认值：120 次）  

## 本地文件上传  

```js
const fs = require('fs');
const advanceReq = new Client.SubmitDocStructureJobAdvanceRequest();
advanceReq.fileUrlObject = fs.createReadStream('./example.pdf');
advanceReq.fileName = 'example.pdf';
const runtime = new Util.RuntimeOptions({});
const resp = await client.submitDocStructureJobAdvance(advanceReq, runtime);
```  

## 关于 Claude Code/Codex 的注意事项：  
- DocMind 是异步执行的：提交任务后需要持续轮询，直到任务状态变为 `completed=true`。  
- 每约 10 秒轮询一次；最大处理时间为 120 分钟。  
- 使用 URL 提交任务时，请确保文件可公开访问。  

## 错误处理：  
- `UrlNotLegal`：URL 无法公开访问或格式不正确。  
- `DocProcessing`：任务仍在进行中；请继续轮询。  
- `Fail`：查看 `message` 和错误代码以确定根本原因。  

## 参考资料：  
- DocMind Node.js SDK：`@alicloud/docmind-api20220711`  
- 源代码列表：`references/sources.md`