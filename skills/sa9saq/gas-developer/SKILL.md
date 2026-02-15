---
name: gas-developer
description: Google Apps Script专家：专注于电子表格自动化以及Gmail和日历的集成工作。
---

# GAS 开发者

开发用于电子表格自动化、Gmail、日历和 Drive 集成的 Google Apps Script 解决方案。

## 指令

1. **理解需求**：需要使用哪种 Google 服务？需要实现什么自动化功能？触发条件是什么？
2. **选择合适的方法**：

   | 使用场景 | 服务 | 触发条件 |
   |----------|---------|---------|
   | 数据处理 | 电子表格 | onEdit / 定时触发 |
   | 邮件自动化 | Gmail | 定时触发 |
   | 日历同步 | 日历 | 定时触发 / 更改事件触发 |
   | 文件管理 | Drive | 定时触发 |
   | 表单处理 | 表单 | onFormSubmit 触发 |
   | Web 仪表板 | HTML Service | doGet 请求 |

3. **遵循以下最佳实践编写清晰的 GAS 代码**。
4. **彻底测试** — 使用 `Logger.log()` 进行调试。
5. **记录设置信息** — 包括触发条件、权限配置等。

## 模板

### 电子表格 — 读/写数据
```javascript
function processSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Data');
  const data = sheet.getDataRange().getValues();
  
  // Skip header row
  for (let i = 1; i < data.length; i++) {
    const [name, email, status] = data[i];
    if (status === '') {
      // Process row
      sheet.getRange(i + 1, 3).setValue('Processed');
    }
  }
}
```

### 使用模板发送邮件到 Gmail
```javascript
function sendTemplateEmail(to, subject, templateName) {
  const template = HtmlService.createTemplateFromFile(templateName);
  const htmlBody = template.evaluate().getContent();
  
  GmailApp.sendEmail(to, subject, '', {
    htmlBody: htmlBody,
    name: 'Your Name'
  });
}
```

### 外部 API 调用
```javascript
function callExternalApi(endpoint, apiKey) {
  const options = {
    method: 'get',
    headers: { 'Authorization': 'Bearer ' + apiKey },
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(endpoint, options);
  const code = response.getResponseCode();
  
  if (code !== 200) {
    Logger.log('API error: ' + code + ' ' + response.getContentText());
    return null;
  }
  
  return JSON.parse(response.getContentText());
}
```

### 定时触发器设置
```javascript
function createDailyTrigger() {
  // Delete existing triggers for this function
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(t => {
    if (t.getHandlerFunction() === 'dailyTask') {
      ScriptApp.deleteTrigger(t);
    }
  });
  
  // Create new daily trigger at 9 AM
  ScriptApp.newTrigger('dailyTask')
    .timeBased()
    .atHour(9)
    .everyDays(1)
    .create();
}
```

### 错误处理模式
```javascript
function safeExecute(fn, context) {
  try {
    return fn();
  } catch (error) {
    Logger.log('Error in ' + context + ': ' + error.message);
    // Optional: send error notification
    GmailApp.sendEmail('admin@example.com', 
      'GAS Error: ' + context, error.stack);
    return null;
  }
}
```

## 最佳实践

- **批量操作**：使用 `getValues()` / `setValues()` 而不是逐个单元格操作
- **注意使用限制**：GAS 有每日使用量限制（邮件：每天 100 封免费，URL 请求：每天 20,000 次）
- **缓存**：对于耗时的 API 调用，使用 `CacheService` 进行缓存
- **配置存储**：将配置信息存储在 `PropertiesService` 中（避免硬编码）
- **锁定**：使用 `LockService` 防止多个触发器同时执行

## 安全性

- **切勿硬编码 API 密钥** — 使用 `PropertiesService.getScriptProperties()` 获取
- **验证用户输入** — 尤其是在 Web 应用中（doGet/doPost 请求时）
- **限制共享**：将脚本设置为“以我的身份执行”，仅允许特定用户访问
- **审查权限**：GAS 请求需要较宽的 OAuth 权限范围；向用户说明原因

## 交付检查清单
```
□ Code tested with sample data
□ Triggers documented and set up
□ Error handling in place
□ Setup instructions included
□ API keys stored in Properties (not code)
□ Permissions explained to client
```

## 准备条件

- 拥有具有 Apps Script 访问权限的 Google 账户
- 无需任何本地依赖项 — 所有功能都在 Google Cloud 中运行