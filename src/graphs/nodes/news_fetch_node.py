import os
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import NewsFetchInput, NewsFetchOutput


def news_fetch_node(state: NewsFetchInput, config: RunnableConfig, runtime: Runtime[Context]) -> NewsFetchOutput:
    """
    title: 获取热门新闻
    desc: 使用web搜索获取最新的热门新闻
    integrations: web-search
    """
    ctx = runtime.context
    
    # 初始化搜索客户端
    search_client = SearchClient(ctx=ctx)
    
    # 执行搜索
    response = search_client.search(
        query=state.search_query,
        search_type="web",
        count=10,
        time_range=state.time_range,
        need_summary=True
    )
    
    # 提取新闻列表
    news_list = []
    if response.web_items:
        for idx, item in enumerate(response.web_items, 1):
            news_item = {
                "index": idx,
                "title": item.title or "无标题",
                "url": item.url or "",
                "snippet": item.snippet or "",
                "summary": item.summary or "",
                "site_name": item.site_name or "",
                "publish_time": item.publish_time or ""
            }
            news_list.append(news_item)
    
    # 格式化新闻摘要
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_lines = [
        f"📰 **热门新闻简讯** ({current_time})\n",
        f"📅 时间范围：{state.time_range}\n",
        f"🔍 搜索关键词：{state.search_query}\n",
        "-" * 50
    ]
    
    if news_list:
        for news in news_list:
            summary_lines.append(f"\n{news['index']}. **{news['title']}**")
            if news['site_name']:
                summary_lines.append(f"   来源：{news['site_name']}")
            if news['publish_time']:
                summary_lines.append(f"   时间：{news['publish_time']}")
            if news['snippet']:
                snippet = news['snippet'][:100] + "..." if len(news['snippet']) > 100 else news['snippet']
                summary_lines.append(f"   摘要：{snippet}")
            if news['url']:
                summary_lines.append(f"   链接：{news['url']}")
    else:
        summary_lines.append("\n暂无相关新闻")
    
    news_summary = "\n".join(summary_lines)
    
    return NewsFetchOutput(
        news_list=news_list,
        news_summary=news_summary
    )
