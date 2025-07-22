#!/bin/bash

echo "🐍 Python 技能图谱可视化系统"
echo "================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查依赖是否安装
echo "🔍 检查依赖..."
python3 -c "import flask, pandas, openpyxl, flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  依赖包未完全安装，正在安装..."
    pip install --break-system-packages Flask pandas openpyxl flask-cors werkzeug
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动运行："
        echo "pip install Flask pandas openpyxl flask-cors werkzeug"
        exit 1
    fi
fi

echo "✅ 依赖检查完成"

# 创建必要的目录
mkdir -p uploads

echo ""
echo "🚀 启动服务器..."
echo "📱 访问地址: http://localhost:5000"
echo "📝 按 Ctrl+C 停止服务器"
echo ""

# 启动Flask应用
python3 app.py