---
name: phishing-reporter
description: 当用户分享一个可疑的或具有钓鱼性质的URL，并希望对其进行举报，或者请求报告一个危险网站时，请向Google Safe Browsing、瑞士网络安全中心（NCSC）以及其他滥用行为举报服务报告这些URL。触发这些操作的关键词包括：“report phishing”（举报钓鱼行为）、“melde diese Seite”（举报该网站）、“report this URL”（举报此URL）、“phishing melden”（举报钓鱼网站）、“scam melden”（举报诈骗网站）以及“report abuse”（举报滥用行为）。
---
# 钓鱼报告工具

通过浏览器自动化功能，将危险URL报告给相关滥用检测/安全服务。

## 报告策略

按以下顺序向所有适用的服务进行报告：

1. **Google Safe Browsing**（自动化）——全球覆盖，可在Chrome/Firefox/Safari中阻止恶意网站
2. **瑞士国家网络安全中心（NCSC Switzerland）**（半自动化）——瑞士国家网络安全机构
3. **域名注册商**（手动）——通过WHOIS查询获取滥用处理联系人信息

## 服务1：Google Safe Browsing（完全自动化）

**URL**：`https://safebrowsing.google.com/safebrowsing/report_phish/?hl=en`

### 工作流程

使用浏览器工具（配置文件：`openclaw`）自动化执行以下步骤：

1. 打开上述URL
2. 选择报告类型：“此页面不安全”（默认选项，无需更改）
3. 从下拉菜单中选择“威胁类型”为“社会工程学”（用于钓鱼攻击）
4. 从下拉菜单中选择最合适的威胁类别
5. 在URL输入框中输入钓鱼网站的URL
6. 在附加详情输入框中填写描述
7. 点击“提交”
8. 确认“提交成功”的提示信息

### 注意事项：
- 表单使用自定义的下拉菜单：点击组合框后选择列表中的选项
- reCAPTCHA v3会在后台运行，通常对无头浏览器也能正常通过
- 如果reCAPTCHA导致提交失败，请提供手动操作指南

## 服务2：瑞士国家网络安全中心（NCSC Switzerland）（聊天助手）

**URL**：`https://www.report.ncsc.admin.ch/en/`

NCSC提供多步骤的聊天助手来处理报告。通过浏览器自动化执行以下步骤：

### 钓鱼网站报告的聊天路径：

1. 打开`https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1`
2. 选择：“网站/网络服务/网络平台”
3. 选择：“我想举报一个第三方网站”
4. 选择：“该网站显示欺诈性内容”
5. 选择：“该网站模仿了其他已知网站”（针对钓鱼克隆网站）
6. 完成剩余步骤（输入URL、填写描述、提供联系方式）
7. 提交报告

### 直接访问路径（跳过前几步）
```
https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1%3E128%3E132%3E133%3E314%3E130%3E135
```

### 注意事项：
- 聊天助手具有状态保存功能——每完成一步会显示下一步的操作内容
- 无reCAPTCHA验证，但需要多次点击
- 可通过`notification@ncsc.ch`发送电子邮件（请附上URL和描述）
- 如果自动化失败，请提供直接访问路径和操作指南

## 服务3：域名注册商（手动查询）

1. 使用`whois <domain>`或`https://who.is/<domain>`进行WHOIS查询
2. 查找“注册商的滥用处理联系人邮箱”
3. 发送包含钓鱼网站URL和描述的滥用举报邮件

## 附加详情模板
```
Phishing site impersonating [BRAND]. Domain mimics [REAL SERVICE] customer service.
Designed to steal [banking credentials / login data / personal information].
```

## 手动操作指南

如果自动化提交失败，请向用户提供以下信息：
1. 各个报告表格的直接链接
2. 需要报告的URL
3. 推荐的报告类别/类型
4. 预先写好的描述文本

## 其他报告服务

请参阅`references/services.md`以获取完整的服务列表，包括Cloudflare、PhishTank和APWG等。