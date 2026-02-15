# EmailAgent README

## 概述

`EmailAgent` 类利用 OpenAI 的 GPT 模型和 LangChain 提供了基于人工智能的电子邮件撰写和发送功能。该类包含一个“人工介入”（human-in-the-loop）中间件，在发送电子邮件之前需要经过审批。

## 配置

### 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `OPENAI_MODEL` | `gpt-4o-mini` | 要使用的 OpenAI 模型 |

## 使用方法

```typescript
import { EmailAgent } from './email.agent';
import { SendEmailDto } from '../dto/send-email.dto';

const agent = new EmailAgent();

const dto: SendEmailDto = {
  email: 'recipient@example.com',
  name: 'John Doe',
  subject: 'Meeting Request',      // optional
  body: 'Initial email content',   // optional
  instructions: 'Keep it formal'   // optional
};

const result = await agent.sendEmail(dto);
```

## 人工介入中间件

该代理在发送电子邮件之前会使用 `humanInTheLoopMiddleware` 中间件来中断 `EmailTool` 的执行流程。这允许用户执行以下操作：

- **approve**：批准已撰写的电子邮件并发送。
- **edit**：在发送前修改电子邮件内容。
- **reject**：取消电子邮件发送操作。

`readEmailTool` 被排除在中间件干预之外（其值为 `false`），因此读取电子邮件的操作可以无需审批即可继续进行。

## 参数

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `email` | 字符串 | 是 | 收件人电子邮件地址 |
| `name` | 字符串 | 是 | 收件人姓名 |
| `subject` | 字符串 | 否 | 电子邮件主题行 |
| `body` | 字符串 | 否 | 电子邮件正文内容 |
| `instructions` | 字符串 | 否 | 用于指导人工智能撰写电子邮件的指令 |

## 返回值

该函数返回代理处理后的最终邮件内容（以字符串形式）。