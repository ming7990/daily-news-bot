# GitHub Actions 快速配置（5分钟完成）

## 📋 准备工作
- [ ] GitHub账号（没有就去 https://github.com 注册）
- [ ] 企业微信机器人已配置好

---

## 步骤1：创建GitHub仓库（1分钟）

1. 打开 https://github.com
2. 点击右上角 **+** → **New repository**
3. 填写：
   - Repository name: `daily-news-bot`
   - 选择 **Public**
   - 勾选 **Add a README file**
   - 点击 **Create repository**

---

## 步骤2：上传代码（2分钟）

### 方式A：使用git命令
```bash
cd /workspace/projects  # 您的项目目录
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/您的用户名/daily-news-bot.git
git push -u origin main
```

### 方式B：网页上传（更简单）
1. 在GitHub仓库页面，点击 **Add file** → **Upload files**
2. 拖拽所有文件到网页
3. 点击 **Commit changes**

---

## 步骤3：创建工作流文件（1分钟）

1. 在GitHub仓库页面，点击 **Add file** → **Create new file**
2. 文件名输入：`.github/workflows/daily-news.yml`
3. **复制粘贴** 以下内容：

```yaml
name: Daily News Push

on:
  schedule:
    - cron: '0 1 * * *'   # 北京时间9:00
    - cron: '0 10 * * *'  # 北京时间18:00
  workflow_dispatch:

jobs:
  push-news:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    - env:
        WECHAT_ROBOT_WEBHOOK_KEY: ${{ secrets.WECHAT_ROBOT_WEBHOOK_KEY }}
      run: |
        uv run python src/main.py -m flow -i '{"search_query":"今日热点","time_range":"1d"}'
```

4. 点击 **Commit new file**

---

## 步骤4：设置密钥（1分钟）⭐关键步骤

1. 在GitHub仓库页面，点击 **Settings**
2. 左侧点击 **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写：
   - **Name**: `WECHAT_ROBOT_WEBHOOK_KEY`
   - **Value**: `1b207e3a-47aa-441c-af74-50c704bb2014`
5. 点击 **Add secret**

---

## 步骤5：测试运行

1. 在GitHub仓库页面，点击 **Actions**
2. 点击 **Daily News Push**
3. 点击 **Run workflow** → **Run workflow**
4. 等待1-2分钟
5. 查看您的企业微信，应该收到早报！

---

## ✅ 完成！

**明天开始，您将每天收到：**
- 🌅 早上 9:00 自动推送早报
- 🌆 晚上 18:00 自动推送晚报

**关闭电脑也能正常运行！**

---

## 🔍 查看日志

如果收不到消息，查看日志排查：
1. 在GitHub仓库页面，点击 **Actions**
2. 点击最近的一次运行记录
3. 查看错误信息

---

**遇到问题？** 查看详细文档：`GITHUB_ACTIONS_SETUP.md`
