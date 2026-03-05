---
name: browser-setup
description: "在没有 root/sudo 权限的环境中（如云容器、VPS、沙箱主机），安装并配置无头 Chrome 浏览器以供 OpenClaw 浏览器工具使用。适用场景包括：  
1. 当浏览器工具提示“未找到支持的浏览器”时；  
2. 当 Chrome 抛出“页面崩溃”或“缺少库文件”的错误时；  
3. 在新服务器或容器上设置浏览器自动化功能时；  
4. 当用户请求为 OpenClaw 安装或修复浏览器时。  
**注意：** 本方法不适用于已安装 Chrome 的 macOS/Windows 桌面系统，也不适用于 Chrome 扩展程序的配置。"
---
# 浏览器设置（无root权限的Linux系统）

在没有root权限的Linux系统中，需要安装无界面的Google Chrome浏览器，以便OpenClaw的`browser`工具能够使用。

## 使用场景

- 当执行`browser start`时出现“未找到支持的浏览器”错误。
- Chrome虽然启动了，但页面会崩溃（显示“页面崩溃”或“目标页面已关闭”）。
- 在云容器、VPS或沙箱环境中运行时，且没有使用`sudo`权限。

## 快速启动

```bash
bash scripts/install-browser.sh
```

该脚本会下载Chrome浏览器，解压约40个共享库文件，安装Liberation字体，创建一个封装脚本，并验证安装是否成功。整个过程大约需要2分钟。

接下来配置OpenClaw：

```bash
openclaw config set browser.executablePath "$HOME/local-libs/chrome-wrapper.sh"
openclaw config set browser.headless true
openclaw config set browser.noSandbox true
openclaw config set browser.attachOnly true
```

设置openclaw配置文件中的CDP端口（编辑`~/data/openclaw.json`或相应的配置文件）：

```json
{
  "browser": {
    "executablePath": "~/local-libs/chrome-wrapper.sh",
    "headless": true,
    "noSandbox": true,
    "attachOnly": true,
    "profiles": {
      "openclaw": { "cdpPort": 18800, "color": "#FF4500" }
    }
  }
}
```

## 重要提示：`attachOnly`必须设置为`true`

OpenClaw内部有两个用于浏览器操作的路径：

- **CDP路径**（用于启动/停止/切换标签页）：直接与Chrome的CDP端口通信。
- **Playwright路径**（用于导航/截图/执行操作）：使用OpenClaw自带的`playwright-core`库。

当`attachOnly`设置为`false`时，Playwright会调用`launchOpenClawChrome()`方法，该方法会检查`ensurePortAvailable(cdpPort)`。由于Chrome已经在该端口上监听，因此每次执行`navigate/snapshot/act`操作时都会抛出`PortInUseError`错误。

当`attachOnly`设置为`true`时，Playwright会通过`connectOverCDP()`方法连接到正在运行的Chrome实例，从而避免端口冲突。

**在使用封装脚本或手动启动Chrome时，务必将`attachOnly`设置为`true`。**

## 使用流程

### 启动Chrome

在OpenClaw使用Chrome之前，必须先启动Chrome。可以手动启动Chrome：

```bash
~/local-libs/chrome-wrapper.sh \
  --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \
  --remote-debugging-port=18800 \
  --user-data-dir=~/data/browser/openclaw/user-data \
  --no-first-run --disable-setuid-sandbox \
  about:blank &
```

或者让OpenClaw来启动Chrome（但这种情况下Playwright操作会抛出`PortInUseError`错误，因此不推荐这样做）。

### 浏览器工具流程

```
browser start (profile=openclaw)   → detects running Chrome via CDP
browser navigate (targetUrl)       → Playwright connectOverCDP → loads page
browser snapshot                   → accessibility tree (structured page data)
browser screenshot                 → PNG capture
browser act (ref=e12, kind=click)  → interact via ref from snapshot
```

## 常见问题及解决方法

### 共享库缺失

**症状：**在加载共享库时出现错误：“libXXX.so: 无法打开共享对象文件”。

**解决方法：**安装脚本会处理这个问题。如果Chrome更新后出现新的缺失库文件，请检查以下步骤：

```bash
LD_LIBRARY_PATH=~/local-libs/lib ldd ~/chrome-install/opt/google/chrome/chrome | grep "not found"
```

然后执行`apt-get download <package>`，使用`dpkg-deb -x`解压文件，并将生成的`.so`文件复制到`~/local-libs/lib/`目录下。

### 页面崩溃

**症状：**执行`page.goto`时页面崩溃，或者目标页面、上下文或浏览器本身被关闭。

**原因：**缺少字体。当系统中没有可用的字体时，Chrome的渲染引擎会崩溃。

**解决方法：**安装相应的字体文件（安装脚本会自动完成这一操作）。请确保`~/.fonts/`目录下存在`.ttf`格式的字体文件，并且`~/.config/fontconfig/fonts.conf`配置文件存在。封装脚本需要正确设置`FONTCONFIG_FILE`环境变量。

### PortInUseError

**症状：**出现`PortInUseError：端口18800已被占用`。

**原因：**`attachOnly`设置为`false`，导致Playwright尝试在同一端口上启动新的Chrome实例。

**解决方法：**在OpenClaw的配置文件中将`browser.attachOnly`设置为`true`。

### CDP连接超时/积压

**症状：**`browser start`操作成功，但后续调用出现超时。

**原因：**Chrome的TCP监听队列中积累了过多的连接请求（处于CLOSE-WAIT状态），导致新的连接请求被阻塞。

**解决方法：**终止Chrome进程（使用`pkill -9 -f chrome`），等待几秒钟后重新启动Chrome。

### 容器中的`/dev/shm`空间不足

**症状：**在容器中加载复杂页面时，Chrome的渲染引擎会崩溃。

**原因：**默认的容器`/dev/shm`空间仅为64MB，不足以满足Chrome的运行需求。

**解决方法：**在安装脚本中添加`--disable-dev-shm-usage`选项；对于Docker容器，还需添加`--shm-size=256m`参数来增加`/dev/shm`的空间。

## 安装脚本的功能

1. 从Google下载稳定的Chrome `.deb`包。
2. 使用`dpkg-deb -x`将Chrome二进制文件解压到`~/chrome-install/`目录（无需root权限）。
3. 通过`ldd`命令检测缺失的共享库。
4. 使用`apt-get download`下载约40个共享库的`.deb`包（无需root权限）。
5. 将所有`.so`文件解压到`~/local-libs/lib/`目录。
6. 下载`fonts-liberation`并安装`.ttf`字体文件到`~/.fonts/`目录。
7. 创建`~/local-libs/chrome-wrapper.sh`脚本，设置`LD_LIBRARY_PATH`和`FONTCONFIG_FILE`环境变量。
8. 验证Chrome是否能够成功启动，并显示其版本信息。

## 包列表参考

下载的库文件（基于Ubuntu/Debian系统，不同发行版可能略有差异）：

```
libglib2.0, libnss3, libnspr4, libatk1.0, libatk-bridge2.0, libcups2, libdrm2,
libxkbcommon0, libxcomposite1, libxdamage1, libxfixes3, libxrandr2, libgbm1,
libasound2, libatspi2.0, libdbus-1-3, libxcb1, libx11-6, libxext6, libcairo2,
libpango-1.0, libpangocairo-1.0, libffi8, libpcre2-8-0, libxau6, libxdmcp6,
libxi6, libxrender1, libpng16-16, libfontconfig1, libfreetype6, libxcb-render0,
libxcb-shm0, libpixman-1-0, libfribidi0, libthai0, libharfbuzz0b,
libavahi-common3, libavahi-client3, libdatrie1, libgraphite2-3
```