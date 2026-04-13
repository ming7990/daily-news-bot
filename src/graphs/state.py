from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class GlobalState(BaseModel):
    """全局状态定义"""
    news_list: List[Dict] = Field(default=[], description="获取的新闻列表")
    news_summary: str = Field(default="", description="新闻摘要文本")
    send_result: Dict = Field(default={}, description="企业微信发送结果")


class GraphInput(BaseModel):
    """工作流的输入"""
    search_query: str = Field(default="今日热门新闻", description="搜索关键词，默认为'今日热门新闻'")
    time_range: str = Field(default="1d", description="时间范围，默认为1天（1d）")


class GraphOutput(BaseModel):
    """工作流的输出"""
    send_result: Dict = Field(..., description="企业微信发送结果")


class NewsFetchInput(BaseModel):
    """获取热门新闻节点的输入"""
    search_query: str = Field(..., description="搜索关键词")
    time_range: str = Field(..., description="时间范围，如1d、1w、1m")


class NewsFetchOutput(BaseModel):
    """获取热门新闻节点的输出"""
    news_list: List[Dict] = Field(..., description="获取的新闻列表")
    news_summary: str = Field(..., description="新闻摘要文本")


class WechatSendInput(BaseModel):
    """企业微信发送节点的输入"""
    news_list: List[Dict] = Field(..., description="新闻列表")
    news_summary: str = Field(..., description="新闻摘要")


class WechatSendOutput(BaseModel):
    """企业微信发送节点的输出"""
    send_result: Dict = Field(..., description="发送结果")
