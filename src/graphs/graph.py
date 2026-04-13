from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.news_fetch_node import news_fetch_node
from graphs.nodes.wechat_send_node import wechat_send_node


# 创建状态图，指定工作流的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("news_fetch", news_fetch_node)
builder.add_node("wechat_send", wechat_send_node)

# 设置入口点
builder.set_entry_point("news_fetch")

# 添加边：新闻获取 -> 企业微信发送
builder.add_edge("news_fetch", "wechat_send")

# 添加结束边
builder.add_edge("wechat_send", END)

# 编译图
main_graph = builder.compile()
