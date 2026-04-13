import os
import json
import re
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_workload_identity import Client
from cozeloop.decorator import observe
from graphs.state import WechatSendInput, WechatSendOutput

# 加载.env文件（用于开发测试）
load_dotenv()


def get_webhook_key():
    """从集成凭证或环境变量中获取企业微信机器人webhook key"""
    # 方式1: 优先从集成凭证获取
    try:
        client = Client()
        wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")

        # 检查返回的凭证是否为字符串
        if not isinstance(wechat_bot_credential, str):
            raise Exception(f"凭证类型错误，期望字符串，得到 {type(wechat_bot_credential)}")

        credential_dict = json.loads(wechat_bot_credential)

        # 首先尝试直接获取webhook_key
        if "webhook_key" in credential_dict:
            webhook_key = credential_dict["webhook_key"]
        # 如果没有webhook_key，尝试从webhook_url中提取
        elif "webhook_url" in credential_dict:
            webhook_url = credential_dict["webhook_url"]
            match = re.search(r"key=([a-zA-Z0-9-]+)", webhook_url)
            if match:
                webhook_key = match.group(1)
            else:
                raise Exception(f"无法从webhook_url中提取webhook_key: {webhook_url}")
        else:
            raise Exception(f"凭证中既没有webhook_key也没有webhook_url字段，包含字段: {list(credential_dict.keys())}")

        return webhook_key
    except Exception as e:
        # 如果集成凭证获取失败，尝试从环境变量读取（备选方案）
        webhook_key = os.getenv("WECHAT_ROBOT_WEBHOOK_KEY")
        if webhook_key:
            return webhook_key

        # 如果都没有，抛出详细的错误提示
        raise Exception(
            f"无法获取企业微信webhook_key。\n"
            f"集成凭证错误: {str(e)}\n"
            f"请选择以下任一方式配置：\n"
            f"1. 在平台配置企业微信机器人集成凭证（推荐）\n"
            f"2. 设置环境变量 WECHAT_ROBOT_WEBHOOK_KEY"
        )


@observe
def wechat_send_node(state: WechatSendInput, config: RunnableConfig, runtime: Runtime[Context]) -> WechatSendOutput:
    """
    title: 发送企业微信消息
    desc: 将新闻简讯发送到企业微信群组
    integrations: 企业微信机器人
    """
    ctx = runtime.context
    
    # 构建markdown格式的消息内容
    markdown_content = state.news_summary

    # 检查消息长度（企业微信markdown限制4096字节）
    message_bytes = len(markdown_content.encode('utf-8'))
    if message_bytes > 4096:
        # 如果消息过长，只保留前5条新闻
        lines = markdown_content.split('\n\n')
        header_parts = []
        news_parts = []
        collecting_news = False

        for line in lines:
            if collecting_news:
                if line.strip().startswith(('1、', '2、', '3、', '4、', '5、')):
                    news_parts.append(line)
            else:
                header_parts.append(line)
                if '微语' not in line and line.strip():
                    # 检查是否开始新闻列表（有数字序号）
                    if any(line.strip().startswith(f"{i}、") for i in range(1, 11)):
                        collecting_news = True
                        news_parts.append(line)

        markdown_content = '\n\n'.join(header_parts) + '\n\n' + '\n\n'.join(news_parts) + '\n\n✨【今日心语】消息较长，仅显示前5条新闻'
    
    # 调用企业微信API发送消息
    try:
        # 这里需要实现企业微信发送逻辑
        # 由于企业微信API需要HTTP调用，这里使用requests库
        import requests
        
        webhook_key = get_webhook_key()
        send_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "msgtype": "text",
            "text": {"content": markdown_content}
        }
        
        response = requests.post(send_url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        if result.get("errcode", 0) != 0:
            raise Exception(f"发送失败: {result}")
        
        send_result = {
            "success": True,
            "errcode": result.get("errcode", 0),
            "errmsg": result.get("errmsg", "success"),
            "message_count": len(state.news_list)
        }
        
    except Exception as e:
        # 返回真实的错误信息，便于排查问题
        send_result = {
            "success": False,
            "error": str(e),
            "message_count": 0
        }

    return WechatSendOutput(send_result=send_result)
