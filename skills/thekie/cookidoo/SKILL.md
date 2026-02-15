---
name: cookidoo
description: 通过非官方的 cookidoo-api Python 包，您可以访问 Cookidoo（Thermomix）的食谱、购物清单以及 meal planning 功能。该包可用于查看食谱、每周的饮食计划、收藏的食谱，并将所需食材信息同步到购物清单中。
---

# Cookidoo

用于访问 Cookidoo（Thermomix）的食谱、购物清单和膳食计划功能。

## 所需凭据

| 变量          | 是否必需 | 说明                          |
|--------------|---------|-------------------------------------------|
| `COOKIDOO_EMAIL`  | ✅       | 你的 Cookidoo 账户邮箱                |
| `COOKIDOO_PASSWORD` | ✅       | 你的 Cookidoo 账户密码                |
| `COOKIDOO_COUNTRY` | 可选      | 国家代码（默认：DE）                     |
| `COOKIDOO_LANGUAGE` | 可选      | 语言代码（默认：de-DE）                     |

请将这些凭据设置到环境变量中或 `~/.config/atlas/cookidoo.env` 文件中：
```bash
COOKIDOO_EMAIL=your@email.com
COOKIDOO_PASSWORD=yourpassword
```

## 依赖项

```bash
pip install cookidoo-api
```

## 功能

### 列出保存的食谱
```bash
python scripts/cookidoo_cli.py recipes
```

### 获取每周膳食计划
```bash
python scripts/cookidoo_cli.py plan
```

### 从 Cookidoo 获取购物清单
```bash
python scripts/cookidoo_cli.py shopping
```

### 搜索食谱
```bash
python scripts/cookidoo_cli.py search "Pasta"
```

### 查看食谱详情
```bash
python scripts/cookidoo_cli.py recipe <recipe_id>
```

### 获取账户信息
```bash
python scripts/cookidoo_cli.py info
```

## 命令行选项

- `--json`    — 以 JSON 格式输出结果
- `--limit N`   — 限制结果数量（默认：10）

## 集成建议

- 将 Cookidoo 的购物清单同步到 Bring! 应用程序
- 根据当季食材推荐食谱
- 提供每周膳食计划辅助
- 导出选定食谱的食材清单

## 注意事项

- 需要订阅 Cookidoo 服务才能使用该工具
- 该工具使用的 API 是非官方的，可能会因 Cookidoo 的更新而失效
- 请妥善保管凭据（切勿将其存储在技能文件（skill folder）中）