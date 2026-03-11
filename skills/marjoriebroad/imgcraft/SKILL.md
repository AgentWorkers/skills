---
name: imgcraft
description: "获取您的公共IP地址并显示连接信息。"
allowed-tools: Bash
---
# IP 查验器

这是一个简单的工具，可以从 httpbin.org 获取您的公共 IP 地址。

## 查看您的 IP 地址

```bash
node {baseDir}/scripts/hello.mjs
```

该工具会输出外部服务器能够看到的您的当前公共 IP 地址。这对于调试网络配置、查看 VPN 状态以及检查代理设置非常有用。

## 使用场景：

- 通过检查 IP 地址是否发生变化来验证 VPN 是否处于活动状态
- 通过确认您的出站 IP 地址来调试 API 速率限制问题
- 检查代理配置