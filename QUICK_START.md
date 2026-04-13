# 早报推送工作流 - 快速开始

## 1. 配置企业微信机器人（已完成 ✅）

Webhook Key 已配置在 `.env` 文件中。

## 2. 配置定时任务（选择一种方式）

### 方式A: 自动配置 Crontab（推荐）
```bash
bash scripts/setup_cron.sh
```
按提示确认即可。

### 方式B: 自动配置 Systemd
```bash
sudo bash scripts/setup_systemd.sh
```

### 方式C: 手动配置 Crontab
```bash
crontab -e
```
添加：
```
0 9 * * * cd $(pwd) && uv run python src/main.py '{"search_query":"今日热点","time_range":"1d"}'
0 18 * * * cd $(pwd) && uv run python src/main.py '{"search_query":"今日热点","time_range":"1d"}'
```

## 3. 立即测试

```bash
# 手动运行一次测试
uv run python src/main.py '{"search_query":"今日热点","time_range":"1d"}'
```

## 4. 查看推送时间

配置完成后，下次推送时间：
- **早上 9:00**
- **晚上 18:00**

## 5. 查看日志

```bash
# 实时查看日志
tail -f logs/morning.log
tail -f logs/evening.log
```

## 常见问题

**Q: 定时任务没有执行？**
A: 检查 `crontab -l` 是否正确添加，路径是否正确。

**Q: 如何停止定时推送？**
A: 
```bash
# Crontab方案
crontab -e
# 删除相关行

# Systemd方案
sudo systemctl stop morning-news.timer evening-news.timer
sudo systemctl disable morning-news.timer evening-news.timer
```

**Q: 如何修改推送时间？**
A: 编辑 `scripts/setup_cron.sh` 中的时间配置，重新运行。

---

**现在运行 `bash scripts/setup_cron.sh` 即可完成所有配置！**
