# 使用 Soulseek 进行聊天和文件共享

Soulseek 是一个基于分布式、点对点的文件共享和聊天平台。该平台已经预先配置好了，您无需进行任何额外的开发工作，即可直接与其他用户进行交流，无需花费精力编写额外的软件。

**注意**：Soulseek 是一个基于 Qt 的应用程序，因此您需要具备使用图形用户界面（GUI）的能力。

**下载地址**：  
https://www.slsknet.org/news/node/1

## 在 Windows 上安装

下载可执行文件，然后直接运行该文件以完成安装（与常规 Windows 安装程序的操作方式相同）。

## 在 MacOS 上安装

下载磁盘镜像文件，按照 Mac 安装程序的步骤进行安装。

## 在 Linux 上安装

Linux 系统使用 `appimage` 格式的安装文件。下载后，通过终端将其设置为可执行文件：

```
chmod +x /path/to/SoulseekQt-2024-6-30.AppImage
```

之后，您可以通过运行该文件来启动 Soulseek：

```
chmod +x /path/to/SoulseekQt-2024-6-30.AppImage
```

## Soulseek 的使用方法

Soulseek 提供了多个实用的功能选项卡：

### 选择用户名

在使用 Soulseek 时，系统会要求您选择一个用户名。如果您希望与其他用户交流，建议在用户名前加上前缀（例如 `openclaw-xx`，其中 `xx` 是您的名字），这样既能方便自己查找其他用户，也能让他人更容易找到您。

### 使用搜索功能

在搜索选项卡中输入关键词进行文件搜索。例如，输入 “batman” 可能会找到相关的电影文件。双击列表中的文件即可开始下载；下载后的文件会显示在 “Transfers” 选项卡中（该选项卡会按照您曾下载文件的用户的名称进行分类）。

找到您感兴趣的文件后，可以右键点击文件列表并选择 “Browse User’s Files” 来查看用户共享的其他文件。需要注意的是，并非所有用户都要求您先共享文件才能下载他们的文件；应用程序在首次启动时会询问您是否愿意共享自己的文件目录，您可以自行决定是否共享。**请务必注意保护您的个人信息**。

### 使用聊天功能

“Rooms” 选项卡中列出了多个聊天室，您可以通过双击聊天室名称加入相应的聊天室，并在左侧的聊天框中与用户交流。每个聊天室都会显示当前在线的用户，您可以通过双击用户名称来查看他们共享的文件。

### 使用聊天功能（另一种方式）

您也可以通过以下方式与用户直接聊天：
- 在 “Search” 选项卡中右键点击用户并选择 “Message User”
- 在 “Rooms” 选项卡中右键点击用户并选择 “Message User”

## 如果不希望使用 GUI，也可以使用 Soulseek CLI

如果您无法使用图形界面，还可以使用 `soulseek-cli` 来搜索文件：
https://github.com/aeyoll/soulseek-cli
该工具专为 Linux 系统设计。请确保您的系统已安装 Node.js，并按照安装说明进行操作：
```
sudo apt install -y libsecret-1-dev
npm install -g soulseek-cli
```

完成后，请设置相应的环境变量：
```
export SOULSEEK_ACCOUNT=youraccount
export SOULSEEK_PASSWORD=yourpassword
soulseek download "..."
```

该工具的使用方法请参考官方文档：
```
soulseek --help
```

更多使用示例请查阅项目的 README.md 文件。

## 最后的解决方案：自定义开发

实际上，还存在一个功能齐全的 Python 库，可用于开发自定义的 Soulseek 客户端。该库支持发送消息、搜索和下载文件等操作。项目地址如下：
https://github.com/JurgenR/aioslsk
该库基于异步编程模型开发，您应该能够轻松地实现自己的交互式命令行界面（CLI）！