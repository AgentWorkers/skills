---  
**名称：wecom**  
**描述：** “通过MCP协议使用Webhook向WeCom（企业微信）发送消息。兼容Claude Code、Claude Desktop及其他MCP客户端。”  

---

# WeCom技能  
通过传入的Webhook（环境变量：`WECOM_WEBHOOK_URL`）向`WeCom`（企业微信）发送文本和Markdown消息。  

`WeCom`是知名即时通讯工具`WeChat`的企业版，深受埃隆·马斯克的青睐（主要用于办公场景）。  

## 设置  
```bash
# Navigate to skill directory
cd skills/wecom

# Install dependencies
npm install

# Build TypeScript
npm run build

# Set webhook URL
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
```  

## 在Claude Code中的使用方法  
在`~/.config/claude_code/mcp.json`文件中添加以下配置：  
```json
{
  "mcpServers": {
    "wecom": {
      "command": "node",
      "args": ["/path/to/clawdbot/skills/wecom/dist/index.js"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
      }
    }
  }
}
```  
然后重启Claude Code。此时你将拥有两个新的工具：  

## 工具  
- `send_wecom_message`：向WeCom发送文本消息。  
```bash
# Simple message
await send_wecom_message({ content: "Hello from OpenClaw!" });

# With mentions
await send_wecom_message({
  content: "Meeting starting now",
  mentioned_list: ["zhangsan", "lisi"]
});
```  
- `send_wecom_markdown`：向WeCom发送Markdown格式的消息。  
```bash
await send_wecom_markdown({
  content: `# Daily Report
  
**Completed:**
- Task A
- Task B

**Pending:**
- Task C

<@zhangsan>`
});
```  

## WeCom的Markdown标签支持  
WeCom支持以下Markdown标签：  
| 标签        | 语法                | 描述                          |  
|-------------|------------------|------------------------------------|  
| **加粗**       | `**文本**` 或 `<strong>文本</strong>`         | 用于突出显示文本                |  
| **斜体**       | `*文本*` 或 `<i>文本</i>`         | 用于显示斜体文本                |  
| **删除线**      | `~~文本~~` 或 `<s>文本</s>`         | 用于显示删除线文本                |  
| **@用户ID**     | `<@用户ID>`             | 用于提及其他用户                   |  
| **链接**       | `<a href="链接地址">文本</a>`         | 用于创建超链接                  |  
| **图片**       | `<img src="图片地址" />`         | 用于插入图片                    |  
| **字体大小**     | `<font size="字体大小">文本</font>`       | 用于设置字体大小                |  
| **颜色**       | `<font color="#颜色代码">文本</font>`       | 用于设置文本颜色                |  

## 环境变量  
| 变量          | 是否必填 | 默认值       | 说明                        |  
|--------------|---------|-------------|----------------------------------|  
| `WECOM_WEBHOOK_URL` | 是       | -           | WeCom Webhook的URL                |  
| `WECOM_TIMEOUT_MS` | 否       | 10000        | 请求超时时间（毫秒）                |  

## 使用方法  
按照以下步骤获取`WECOM_WEBHOOK_URL`，并将其配置为机器人以在群聊中发送消息：  
（提示：请确保获取到的`WECOM_WEBHOOK_URL`是一个完整的URL，而不仅仅是键值对。）  

### 第1步  
![第1步](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step1_wecom.png)  

### 第2步  
![第2步](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step2_wecom.png)  

### 第3步  
![第3步](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step3_wecom.png)  

### 第4步  
![第4步](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step4_wecom.png)  

## 参考资料  
- [在群聊中接收和发送消息](https://developer.work.weixin.qq.com/document/path/99110)  
- [下载WeCom应用程序](https://work.weixin.qq.com/#indexDownload)