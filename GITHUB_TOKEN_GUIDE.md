# GitHub Token 创建指南

## 为什么需要Token？
GitHub在2021年后不再支持密码验证，需要使用Personal Access Token。

## 创建步骤

1. 登录GitHub账号
2. 访问 https://github.com/settings/tokens
3. 点击 **Generate new token** → **Generate new token (classic)**
4. 填写：
   - Note: `Daily News Bot`
   - Expiration: 选择 **No expiration**（永不过期）
   - 勾选以下权限：
     - [x] **repo** （完整仓库权限）
5. 点击 **Generate token**
6. **复制生成的Token**（类似：`ghp_xxxxxxxxxxxxxxxxxxxx`）

## 使用Token推送代码

```bash
# 使用Token推送（替换 YOUR_TOKEN 为实际Token）
git remote set-url origin https://ming7990:YOUR_TOKEN@github.com/ming7990/daily-news-bot.git
git push -u origin main --force
```

## Token保存好！
Token只显示一次，请保存好，后续配置Secrets也需要使用。
