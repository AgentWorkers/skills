# LegiScan 议案跟踪器

这是一个用于通过 LegiScan API 监控州立法活动的工具。它可以根据自定义关键词和州的选择来筛选出正在审议中的议案。

## 设置

1. **API 密钥**：从 [LegiScan](https://legiscan.com/legiscan) 获取免费的 API 密钥。
2. **环境变量**：在您的环境中设置 `LEGISCAN_API_KEY`。
3. **依赖库**：需要 `requests` 库。

## 使用方法

可以直接运行该脚本，或者通过定时任务（如 cron）来执行它。

```bash
# Default (TX, cryptocurrency keywords)
python3 search.py

# Custom State and Keywords
python3 search.py --state TX --keywords "crypto, bitcoin, blockchain"

# Include passed/completed bills
python3 search.py --state TX --keywords "crypto, bitcoin, blockchain" --all
```

## 配置选项

- `--state`：州的缩写（两个字母，默认值为 `TX` 或环境变量 `LEGISCAN_STATE`）。
- `--keywords`：用逗号分隔的搜索关键词。
- `--all`：如果设置了此参数，将包括已通过或已完成审议的议案。

## 最佳实践
- 该脚本使用环境变量来存储敏感的认证信息。
- 通过命令行参数提供灵活性，无需修改代码。
- 脚本包含了对 API 错误和配置缺失的错误处理机制。