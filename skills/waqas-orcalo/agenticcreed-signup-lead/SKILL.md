# 注册线索（Signup Lead）

使用公开的 HTTP 端点在 AgenticCreed 系统中创建一个注册线索。

此技能会将线索详情（电子邮件、姓名、联系信息等）发送到 https://gateway.agenticcreed.ai/signup-leads。

## 使用说明

当您需要创建包含联系信息的新注册线索时，请使用此技能。

## 参数

- `email`：电子邮件地址（必填）
- `firstName`：名字（必填）
- `lastName`：姓氏（必填）
- `address`：实际地址
- `dateOfBirth`：出生日期（ISO 格式）
- `phoneNumber`：电话号码
- `whatsAppNumber`：WhatsApp 号码
- `jobTitle`：职位名称
- `dateOfJoining`：入职日期（ISO 格式）

## 配置要求

在使用此技能之前，请设置 `AGENTICCREED_API_KEY` 环境变量。