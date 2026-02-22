# Passo - 远程浏览器访问

为用户提供对服务器上浏览器的远程访问权限。非常适合用于登录、二次身份验证（2FA）、验证码验证或任何需要手动操作的浏览器任务。

## 安装

在需要使用浏览器的服务器上运行以下脚本：

```bash
curl -fsSL https://raw.githubusercontent.com/felipegoulu/passo-client/main/install.sh | bash
```

该脚本将执行以下操作：
1. 如果用户尚未注册账户，会提示其在 getpasso.app 上注册。
2. 安装所需的依赖程序（如 Chromium、VNC 等）。
3. 创建名为 `passo` 的命令。

## 浏览器地址

{{ACCESS_URL}}

由以下用户进行保护：{{EMAIL}}

## 可用命令

```bash
passo start   # Start the browser tunnel
passo stop    # Stop everything  
passo status  # Check if running
```

## 使用方法

1. 当需要用户协助时，发送上述浏览器地址。
2. 用户在手机或笔记本电脑上打开该地址。
3. 用户使用 Google 账户登录（只有该用户的邮箱才能访问该浏览器）。
4. 用户完成所需的操作（登录、二次身份验证、验证码验证等）。
5. 用户告知您操作已完成。
6. 您可以继续后续流程。

## 价格

30 天免费试用期后，费用为每月 5 美元。费用通过 getpasso.app 的管理面板进行收取。

## 链接

- 网站：https://getpasso.app
- 文档：https://getpasso.app/docs