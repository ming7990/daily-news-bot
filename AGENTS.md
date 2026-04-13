## 项目概述
- **名称**: 热门新闻企业微信推送工作流
- **功能**: 每日定时获取top10热门新闻简讯，并通过企业微信机器人发送到指定群组

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| news_fetch | `nodes/news_fetch_node.py` | task | 使用web搜索获取热门新闻并格式化为早报 | - | - |
| wechat_send | `nodes/wechat_send_node.py` | task | 将新闻发送到企业微信 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
无

## 技能使用
- 节点`news_fetch`使用web-search技能
- 节点`wechat_send`使用企业微信机器人技能

## 工作流输入参数
- `search_query` (str): 搜索关键词，默认"今日热点新闻"
- `time_range` (str): 时间范围，默认"1d"（一天内）

## 工作流输出参数
- `send_result` (dict): 企业微信发送结果，包含success、errcode、errmsg、message_count等字段

## 消息格式说明
早报格式包含以下部分：
1. **头部信息**：日期、星期、农历、问候语
2. **节日提醒**：如果是特殊节日，显示节日名称和介绍
3. **新闻列表**：10条简短新闻标题，每条之间有空行隔开
4. **今日心语**：每日励志语录，传递正能量

## 定时任务配置
本工作流支持每日自动推送早报，需要配置定时任务。

### ✅ 已配置完成（当前环境）
调度器已启动并运行中！

```bash
# 查看调度器状态
ps aux | grep scheduler.py

# 查看调度日志
tail -f logs/scheduler.log

# 停止调度器
bash stop_scheduler.sh

# 重新启动调度器
bash start_scheduler.sh
```

### 推送时间
- **早上 9:00** - 晨报
- **晚上 18:00** - 晚报

### 其他配置方式
如果需要在其他环境配置，支持以下方案：

**方式1: Crontab（Linux/Mac）**
```bash
bash scripts/setup_cron.sh
```

**方式2: Systemd（现代Linux）**
```bash
sudo bash scripts/setup_systemd.sh
```

**方式3: Python调度器（当前使用的方案）**
```bash
bash start_scheduler.sh
```

详细配置说明请参考 `docs/cron_setup.md` 文档。

## 企业微信配置说明
在使用前，需要配置企业微信机器人集成：
1. 在企业微信中创建机器人并获取webhook地址
2. 在工作流配置中添加企业微信机器人集成凭证
3. 凭证中需包含webhook_url或webhook_key字段

## 注意事项
- 新闻数量固定为10条
- 时间范围默认为1天，可根据需要调整（如"1w"表示一周内）
- 使用zhdate库计算农历日期
- 包含节日提醒功能（内置常见节日列表）
- 每日心语从预设语录库中随机选择
- 消息格式严格按照早报样式输出
- 每条新闻之间有空行隔开，便于阅读
