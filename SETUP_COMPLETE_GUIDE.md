# 🚀 一键完成 GitHub Actions 配置

## 您只需要做这3件事：

---

## 第1步：在GitHub创建仓库（2分钟）

1. 打开 https://github.com/new
2. 输入 Repository name: `daily-news-bot`
3. 选择 **Public**
4. 勾选 ☑️ **Add a README file**
5. 点击 **Create repository**
6. **复制仓库地址**（例如：`https://github.com/您的用户名/daily-news-bot.git`）

---

## 第2步：上传代码（1分钟）

**在下方输入您的GitHub用户名，我会生成完整的命令：**

假设您的GitHub用户名是：`yourname`

```bash
# 设置远程仓库地址（替换 yourname 为您的用户名）
git remote add origin https://github.com/yourname/daily-news-bot.git

# 推送代码
git push -u origin main
```

**执行完上述命令后，刷新GitHub页面，应该能看到所有代码**

---

## 第3步：设置密钥（2分钟）⭐最重要

1. 打开您的GitHub仓库页面
2. 点击顶部 **Settings** 标签
3. 左侧菜单点击 **Secrets and variables** → **Actions**
4. 点击绿色按钮 **New repository secret**
5. 填写：
   - **Name**: `WECHAT_ROBOT_WEBHOOK_KEY`
   - **Value**: `1b207e3a-47aa-441c-af74-50c704bb2014`
6. 点击 **Add secret**

---

## ✅ 完成！自动推送已启用

**GitHub Actions 工作流已包含在代码中**（`.github/workflows/daily-news.yml`），代码推送后会自动生效。

### 测试一下：
1. 在GitHub仓库页面，点击 **Actions**
2. 点击 **Daily News Push**
3. 点击右侧 **Run workflow** → **Run workflow**
4. 等待1-2分钟
5. **检查您的企业微信群，应该收到早报！**

---

## ⏰ 推送时间表

从明天开始：
- 🌅 **每天 9:00** 自动推送晨报
- 🌆 **每天 18:00** 自动推送晚报

**关闭电脑、关闭浏览器也能正常运行！**

---

## 🔧 如果第2步遇到问题

### 情况A：提示需要登录
```bash
# 会弹出窗口让您登录GitHub
git push -u origin main
```

### 情况B：提示权限错误
使用Token方式：
```bash
# 1. 去 https://github.com/settings/tokens 生成token
# 2. 使用token推送
git remote set-url origin https://您的用户名:token@github.com/您的用户名/daily-news-bot.git
git push -u origin main
```

### 情况C：不想用命令行
直接在GitHub网页上传：
1. GitHub仓库页面 → **Add file** → **Upload files**
2. 拖拽或选择所有项目文件
3. 点击 **Commit changes**
4. 确保 `.github/workflows/daily-news.yml` 文件已上传

---

## 📞 配置完成检查清单

- [ ] 在GitHub创建了名为 `daily-news-bot` 的仓库
- [ ] 代码已推送到GitHub（能看到所有文件）
- [ ] 在Settings → Secrets中添加了 `WECHAT_ROBOT_WEBHOOK_KEY`
- [ ] 在Actions页面手动运行测试成功
- [ ] 企业微信收到了测试消息

**完成以上5项，就大功告成了！** 🎉

---

## ❓ 常见问题

**Q: 提示 "reinitialized existing git repository"？**  
A: 正常，说明git已初始化，继续执行即可。

**Q: 提示 "failed to push some refs"？**  
A: 先在GitHub创建README文件，或执行 `git pull origin main` 后再push

**Q: 企业微信没收到消息？**  
A: 检查Actions页面的运行日志，看错误信息

---

## 🆘 还是搞不定？

**提供以下信息给我：**
1. 您的GitHub用户名
2. 遇到的错误截图或文字

我可以进一步帮您解决！
