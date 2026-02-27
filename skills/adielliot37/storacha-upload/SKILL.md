---
name: storacha-upload
description: 将文件上传到 IPFS，存储在 Storacha 上，上传到去中心化存储平台；查看 Storacha 的状态，查看存储使用情况；创建新的存储空间，切换存储空间，列出所有存储空间；通过 CID 查找文件；打开 IPFS 内容；获取 IPFS 的网关链接；使用 Web3 存储服务；将文件固定（pin）到 IPFS 上；使用基于内容寻址的存储方式；将文件存储在区块链上；获取自己的 CID（内容标识符）；将文件备份到 IPFS；分享 IPFS 链接；上传目录或单个文件；从 Storacha 中删除文件；实现 Storacha 的委托管理功能；支持 IPFS 文件共享；提供永久性的存储服务；实现 Filecoin 文件备份功能；管理 Storacha 账户；上传图片、照片或文件到 Storacha；将文件保存到 IPFS 上；查看自己拥有的存储空间大小及剩余存储量；检查存储使用情况；判断是否即将耗尽存储空间；创建新的存储空间；设置 Storacha 服务；登录 Storacha 账户；连接并验证用户身份；查看自己上传的所有文件；列出所有文件；删除已上传的文件；获取文件的 IPFS 链接；分享文件；获取文件的下载链接；上传图片或文档；将图片保存到 IPFS 上；查看 Storacha 的整体状态。
  Upload files to IPFS, store on Storacha, upload to decentralized storage,
  check Storacha status, view storage usage, create Storacha space, switch space,
  list spaces, retrieve files by CID, open IPFS content, get gateway link,
  decentralized storage, web3 storage, pin to IPFS, content-addressed storage,
  store on chain, get my CID, backup to IPFS, share IPFS link, upload directory,
  remove upload, Storacha delegation, IPFS file sharing, permanent storage,
  Filecoin backup, manage Storacha account, upload this image, upload this photo,
  upload this file to storacha, save this to IPFS, put this on IPFS,
  how much space do I have, how much storage left, check my storage,
  what's my storage usage, am I running out of space, storage remaining,
  create a new space, make a space, set up storacha, setup storacha,
  login to storacha, sign in to storacha, connect storacha, authenticate storacha,
  show my uploads, what have I uploaded, list my files, my IPFS files,
  delete this upload, remove this file from storacha, get me the link,
  give me the IPFS link, share this file, get download link, open this CID,
  upload pic, upload document, store image, save photo to IPFS,
  how much space is there, check storacha, storacha status
version: 1.3.1
homepage: https://github.com/adielliot37/storacha-skill
metadata:
  clawdbot:
    emoji: "🔥"
    requires:
      bins:
        - storacha
        - node
      env: []
    primaryEnv: ""
    files:
      - "scripts/*"
---
# Storacha 上传

通过 Storacha 分布式存储系统，在 IPFS 上上传、管理和检索文件。

> **代理执行注意事项：** 当提供参数时，所有 `storacha` CLI 命令都是非交互式的。您必须直接执行这些命令——切勿告诉用户“手动运行此命令”或说“我无法运行它”。用户唯一需要参与的交互是：(1) 提供他们的电子邮件地址以进行登录，以及 (2) 点击验证邮件链接。其他所有操作都由系统自动完成。

> **公共数据警告：** 所有上传到 Storacha/IPFS 的文件都是公开可访问的。任何拥有该文件 CID 的人都可以检索这些文件。切勿上传未加密的敏感数据。

> **永久数据警告：** 删除文件仅会从您的列表中移除该文件。其他 IPFS 节点可能会无限期地保留该文件的副本。请将每次上传视为永久性操作。

---

## 理解用户意图

用户会发送自然语言的消息。根据他们的意图执行相应的操作：

| 用户输入 | 操作 |
|---|---|
| “上传这张图片/文件”，“将这个保存到 IPFS”，“把这个存储在 Storacha 上”，“存储这张图片” | **上传** —— 保存附件或引用的文件，然后使用 `storacha up` 命令上传 |
| “我还有多少空间？”，“剩余存储空间？”，“我的空间用完了吗？”，“查看我的使用情况” | **查看使用情况** —— 运行 `storacha usage report` 并显示易于理解的统计信息 |
| “创建一个空间”，“新建一个存储空间” | **创建空间** —— 请求一个名称（或建议一个名称），然后运行 `storacha space create "Name" --no-recovery` |
| “登录 Storacha”，“设置 Storacha”，“连接我的 Storacha”，“身份验证” | **登录** —— 开始身份验证流程（步骤 2a） |
| “显示我的上传文件”，“我上传了什么”，“列出我的文件”，“我的 IPFS 文件” | **列出文件** —— 运行 `storacha ls` 并展示结果 |
| “删除这个”，“移除这个上传文件”，“移除 CID” | **删除** —— 运行 `storacha rm CID` 并提供相应的警告 |
| “给我链接”，“分享这个文件”，“这个文件的 IPFS 链接”，“下载链接” | **检索** —— 构建并分享两种类型的网关 URL |
| “切换空间”，“使用我的另一个空间”，“更改空间” | **切换空间** —— 运行 `storacha space ls`，然后运行 `storacha space use` |
| “检查 Storacha”，“Storacha 的状态”，“Storacha 是否正常工作” | **健康检查** —— 运行完整的诊断流程（步骤 1-5） |

**处理用户消息的规则：**

1. **始终先检查身份验证。** 在执行任何操作之前，默默地运行 `storacha whoami`。如果未通过身份验证，启动登录流程并告知用户情况。
2. **处理文件附件。** 如果用户发送文件/图片/文档，并附上类似 “上传这个” 的消息，首先将附件保存到临时位置，然后使用 `storacha up` 命令上传。上传完成后，分享网关 URL。
3. **主动提供结果。** 上传完成后，务必分享网关链接。查看使用情况后，将字节转换为易于理解的格式。列出上传文件后，以整齐的格式展示结果。
4. **不要直接显示原始的 CLI 输出。** 解析命令输出，并用友好、对话式的语言回应用户。用户不希望看到原始的终端文本。
5. **自动从错误中恢复。** 如果由于没有可用空间而导致命令失败，默默地解决问题（创建或选择一个空间），然后重试。只有在确实需要用户输入时（例如登录时需要电子邮件地址）才询问用户。

---

## 先决条件

在继续之前，请先运行以下命令：

```bash
which storacha && storacha --version
```

如果未找到 `storacha`，请安装它：

```bash
npm install -g @storacha/cli
```

需要 **Node.js v18+**。使用 `node -v` 进行验证。如果缺少或版本过低，请引导用户访问 [nodejs.org](https://nodejs.org)。

---

## 首次设置与身份验证

在进行任何上传操作之前，请按照以下步骤操作。

### 第一步 —— 检查 CLI 是否已安装

```bash
which storacha && storacha --version
```

**预期输出：**
```
/usr/local/bin/storacha
x.y.z
```

如果未安装，请安装：
```bash
npm install -g @storacha/cli
```

然后重新运行检查。如果安装失败，请确认 Node.js 版本是否为 v18+。

### 第二步 —— 检查身份验证

```bash
storacha whoami
```

**如果输出包含 `did:key:`** → 表示已成功身份验证。继续执行第三步。

**如果出现错误或没有 DID** → 表示未登录。返回步骤 2a。

### 第二步a —— 登录流程

这是与用户的对话过程。用户可能通过 Telegram、WhatsApp、Discord 或其他平台进行交流。引导他们完成每个步骤，并在继续之前等待他们的回复。

**步骤 A —— 请求电子邮件地址：**

如果用户尚未提供电子邮件地址，请询问：
> “要使用 Storacha，我需要您登录。您的电子邮件地址是什么？如果您还没有 Storacha 账户，可以在 https://console.storacha.network 免费注册，然后提供您的电子邮件地址。”

如果用户已经提供了电子邮件地址（例如 “登录到 Storacha，我的电子邮件是 user@example.com”），则跳过此步骤，直接进入步骤 B。

**在获取到用户的电子邮件地址之前，请勿继续。**

**步骤 B —— 运行登录：**

**重要提示：** 当您将电子邮件地址作为参数传递给 `storacha login` 命令时，该命令是非交互式的。您必须直接运行它。切勿告诉用户手动运行该命令，也不要说您无法运行它。您需要亲自运行该命令。**

```bash
storacha login user@example.com
```

将 `user@example.com` 替换为用户实际提供的电子邮件地址。此命令：
- 将电子邮件地址作为命令行参数接收（无需提示或交互式输入）
- 自动发送验证邮件
- 等待用户点击邮件中的链接
- 成功后返回 `Agent was authorized by did:mailto:...`

命令执行完成后，立即通知用户：
> “我已经开始登录流程。验证链接已发送到 user@example.com。请检查您的收件箱（和垃圾邮件文件夹）并点击链接。我正在等待您的确认。”

**在等待期间，请勿运行其他命令。** CLI 会自动检测用户是否点击了链接。

**步骤 C —— 处理新账户：**

如果这是用户的第一次登录，他们可能需要在点击验证链接后选择一个存储计划。告知他们：
> “由于这是您的第一次登录，系统可能会要求您在打开的页面上选择一个存储计划。以下是您的选项：”

| 计划 | 价格 | 存储空间 | 出口地址 | 超量费用 |
|---|---|---|---|---|
| 基本（免费） | $0/月 | 5 GB | 5 GB | $0.15/GB |
| 中级 | $10/月 | 100 GB | 100 GB | $0.05/GB |
| 高级 | $100/月 | 2 TB | 2 TB | $0.03/GB |

> “免费的 Basic 计划提供 5 GB 存储空间，足够您开始使用。”

**步骤 D —— 确认登录成功：**

当 CLI 成功返回结果后，通过运行以下命令进行验证：

```bash
storacha whoami
```

如果返回 `did:key:` 值，告知用户：
> “您已成功登录 Storacha。”

如果失败，请询问用户是否需要再次点击验证链接，或者检查他们是否使用了正确的电子邮件地址。

### 第三步 —— 检查存储空间

```bash
storacha space ls
```

**预期输出：**
```
* did:key:z6Mk... SpaceName
  did:key:z6Mk... AnotherSpace
```

带有 `*` 标记的空间表示当前激活的空间。

- **如果存在带有 `*` 标记的空间** → 表示当前激活的空间已设置。继续执行步骤 4。
- **如果没有空间** → 自动创建一个空间：
  ```bash
  storacha space create "MyFiles" --no-recovery
  ```
  然后告知用户：
  > “我已经为您创建了一个名为 ‘MyFiles’ 的存储空间。您的上传文件将存储在这里。”

  空间名称是永久性的，无法更改。
- **如果存在空间但都没有激活** → 选择第一个空间并激活它：
  ```bash
  storacha space use "SpaceName"
  ```
  然后告知用户：
  > “我已经将 ‘SpaceName’ 设置为您的激活存储空间。”

所有这些操作都应在后台自动完成，无需用户手动运行命令。用户正在聊天，他们期望您完成这些操作并确认结果。

### 第四步 —— 验证提供商注册

```bash
storacha space info
```

**预期输出包括：**
```
Providers: did:web:web3.storage
```

如果没有列出任何提供商，表示空间尚未注册。引导用户访问 https://console.storacha.network 进行注册或创建新的存储空间。

### 第五步 —— 检查存储空间使用情况

```bash
storacha usage report
```

**预期输出格式：**
```
Account: did:mailto:...
Provider: did:web:web3.storage
Space: did:key:z6Mk...
Size: 123456789
```

解析 `Size` 值并将其转换为易于理解的格式：
- < 1024 → 字节
- < 1,048,576 → KB
- < 1,073,741,824 → MB
- >= 1,073,741,824 → GB

向用户展示存储空间使用情况的仪表板：

```
╔══════════════════════════════════════╗
║       Storacha Status Dashboard      ║
╠══════════════════════════════════════╣
║ Account:  did:mailto:user@email.com  ║
║ Space:    MyFiles (did:key:z6Mk...)  ║
║ Storage:  117.7 MB used              ║
║ Plan:     Mild (Free) — 5 GB limit   ║
╚══════════════════════════════════════╝
```

如果存储空间使用量超过计划限制的 80%，警告用户并建议升级或删除旧的上传文件。

如果使用情况报告返回权限错误，请告知用户，但请注意上传文件仍然可以正常使用。

---

## 核心操作

### 上传文件

当用户请求上传文件（图片、照片、文档等）时：

1. **如果用户附上了文件** —— 将文件保存到临时位置（例如 `/tmp/upload/filename.ext`）
2. **如果用户提供了文件路径** —— 直接使用该路径
3. **默默地检查身份验证和当前激活的空间** —— 运行 `storacha whoami` 和 `storacha space ls`。在用户不知情的情况下解决任何问题。
4. **上传文件：**

```bash
storacha up /path/to/file
```

5. **解析输出结果并以对话式语言回应用户：**

> “上传完成！您的文件已上传到 IPFS。以下是链接：
> https://storacha.link/ipfs/bafy...
> 任何拥有此链接的人都可以访问该文件。”

始终提供两种类型的网关 URL：
- 路径格式：`https://storacha.link/ipfs/CID`
- 子域名格式：`https://CID.ipfs.storacha.link`

如果上传的是图片/照片，还需说明：
> “您可以直接分享此链接——它在任何浏览器中都可以访问。”

### 上传目录

```bash
storacha up /path/to/directory/
```

- 默认情况下，隐藏文件（dotfiles）不会被包含在内。使用 `--hidden` 选项可以包含它们。
- 使用 `--no-wrap` 选项可以避免在 URL 中包含目录结构（这样文件名不会显示在链接中）。

对于目录上传，文件可以通过以下链接访问：
```
https://storacha.link/ipfs/CID/filename.txt
```

### 列出上传文件

```bash
storacha ls
```

显示当前空间中的所有上传文件及其 CID。

### 删除上传文件

```bash
storacha rm CID
```

同时删除底层的数据片段：
```bash
storacha rm CID --shards
```

**警告用户：** 删除操作仅会从您的列表中移除文件。数据可能仍会保存在其他 IPFS 节点上。

### 检索/打开文件

在浏览器中打开文件：
```bash
storacha open CID
```

程序化下载文件：
```bash
curl -o output.txt "https://storacha.link/ipfs/CID"
```

子域名格式：
```bash
curl -o output.txt "https://CID.ipfs.storacha.link"
```

---

## 空间管理

**创建存储空间：**
```bash
storacha space create "ProjectName" --no-recovery
```
**重要提示：** 必须使用 `--no-recovery` 选项。如果不使用此选项，CLI 会提示用户输入恢复密钥，这在非交互式环境中可能会导致问题。空间名称是永久性的，创建后无法更改。

**列出所有空间：**
```bash
storacha space ls
```
激活的空间会用 `*` 标记。

**切换激活空间：**
```bash
storacha space use "SpaceName"
```
或者通过 DID 来切换：
```bash
storacha space use did:key:z6Mk...
```

**查看空间详细信息：**
```bash
storacha space info
```
显示空间的 DID 和注册的提供商信息。

---

## 共享与授权

为其他代理创建 UCAN 授权：
```bash
storacha delegation create AUDIENCE_DID --can store/add --can upload/add --output ./delegation.ucan
```

完全的管理员权限授权：
```bash
storacha delegation create AUDIENCE_DID --can '*' --output ./admin.ucan --base64
```

列出所有授权信息：
```bash
storacha delegation ls
```

---

## 错误处理

1. **“命令未找到：storacha”** → 安装 CLI：`npm install -g @storacha/cli`
2. **“资源没有可用的证明”** → 使用 `storacha login 用户电子邮件地址` 重新登录，或使用 `storacha space use “空间名称”` 切换空间
3. **“未在提供商处注册”** → 运行 `storacha space info` 检查提供商信息。在 https://console.storacha.network 注册或创建新的存储空间。
4. **上传失败或超时** → 检查网络连接。重新尝试上传。对于大文件，请确保网络连接稳定。
5. **“使用/报告权限错误”** —— 这只是提示信息。上传操作仍可继续进行。
6. **“没有空间”或空间列表为空** → 创建空间：`storacha space create “MyFiles” --no-recovery`
7. **存储空间限制错误** → 在 https://console.storacha.network 升级存储计划，或删除旧的上传文件：`storacha rm CID --shards`

---

## 快速参考

| 操作 | 命令 |
|---|---|
| 安装 CLI | `npm install -g @storacha/cli` |
| 登录 | `storacha login 用户电子邮件地址` |
| 检查身份 | `storacha whoami` |
| 创建空间 | `storacha space create “空间名称” --no-recovery` （始终使用 `--no-recovery`） |
| 列出空间 | `storacha space ls` |
| 切换空间 | `storacha space use “空间名称” |
| 查看空间详细信息 | `storacha space info` |
| 上传文件 | `storacha up /文件路径` |
| 上传目录 | `storacha up /目录路径` |
| 无目录结构上传 | `storacha up /路径 --no-wrap` |
| 包含隐藏文件上传 | `storacha up /路径 --hidden` |
| 列出上传文件 | `storacha ls` |
| 删除上传文件 | `storacha rm CID` |
| 删除文件及其片段 | `storacha rm CID --shards` |
| 在浏览器中打开文件 | `storacha open CID` |
| 查看使用情况 | `storacha usage report` |
| 创建授权 | `storacha delegation create DID --can-store/add --output 文件.ucan` |
| 列出授权信息 | `storacha delegation ls` |

---

## 重要说明

- 身份验证基于电子邮件地址和 DID 进行。没有 API 密钥或令牌。
- 空间是通过 `did:key` 标识的存储命名空间。每个空间独立记录其上传的文件。
- 内容寻址意味着每个文件都会根据其内容获得唯一的 CID。相同的文件会生成相同的 CID。
- Filecoin 备份提供了 Filecoin 网络上的存储证明。
- 提供两种类型的网关 URL：
  - 路径格式：`https://storacha.link/ipfs/CID`
  - 子域名格式：`https://CID.ipfs.storacha.link`
- 当前的 CLI 可执行文件名为 `storacha`。在 web3.storage 时代，它的名称曾是 `w3`。