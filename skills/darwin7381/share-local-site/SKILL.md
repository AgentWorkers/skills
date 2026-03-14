---
name: share-local-site
description: 通过公共URL与任何人共享本地开发服务器。当您需要向客户演示网站、让同事预览您的作品、在移动设备上进行测试，或者通过互联网共享本地主机（localhost）时，可以使用此功能。支持使用ngrok（推荐）、localhost.run（无需安装）和cloudflared作为代理服务。能够自动处理常见的错误，例如Vue CLI中出现的“Invalid Host Header”问题。
---
# 共享本地站点

将本地开发服务器暴露到互联网上，以便任何人都可以通过公共URL访问它。无需进行任何部署。

## 使用场景

- 向客户或同事展示正在开发的网站
- 在移动设备上测试本地站点
- 用于协作编程或代码审查
- 在不进行部署的情况下快速提供外部访问

## 方法比较

| 方法 | 注册 | 安装 | 稳定性 | 适用场景 |
|--------|--------|---------|-----------|----------|
| **localhost.run** | 无需注册 | 无需安装 | ⭐⭐ | **最快启动方式**。无需设置，非常适合初次使用 |
| **ngrok** | 需要注册 | 需要安装 | ⭐⭐⭐⭐ | 最稳定。提供控制面板，支持多隧道，会话持续时间更长 |
| **cloudflared** | 无需注册 | 需要安装 | ⭐⭐⭐ | 已经预安装好，可快速创建隧道 |

## 快速入门

### localhost.run（无需安装，启动最快）

无需安装任何软件，也无需注册。只需运行以下命令：

```bash
ssh -o StrictHostKeyChecking=no -R 80:localhost:3000 nokey@localhost.run
```

在输出中找到生成的URL（例如：`https://xxxxx.lhr.life`），然后立即分享该URL。

### ngrok（最稳定，适合长时间使用）

```bash
# First time only
brew install ngrok        # or: npm i -g ngrok, or download from ngrok.com
ngrok config add-authtoken YOUR_TOKEN   # get token from dashboard.ngrok.com

# Start tunnel
ngrok http 3000           # replace 3000 with your port
```

获取公共URL：
```bash
curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url'
```

Web控制面板：http://127.0.0.1:4040

### cloudflared

```bash
brew install cloudflared   # first time only
cloudflared tunnel --url http://localhost:3000
```

## 共享前的检查事项

**在分享任何隧道URL之前，请务必验证：**

1. **确认隧道连接到了正确的端口：**
   ```bash
   curl -s http://localhost:4040/api/tunnels | python3 -c "
   import sys,json; d=json.load(sys.stdin)
   for t in d['tunnels']:
       print(t['config']['addr'], t['public_url'])"
   ```

2. **验证页面是否能正常加载：**
   ```bash
   curl -sI <TUNNEL_URL>                        # check HTTP 200
   curl -s <TUNNEL_URL> | grep -i '<title>'     # confirm correct site
   ```
   注意可能出现的问题：`Invalid Host header`、显示错误的项目信息、空白页面或502错误。

3. **只有在两项检查都通过后，才能分享URL。**

## 多个隧道（使用ngrok）

ngrok的免费版本支持同时创建最多3个隧道。每个隧道可以在单独的终端或tmux会话中运行：

```bash
# Terminal 1: frontend on port 5173
ngrok http 5173

# Terminal 2: backend on port 3001
ngrok http 3001
```

查看所有活跃的隧道：
```bash
curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys,json; d=json.load(sys.stdin)
for t in d['tunnels']:
    print(f\"{t['name']:20s} {t['config']['addr']:30s} {t['public_url']}\")"
```

## 框架特定的解决方案

### Vue CLI：`Invalid Host header`问题

Vue CLI的webpack-dev-server默认会阻止非本地主机的访问。

**Vue CLI 2/3（webpack-dev-server v3）：**
```js
// vue.config.js
module.exports = {
  devServer: { disableHostCheck: true }
}
```

**Vue CLI 5+（webpack-dev-server v4+）：**
```js
// vue.config.js
module.exports = {
  devServer: { allowedHosts: 'all' }
}
```

**Vite / Next.js / Nuxt：** 无需配置，隧道功能可立即使用。

### 创建React应用

```bash
DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
```

或者可以在`.env`文件中配置：
```
DANGEROUSLY_DISABLE_HOST_CHECK=true
```

## 常见问题解答

**Q：代码更改后需要重新启动隧道吗？**
不需要。隧道只是转发网络流量，热重载功能可以正常使用——只需刷新页面即可。

**Q：URL的有效期是多久？**
只要隧道进程在运行，URL就有效。关闭隧道后，URL也会失效。

**Q：多人可以访问同一个URL吗？**
可以。该URL是公开可访问的。

**Q：ngrok提示“隧道数量过多”？**
免费版本允许创建3个隧道。关闭不使用的隧道或升级到付费版本。

## 推荐搭配使用：`openclaw-tmux-persistent-process`

OpenClaw的`exec`会话具有自动清理机制——当会话空闲一段时间、系统资源不足或网关重启时，相关后台进程（包括隧道）会自动关闭。这可能会导致演示过程中URL突然失效。

为避免这种情况，建议安装`openclaw-tmux-persistent-process`插件。该插件会在一个与OpenClaw独立运行的tmux会话中维持隧道连接：

```bash
clawhub install openclaw-tmux-persistent-process
```

安装完这两个插件后，告诉代理：“通过tmux共享端口3000”，这样隧道就会在独立的tmux会话中持续运行，不会因网关重启而中断。

## 故障排除

| 问题 | 解决方法 |
|---------|-----|
| `Invalid Host header` | 参见上述针对特定框架的解决方案 |
| ngrok令牌无效 | 从dashboard.ngrok.com重新获取令牌 |
| `localhost.run`运行缓慢 | 更改使用ngrok |
| 页面显示空白或出现502错误 | 确保本地开发服务器正在运行 |
| 显示错误的项目信息 | 使用`curl localhost:4040/api/tunnels`检查端口映射是否正确 |
| cloudflared出现404错误 | 免费版本的cloudflared稳定性可能不稳定——建议切换到ngrok |