#!/bin/bash
# 科研文献汇报系统一键安装脚本

echo "=========================================="
echo "科研文献汇报系统 - 一键安装"
echo "=========================================="

# 检查Python版本
echo ""
echo "[1/5] 检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [ -z "$python_version" ]; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi
echo "✅ Python版本: $python_version"

# 安装依赖
echo ""
echo "[2/5] 安装Python依赖..."
pip3 install -q feedparser requests pyyaml --break-system-packages
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖安装完成"

# 创建目录
echo ""
echo "[3/5] 创建目录结构..."
mkdir -p data logs
echo "✅ 目录创建完成"

# 检查配置文件
echo ""
echo "[4/5] 检查配置文件..."
if [ ! -f "config.yaml" ]; then
    echo "⚠️  未找到config.yaml，请复制config.yaml.example并修改配置"
    cp config.yaml config.yaml.example 2>/dev/null || true
else
    echo "✅ 配置文件已存在"
fi

# 测试运行
echo ""
echo "[5/5] 测试运行..."
echo "请先修改config.yaml中的API Key和飞书用户ID，然后运行："
echo ""
echo "  python3 scripts/fetch_papers.py"
echo ""
echo "或设置定时任务："
echo ""
echo "  openclaw cron add literature-report --time '0 9 * * *'"
echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="