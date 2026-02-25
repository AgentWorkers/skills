# Doginals Skill v1.0.2

## 功能概述
Doginals Skill 允许用户与 Doginals 和 Dunes 协议进行交互，支持铭文创建、代币管理以及与 Dogecoin Core 的无缝集成。

## 主要特性
- **Doginals.js**：用于处理 Dogecoin 原生 NFT 和铭文的核心库。
- **Dunes.js**：支持 DRC-20 可互换代币的创建和管理。
- **批量工具**：包含 `auto_inscriber_v4.py`（用于自动化铭文创建）和 `bulk-mint.sh`（用于批量操作）。
- **自动设置**：自动安装所有依赖项，配置 Dogecoin Core，并确保配置流程顺畅。
- **文档**：提供详细的入门指南（`DoginalsREADME.md` 和 `DUNES.md`），便于用户快速上手。

---

## 安装
使用提供的 `install.sh` 脚本自动配置所有依赖项。

```bash
bash install.sh
```

---

## 使用方法
### 铭文管理：
```bash
node doginals.js wallet sync
node . mint <address> <path>
node . mint <address> <content type> <hex data>
node . mint <address> "" "" <delegate inscription ID>
```
示例：
```bash
node . mint D9UcJkdirVLY11UtF77WnC8peg6xRYsogu "text/plain;charset=utf-8" 576f6f6621
node . mint D9UcJkdirVLY11UtF77WnC8peg6xRYsogu C:\doginals-main\ApeStractArtCollecton\DPAYSTONE.html
```

### DRC-20 代币管理：
```bash
node dunes.js wallet sync
node . drc-20 deploy <address> <ticker> <total> <max mint>
node . drc-20 mint <address> <ticker> <amount>
```
示例：
```bash
node . drc-20 deploy D9pqzxiiUke5eodEzMmxZAxpFcbvwuM4Hg 'DFAT' 100000000 100000000
node . drc-20 mint D9pqzxiiUke5eodEzMmxZAxpFcbvwuM4Hg DCAC 100000000
```

### 批量创建（使用 `auto_inscriber_v4.py` 自动化操作）：
在开始批量创建之前，请确保您的钱包已同步并拥有足够的资金。将所有需要铭文的文件放入 `~/.doginals-main/inscribeBulk/` 目录中。`auto_inscriber_v4.py` 脚本会从这个目录中读取文件进行铭文操作。

#### 步骤：
1. 将文件放入 `~/.doginals-main/inscribeBulk/` 目录。
2. 通过以下参数配置 `auto_inscriber_v4.py` 脚本：
    - `directory`：包含要铭文文件的目录路径（默认为 `~/.doginals-main/inscribeBulk/`）。
    - `file_prefix`：文件名前缀（例如，`ApeImage` 表示文件名格式为 `ApeImage00001.jpg`）。
    - `file_extension`：文件扩展名（例如，`jpg`、`png`）。
    - `start` 和 `end`：要铭文的文件编号范围。

#### 运行脚本：
```bash
python3 auto_inscriber_v4.py
```
脚本将：
- 批量创建铭文。
- 在铭文过程中如果出现“too-long-mempool-chain”错误，会自动同步钱包。
- 记录所有错误，并更新 `.json` 文件中的 `txid` 对应关系。

---

## 查看交易记录
启动 HTTP 服务器：
```bash
node . server
```
然后使用浏览器访问：
```bash
http://localhost:3000/tx/<transaction_id>
```
将 `<transaction_id>` 替换为日志中的相应 TXID。

---

## 注意事项
- 在执行任何操作之前，请确保 Dogecoin Core 已同步。
- 请使用您自己的钱包凭据替换示例中的敏感文件。

---

## 警告
- 仅使用专门用于铭文操作的钱包，以避免意外烧毁代币。
- 在运行创建或铭文命令之前，请仔细检查所有配置。