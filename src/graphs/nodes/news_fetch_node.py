import os
import re
from datetime import datetime
from zhdate import ZhDate
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import NewsFetchInput, NewsFetchOutput


def get_lunar_date():
    """获取农历日期"""
    now = datetime.now()
    lunar_date = ZhDate.from_datetime(now)

    # 中文数字映射
    chinese_nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

    def num_to_chinese(num):
        if num <= 10:
            return chinese_nums[num]
        elif num < 20:
            return '十' + (chinese_nums[num - 10] if num > 10 else '')
        else:
            tens = num // 10
            units = num % 10
            return chinese_nums[tens] + '十' + (chinese_nums[units] if units > 0 else '')

    month_chinese = num_to_chinese(lunar_date.lunar_month)
    day_chinese = num_to_chinese(lunar_date.lunar_day)

    return f"{month_chinese}月{day_chinese}"


def get_weekday():
    """获取星期"""
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[datetime.now().weekday()]


def get_festival_info():
    """获取今日节日信息"""
    month = datetime.now().month
    day = datetime.now().day
    festivals = {
        "3-18": {
            "name": "全国爱肝日",
            "desc": "在我国乙肝、丙肝、酒精肝等肝炎肝病发病率逐年上升，人民健康面临严重威胁情景下，为动员群众，广泛开展预防肝炎肝病科普知识，保障人民身体健康而设立的节日。"
        },
        "3-12": {
            "name": "植树节",
            "desc": "鼓励人们爱护树木，积极参加植树造林活动，促进国土绿化，保护人类赖以生存的生态环境。"
        },
        "3-8": {
            "name": "妇女节",
            "desc": "庆祝妇女在经济、政治和社会等领域做出的重要贡献和取得的巨大成就。"
        },
        "3-15": {
            "name": "消费者权益日",
            "desc": "保护消费者权益，提高消费者维权意识，促进市场经济健康发展。"
        },
        "4-1": {
            "name": "愚人节",
            "desc": "源于西方的民间传统节日，人们通过各种玩笑和恶作剧互相娱乐。"
        },
        "4-22": {
            "name": "世界地球日",
            "desc": "旨在提高民众对于现有环境问题的意识，动员民众参与到环保运动中。"
        },
        "5-1": {
            "name": "劳动节",
            "desc": "全世界劳动人民团结战斗的节日，纪念劳动人民的伟大贡献。"
        },
        "5-4": {
            "name": "青年节",
            "desc": "纪念五四运动，激励青年继承和发扬五四精神。"
        },
        "6-1": {
            "name": "儿童节",
            "desc": "为了保障世界各国儿童的生存权、保健权和受教育权，抚养权，为了改善儿童的生活。"
        },
        "7-1": {
            "name": "建党节",
            "desc": "纪念中国共产党成立，庆祝党的光辉历程和伟大成就。"
        },
        "8-1": {
            "name": "建军节",
            "desc": "纪念中国人民解放军的成立，向军人致敬。"
        },
        "9-10": {
            "name": "教师节",
            "desc": "表彰教师的贡献，提高教师的社会地位，营造尊师重教的社会氛围。"
        },
        "10-1": {
            "name": "国庆节",
            "desc": "庆祝中华人民共和国成立，彰显国家的繁荣昌盛和民族自豪感。"
        }
    }

    key = f"{month}-{day}"
    return festivals.get(key, None)


def get_daily_quote():
    """获取每日微语"""
    quotes = [
        "不要只因一次失败，就放弃你原来决心想达到的目的。",
        "生活不是等待风暴过去，而是学会在雨中跳舞。",
        "成功的秘诀在于坚持自己的目标和信念。",
        "每一个不曾起舞的日子，都是对生命的辜负。",
        "人生没有白走的路，每一步都算数。",
        "保持热爱，奔赴山海，不忘初心，方得始终。",
        "在这个世界上，没有谁的生活是容易的，大家都在努力活着。",
        "与其抱怨黑暗，不如点亮一盏灯。",
        "生命中最重要的是所经历的过程，而不仅仅是结果。",
        "相信自己，你已经是最好的自己了。",
        "梦想不会逃跑，逃跑的永远是自己。",
        "每天进步一点点，成功就会离你更近一步。"
    ]
    import random
    return random.choice(quotes)


def news_fetch_node(state: NewsFetchInput, config: RunnableConfig, runtime: Runtime[Context]) -> NewsFetchOutput:
    """
    title: 获取热门新闻
    desc: 使用web搜索获取最新的热门新闻，并格式化为早报样式
    integrations: web-search
    """
    ctx = runtime.context

    # 初始化搜索客户端
    search_client = SearchClient(ctx=ctx)

    # 执行搜索，获取10条新闻
    response = search_client.search(
        query=state.search_query,
        search_type="web",
        count=10,
        time_range=state.time_range,
        need_summary=False
    )

    # 提取新闻标题列表
    news_list = []
    if response.web_items:
        for idx, item in enumerate(response.web_items, 1):
            # 清理标题，去除多余信息
            title = item.title or ""
            # 移除HTML标签和多余字符
            title = re.sub(r'<[^>]+>', '', title)
            title = title.strip()

            news_item = {
                "index": idx,
                "title": title,
                "url": item.url or ""
            }
            news_list.append(news_item)

    # 格式化新闻摘要（早报格式）
    # 头部信息
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    weekday = get_weekday()
    lunar_date = get_lunar_date()

    header = f"📰 每日早报，{date_str}，{weekday}，农历{lunar_date}，工作愉快，生活喜乐！"

    # 节日提醒
    festival_info = get_festival_info()
    festival_section = ""
    if festival_info:
        festival_section = f"\n\n🎉 今天是{festival_info['name']}，{festival_info['desc']}"

    # 新闻列表
    news_section = ""
    if news_list:
        for news in news_list:
            news_section += f"\n\n{news['index']}、{news['title']}"
    else:
        news_section = "\n\n今日暂无新闻更新"

    # 微语
    quote = get_daily_quote()
    quote_section = f"\n\n✨【微语】{quote}"

    # 组合完整消息
    news_summary = header + festival_section + news_section + quote_section

    return NewsFetchOutput(
        news_list=news_list,
        news_summary=news_summary
    )
