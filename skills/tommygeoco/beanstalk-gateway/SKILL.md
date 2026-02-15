# Beanstalk Gateway

将您的本地 Clawdbot 连接到 [beans.talk](https://beans.talk)，以便进行远程监控和控制。

## 安装

```bash
npm install -g beanstalk-gateway
```

## 设置

1. 访问 [beans.talk](https://beans.talk)，然后点击“Connect Gateway”。
2. 复制设置命令。
3. 在您的机器上运行该命令。
4. 安装完成！

## 手动使用

```bash
# Configure
beanstalk-gateway configure --url wss://... --token gt_...

# Start
beanstalk-gateway start

# Check local Clawdbot status  
beanstalk-gateway status
```

## 更多信息

- [npm 包](https://www.npmjs.com/package/beanstalk-gateway)
- [GitHub](https://github.com/tommygeoco/beanstalk-gateway)