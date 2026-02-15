---
name: quick-reminders
description: "零参数大语言模型（Zero-LLM）的一次性提醒功能（有效期<48小时），通过 `nohup sleep` 命令结合 `openclaw` 发送消息来实现，具体操作流程由脚本 `{baseDir}/scripts/nohup-reminder.sh` 完成。"
metadata: {"openclaw":{"emoji":"⏰","requires":{"bins":["jq","openclaw"]}}}
user-invocable: true
---

# 快速提醒

适用于**未来2天以内的**一次性提醒。系统会在创建提醒时生成最终的提醒内容。当提醒触发时，后台进程会通过`openclaw message send`发送该内容——过程中不会消耗任何LLM（大型语言模型）的token。

## 注意事项：**如果提醒时间超过2天**，请使用日历功能

如果用户请求在未来**2天或更长时间后**收到提醒，请**不要使用此功能**。  
相反，应为用户创建一个日历事件（前提是用户有日历功能或可用的相关技能），并设置适当的提醒通知。  
简要说明：“我会将提醒添加到您的日历中，这样就不会被忽略。”

---

所有操作均通过命令行界面（CLI）执行：  
`bash {baseDir}/scripts/nohup-reminder.sh <command> [args]`  

> 如果`{baseDir}`未被解析，可以使用工作区相对路径：  
`bash ./skills/quick-reminders/scripts/nohup-reminder.sh <command> [args]`  

**`--target`参数**：提醒的接收目标，来自`TOOLS.md`文件中的“Reminders”章节。该参数对于执行“添加”操作是必需的。  
接收目标的格式取决于具体渠道（例如：Telegram聊天ID、WhatsApp的E.164号码、Discord频道ID）。  
如果`TOOLS.md`中未提供该信息，请使用`session_status`工具获取`deliveryContext.to`（去掉前缀如`telegram:`），将其保存到`TOOLS.md`中后再使用。  
**默认渠道**为Telegram；可通过`--channel <name>`（例如`whatsapp`、`discord`、`signal`、`imessage`）进行更改。  

---

## 命令说明  

### 添加提醒  
```
nohup-reminder.sh add "Reminder text here" --target <chat_id> -t TIME [--channel CH] [-z TIMEZONE]
```  
- **提醒内容**：用户实际会收到的信息。请自行编写内容，可适当加入引导语或有用提示。  
- `-t`：时间选项（相对时间：`30s`、`20m`、`2h`、`1d`、`1h30m`；绝对时间：ISO-8601格式，例如`2026-02-07T16:00:00+03:00`）  
- `-z`：时间使用的时区（默认为系统本地时区）  

### 列出所有提醒  
```
nohup-reminder.sh list
```  
系统会自动删除已触发的提醒记录。  

### 删除提醒  
```
nohup-reminder.sh remove ID [ID ...]
nohup-reminder.sh remove --all
```  

---

## 提醒信息的编写规则  

提醒内容应像朋友发消息一样自然，避免使用机械化的表述。  
**绝对禁止使用以下语句：**  
- “提醒：给John打电话”  
- “这是给您的……提醒”  
- “您要求收到关于……的提醒”  
- “任务：清洗餐具”  

**建议使用以下表达方式：**  
- “嘿，您之前想给John打电话呢”  
- “该给John回电话了”  
- “该清洗餐具了”  
- “我知道您不喜欢这个任务，但洗碗机不会自动启动”  
- “包裹已准备好——请去取一下”  

**编写提示时的注意事项：**  
- 使用亲切的开头语（如“嘿”、“那么……”或直接说“注意”）  
- 适当加入幽默或同理心（例如“我知道，我知道……”）  
- 保持内容简短（一行即可，无需正式格式）  
- 即使用户数小时后阅读，内容也应易于理解  

---

## 示例（可直接复制粘贴，将`<chat_id>`替换为实际ID）  

用户：**“2小时后提醒我给John打电话”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh add "Hey, you wanted to call John" --target <chat_id> -t 2h
```  

用户：**“20分钟后提醒我去取衣服”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh add "Laundry's ready — go grab it" --target <chat_id> -t 20m
```  

用户：**“今天下午6点设置一个提醒——去取包裹”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh add "Package is waiting for you" --target <target> -t "2026-02-07T18:00:00" -z "America/New_York"
```  

用户：**“30分钟后通过WhatsApp提醒我检查烤箱”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh add "Check the oven!" --target +15551234567 -t 30m --channel whatsapp
```  

用户：**“我有哪些提醒？”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh list
```  

用户：**“取消提醒#3”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh remove 3
```  

用户：**“取消提醒1和4”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh remove 1 4
```  

用户：**“清除所有提醒”**  
```bash
bash {baseDir}/scripts/nohup-reminder.sh remove --all
```  

---

## 使用规则：  
1. **提醒内容必须在创建时自行编写**。触发提醒时不会运行任何LLM。  
2. 提醒内容在用户阅读时必须能够独立理解（无需上下文信息）。  
3. 回复时请使用简短的话语/短语（如“好的”、“会提醒您”、“明白了”），使用将来时态。  
   **禁止使用**“已完成”、“已添加”、“已创建”或类似表述。  
4. 如需修改提醒内容，请先删除旧提醒，再添加新内容。