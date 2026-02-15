---
name: telnyx-seti-javascript
description: >-
  Access SETI (Space Exploration Telecommunications Infrastructure) APIs. This
  skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: seti
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Seti - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取黑盒测试结果

返回各种黑盒测试的结果

`GET /seti/black_box_test_results`

```javascript
const response = await client.seti.retrieveBlackBoxTestResults();

console.log(response.data);
```
```