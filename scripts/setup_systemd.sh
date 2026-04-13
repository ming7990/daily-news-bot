#!/bin/bash

# Systemd定时任务配置脚本
# 适用于使用systemd的Linux系统（如Ubuntu 16.04+, CentOS 7+, Debian 8+）

set -e

# 获取项目绝对路径
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SERVICE_DIR="$PROJECT_DIR/scripts/systemd"

echo "========================================="
echo "Systemd定时任务配置"
echo "========================================="
echo ""
echo "项目路径: $PROJECT_DIR"
echo ""

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  请使用sudo运行此脚本"
    echo "   sudo bash scripts/setup_systemd.sh"
    exit 1
fi

# 创建日志目录
mkdir -p "$PROJECT_DIR/logs"

# 复制并修改服务文件
for service in morning-news evening-news; do
    # 读取模板并替换路径
    sed -e "s|/path/to/your/project|$PROJECT_DIR|g" \
        "$SERVICE_DIR/$service.service" \
        > "/etc/systemd/system/$service.service"
    
    # 复制定时器文件
    cp "$SERVICE_DIR/$service.timer" "/etc/systemd/system/"
    
    echo "✅ 已创建: /etc/systemd/system/$service.service"
    echo "✅ 已创建: /etc/systemd/system/$service.timer"
done

echo ""
echo "重新加载systemd配置..."
systemctl daemon-reload

echo ""
echo "启用定时器..."
systemctl enable morning-news.timer
systemctl enable evening-news.timer

echo ""
echo "启动定时器..."
systemctl start morning-news.timer
systemctl start evening-news.timer

echo ""
echo "========================================="
echo "✅ Systemd定时任务配置成功!"
echo "========================================="
echo ""
echo "定时任务状态:"
systemctl list-timers --all | grep news

echo ""
echo "下次运行时间:"
systemctl list-timers --all | grep news | awk '{print $1, $2}'

echo ""
echo "查看日志命令:"
echo "• 早上推送: tail -f $PROJECT_DIR/logs/morning.log"
echo "• 晚上推送: tail -f $PROJECT_DIR/logs/evening.log"

echo ""
echo "管理服务命令:"
echo "• 查看状态: sudo systemctl status morning-news.timer"
echo "• 停止服务: sudo systemctl stop morning-news.timer"
echo "• 禁用服务: sudo systemctl disable morning-news.timer"
