# 定时任务配置指南

## 概述
本工作流支持每日自动推送早报，配置以下两个时间点：
- **早上 9:00** - 晨报
- **晚上 18:00** - 晚报

## 方案一：Crontab（推荐，最简单）

### 自动配置（推荐）
```bash
# 给脚本添加执行权限
chmod +x scripts/setup_cron.sh

# 运行配置脚本
bash scripts/setup_cron.sh
```

### 手动配置
```bash
# 编辑crontab
crontab -e

# 添加以下两行（注意修改路径）
0 9 * * * cd /your/project/path && uv run python src/main.py '{"search_query":"今日热点","time_range":"1d"}' >> /your/project/path/logs/morning.log 2>&1
0 18 * * * cd /your/project/path && uv run python src/main.py '{"search_query":"今日热点","time_range":"1d"}' >> /your/project/path/logs/evening.log 2>&1
```

### 查看定时任务
```bash
crontab -l
```

### 删除定时任务
```bash
crontab -e
# 删除相关行后保存
```

---

## 方案二：Systemd Timer（适用于Linux系统）

### 自动配置
```bash
# 使用sudo运行
sudo bash scripts/setup_systemd.sh
```

### 手动配置
```bash
# 1. 复制服务文件到systemd目录
sudo cp scripts/systemd/*.service /etc/systemd/system/
sudo cp scripts/systemd/*.timer /etc/systemd/system/

# 2. 修改文件中的路径为实际路径
sudo sed -i 's|/path/to/your/project|/your/actual/path|g' /etc/systemd/system/*-news.service

# 3. 重新加载systemd
sudo systemctl daemon-reload

# 4. 启用并启动定时器
sudo systemctl enable morning-news.timer evening-news.timer
sudo systemctl start morning-news.timer evening-news.timer

# 5. 查看状态
sudo systemctl list-timers --all
```

### 管理命令
```bash
# 查看定时器状态
sudo systemctl status morning-news.timer

# 查看下次执行时间
sudo systemctl list-timers --all

# 手动触发一次
sudo systemctl start morning-news.service

# 停止定时器
sudo systemctl stop morning-news.timer

# 禁用定时器（开机不启动）
sudo systemctl disable morning-news.timer
```

---

## 方案三：Docker（如果使用Docker部署）

### docker-compose.yml 添加定时任务
```yaml
version: '3.8'

services:
  news-bot:
    build: .
    container_name: morning-news-bot
    environment:
      - WECHAT_ROBOT_WEBHOOK_KEY=${WECHAT_ROBOT_WEBHOOK_KEY}
    volumes:
      - ./logs:/app/logs
    command: >
      sh -c "echo '0 9 * * * cd /app && uv run python src/main.py'
             > /etc/crontabs/root
             && echo '0 18 * * * cd /app && uv run python src/main.py'
             >> /etc/crontabs/root
             && crond -f"
```

---

## 方案四：云平台定时触发

### 阿里云函数计算
配置定时触发器：
```yaml
triggers:
  - name: morning-trigger
    type: timer
    config: 
      cron: '0 9 * * * *'
      enable: true
  - name: evening-trigger
    type: timer
    config:
      cron: '0 18 * * * *'
      enable: true
```

### 腾讯云云函数
在控制台配置定时触发：
- 触发周期：自定义
- Cron表达式：`0 9 * * *`（早上9点）
- Cron表达式：`0 18 * * *`（晚上6点）

---

## 日志查看

### Crontab方案
```bash
# 查看早上推送日志
tail -f logs/morning.log

# 查看晚上推送日志
tail -f logs/evening.log

# 查看所有日志
ls -la logs/
```

### Systemd方案
```bash
# 查看服务日志
sudo journalctl -u morning-news.service -f

# 查看日志文件
tail -f logs/morning.log
```

---

## 常见问题

### Q1: 定时任务没有执行？
**检查步骤：**
1. 检查crontab是否正确添加：`crontab -l`
2. 检查uv命令路径：`which uv`
3. 检查项目路径是否正确
4. 查看日志文件是否有错误

### Q2: 如何测试定时任务？
```bash
# 手动运行一次
uv run python src/main.py '{"search_query":"今日热点","time_range":"1d"}'

# 或者修改crontab为每分钟执行一次测试
* * * * * cd /your/path && uv run python src/main.py
```

### Q3: 如何修改推送时间？
编辑crontab或systemd timer文件，修改时间即可。

**Crontab时间格式：**
```
分钟 小时 日 月 星期
0     9   *  *   *    # 每天9:00
0    18   *  *   *    # 每天18:00
```

### Q4: 如何临时禁用？
**Crontab：** 在任务行前加 `#` 注释掉
**Systemd：** `sudo systemctl stop morning-news.timer`

---

## 推荐选择

| 方案 | 适用场景 | 难度 | 推荐指数 |
|------|----------|------|----------|
| Crontab | 大多数Linux/Unix系统 | ⭐ | ⭐⭐⭐⭐⭐ |
| Systemd | 现代Linux发行版 | ⭐⭐ | ⭐⭐⭐⭐ |
| Docker | 容器化部署 | ⭐⭐ | ⭐⭐⭐ |
| 云平台 | 云函数部署 | ⭐ | ⭐⭐⭐⭐ |

**最简单的方式：** 运行 `bash scripts/setup_cron.sh`
