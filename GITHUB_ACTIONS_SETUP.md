# GitHub Actions 配置指南

## 概述
使用GitHub Actions免费实现每日自动推送早报到企业微信。

**优势**：
- ✅ 完全免费（每月2000分钟额度）
- ✅ 24小时自动运行，无需服务器
- ✅ 代码版本管理
- ✅ 推送日志可查看

---

## 配置步骤

### 步骤1：创建GitHub账号和仓库

1. 访问 https://github.com
2. 注册账号（如果还没有）
3. 点击右上角 **+** → **New repository**
4. 填写信息：
   - Repository name: `daily-news-bot`
   - Description: `每日早报自动推送`
   - 选择 **Public**（免费）
   - 勾选 **Add a README file**
   - 点击 **Create repository**

### 步骤2：上传代码

在您的本地项目目录执行：

```bash
# 1. 初始化git（如果还没初始化）
git init

# 2. 添加所有文件
git add .

# 3. 提交代码
git commit -m "Initial commit: Daily news bot"

# 4. 连接远程仓库（替换为您的用户名）
git remote add origin https://github.com/您的用户名/daily-news-bot.git

# 5. 推送代码
git branch -M main
git push -u origin main
```

**如果没有git，也可以手动上传**：
1. 在GitHub仓库页面点击 **Add file** → **Upload files**
2. 拖拽或选择所有项目文件
3. 点击 **Commit changes**

### 步骤3：创建工作流文件

1. 在GitHub仓库页面，点击 **Add file** → **Create new file**
2. 文件路径输入：`.github/workflows/daily-news.yml`
3. 粘贴以下内容：

```yaml
name: Daily News Push

on:
  schedule:
    # UTC时间，北京时间 = UTC + 8
    # 1:00 UTC = 9:00 北京时间（早上）
    # 10:00 UTC = 18:00 北京时间（晚上）
    - cron: '0 1 * * *'
    - cron: '0 10 * * *'
  workflow_dispatch:  # 允许手动触发

jobs:
  push-morning-news:
    runs-on: ubuntu-latest
    if: github.event.schedule == '0 1 * * *' || github.event_name == 'workflow_dispatch'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install uv
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
        
    - name: Run morning news push
      env:
        WECHAT_ROBOT_WEBHOOK_KEY: ${{ secrets.WECHAT_ROBOT_WEBHOOK_KEY }}
      run: |
        uv run python src/main.py -m flow -i '{"search_query":"今日热点","time_range":"1d"}'

  push-evening-news:
    runs-on: ubuntu-latest
    if: github.event.schedule == '0 10 * * *' || github.event_name == 'workflow_dispatch'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install uv
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
        
    - name: Run evening news push
      env:
        WECHAT_ROBOT_WEBHOOK_KEY: ${{ secrets.WECHAT_ROBOT_WEBHOOK_KEY }}
      run: |
        uv run python src/main.py -m flow -i '{"search_query":"今日热点","time_range":"1d"}'
```

4. 点击 **Commit new file**

### 步骤4：设置企业微信密钥

这是最关键的一步！

1. 在GitHub仓库页面，点击 **Settings**
2. 左侧菜单点击 **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写：
   - Name: `WECHAT_ROBOT_WEBHOOK_KEY`
   - Value: `1b207e3a-47aa-441c-af74-50c704bb2014`
5. 点击 **Add secret**

### 步骤5：测试运行

**手动触发测试**：
1. 在GitHub仓库页面，点击 **Actions**
2. 点击左侧的 **Daily News Push**
3. 点击右侧的 **Run workflow** → **Run workflow**
4. 等待运行完成（约1-2分钟）
5. 检查您的企业微信，应该收到早报

---

## 查看运行日志

1. 在GitHub仓库页面，点击 **Actions**
2. 点击最近的一次运行记录
3. 点击具体的任务（如 **push-morning-news**）
4. 查看详细的执行日志

---

## 常见问题

### Q1: 为什么没有按时推送？

**可能原因**：
- GitHub Actions可能有延迟（通常几分钟）
- 代码有错误，查看Actions日志
- Secret配置不正确

**解决方法**：
1. 查看Actions日志排查错误
2. 检查Secret是否正确设置
3. 手动触发测试

### Q2: 如何修改推送时间？

修改 `.github/workflows/daily-news.yml` 中的cron表达式：

```yaml
# 例如改为早上8点和晚上7点
- cron: '0 0 * * *'  # 8:00 UTC+8 = 北京时间8:00
- cron: '0 11 * * *' # 19:00 UTC+8 = 北京时间19:00
```

### Q3: 免费额度有多少？

- **Public仓库**：完全免费，无限制
- **Private仓库**：每月2000分钟免费额度
- 每次推送约1-2分钟，一个月最多约120分钟，完全够用

### Q4: 如何停止自动推送？

**方法1**：删除工作流文件
1. 进入 `.github/workflows/daily-news.yml`
2. 点击右上角垃圾桶图标删除

**方法2**：禁用Actions
1. Settings → Actions → General
2. 选择 **Disable Actions**

---

## 下一步

完成上述配置后：
1. ✅ 明天早上9:00会自动推送早报
2. ✅ 明天晚上18:00会自动推送晚报
3. ✅ 关闭电脑也能正常运行
4. ✅ 可以在GitHub上随时查看推送日志

**现在就开始配置吧！** 🚀
