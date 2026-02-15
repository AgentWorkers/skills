# vnsh 技能

使用 `vnsh` CLI 通过加密的、有时效性的链接安全地共享文件。

此技能允许您：
1. 上传本地文件以获取一个安全的 `vnsh.dev` 链接。
2. 读取 `vnsh.dev` 链接以解密并访问其内容。

## 使用方法

`vnsh` 工具有两种主要模式：上传和读取。

### 1. 上传文件

要共享文件，请使用 `vnsh` 命令后跟文件路径。该工具会加密文件，上传文件，并返回一个安全的链接。

**命令：**
```bash
vnsh [options] <file_path>
```

**示例：**
```bash
vnsh /path/to/my/document.pdf
```

**输出：**
```
https://vnsh.dev/s/xxxxxxxxxxxxxxxx
```

#### 选项

- `-t, --ttl <小时>`：设置链接的有效期（生存时间）以小时为单位。默认值为 24 小时，最大值为 168 小时（7 天）。

**带 TTL 的示例：**
```bash
# Link will expire in 1 hour
vnsh -t 1 /path/to/my/secret.txt
```

### 2. 读取（解密）链接

要访问 `vnsh` 链接的内容，请使用 `read` 命令。

**命令：**
```bash
vnsh read <url>
```

**示例：**
```bash
vnsh read https://vnsh.dev/s/xxxxxxxxxxxxxxxx
```

该工具会下载文件，解密文件内容，并将其打印到标准输出。对于二进制文件，您可能需要将输出重定向到文件中。

**二进制文件的示例：**
```bash
vnsh read https://vnsh.dev/s/yyyyyyyyyyyyyyyy > received_image.png
```