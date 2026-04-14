#!/bin/bash
# 最终配置脚本 - 请手动执行

echo "========================================="
echo "早报机器人 - 最终配置"
echo "========================================="
echo ""
echo "由于Token权限限制，请按以下步骤手动完成配置："
echo ""

# 步骤1：推送代码
echo "步骤1: 推送代码到GitHub"
echo "请执行以下命令："
echo ""
echo "cd /workspace/projects"
echo "git remote set-url origin https://ming7990:$TOKEN@github.com/ming7990/daily-news-bot.git"
echo "git push -u origin main --force"
echo ""

# 步骤2：设置Secrets
echo "步骤2: 设置GitHub Secrets（关键步骤）"
echo ""
echo "1. 打开浏览器访问:"
echo "   https://github.com/ming7990/daily-news-bot/settings/secrets/actions"
echo ""
echo "2. 点击绿色按钮: 'New repository secret'"
echo ""
echo "3. 填写以下信息："
echo "   Name: WECHAT_ROBOT_WEBHOOK_KEY"
echo "   Value: 1b207e3a-47aa-441c-af74-50c704bb2014"
echo ""
echo "4. 点击 'Add secret'"
echo ""

# 步骤3：测试
echo "步骤3: 测试运行"
echo ""
echo "1. 访问: https://github.com/ming7990/daily-news-bot/actions"
echo "2. 点击 'Daily News Push'"
echo "3. 点击 'Run workflow' -> 'Run workflow'"
echo "4. 等待1-2分钟"
echo "5. 检查企业微信是否收到消息"
echo ""

echo "========================================="
echo "配置完成后，每天9:00和18:00自动推送！"
echo "========================================="
