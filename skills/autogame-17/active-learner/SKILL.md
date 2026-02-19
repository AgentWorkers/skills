# Active Learner

**版本：** 1.0.0  
**作者：** OpenClaw Evolution（循环编号：#2597）

## 说明  
实现了主动学习协议（Active Learning Protocol, R3）。该功能允许代理程序将学习内容自动存储到 `MEMORY.md` 文件中，并生成结构化的“请求帮助”（ask for help）请求。

## 使用方法

### 自动学习（Internalize a Lesson）  
```bash
node skills/active-learner/index.js internalize --id "L1" --category "Protocol" --text "Lesson content here..."
```

### 请求帮助（Ask for Help）  
```bash
node skills/active-learner/index.js ask --text "I don't understand X..."
```