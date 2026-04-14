# 早报机器人 - 云端部署指南

## 配置状态

✅ **已完成**: 所有代码文件已准备就绪
⚠️ **待完成**: 代码推送 + GitHub Secrets配置

---

## 快速配置步骤（约5分钟）

### 步骤1: 准备代码

所有文件已在 `/workspace/projects` 目录中准备完毕。

```bash
cd /workspace/projects
```

### 步骤2: 生成新的GitHub Token

由于当前Token权限不足，需要创建新的Token：

1. 访问: https://github.com/settings/tokens/new
2. 填写Token名称: `DailyNewsBot Deploy`
3. 勾选以下权限：
   - ✅ `repo` (完整仓库权限)
   - ✅ `workflow` (Actions工作流权限)
4. 点击 "Generate token"
5. **复制生成的Token**（只显示一次！）

### 步骤3: 推送代码

使用新Token推送代码：

```bash
# 设置远程仓库地址（替换YOUR_NEW_TOKEN为实际Token）
git remote set-url origin https://ming7990:YOUR_NEW_TOKEN@github.com/ming7990/daily-news-bot.git

# 推送代码
git push -u origin main --force
```

### 步骤4: 设置Secrets

访问GitHub页面设置Secret：

1. 打开: https://github.com/ming7990/daily-news-bot/settings/secrets/actions
2. 点击绿色按钮: **"New repository secret"**
3. 填写：
   - **Name**: `WECHAT_ROBOT_WEBHOOK_KEY`
   - **Value**: `1b207e3a-47aa-441c-af74-50c704bb2014`
4. 点击 **"Add secret"**

### 步骤5: 测试运行

1. 访问: https://github.com/ming7990/daily-news-bot/actions
2. 点击 **"Daily News Push"**
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 等待1-2分钟
5. 检查企业微信是否收到消息！

---

## 配置验证

配置成功后，您将看到：

✅ 代码已推送到GitHub仓库
✅ GitHub Actions页面显示工作流
✅ 企业微信群收到测试消息
✅ 每天9:00和18:00自动推送

---

## 常见问题

### Q: 推送时提示密码验证失败？
A: 需要使用Personal Access Token代替密码，详见步骤2。

### Q: 测试运行时显示红色失败？
A: 检查Secrets是否正确设置，查看Actions日志获取详细错误。

### Q: 企业微信没收到消息？
A: 
- 检查Webhook Key是否正确
- 检查企业微信机器人是否启用
- 查看Actions日志中的错误信息

---

## 支持

如有问题，请：
1. 查看Actions运行日志
2. 检查所有配置是否正确
3. 联系技术支持
