import datetime
from datetime import date, timedelta, timezone
from typing import List, TypedDict

import requests
from bs4 import BeautifulSoup


class Article(TypedDict):
    title: str
    date: str
    url: str
    queryAt: datetime


base_url = "https://www.ptt.cc"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9",
    "Connection": "keep-alive",
}


def get_soup(url: str):
    try:
        r = requests.get(url, headers=headers, timeout=5)  # 加上 timeout
        r.raise_for_status()  # 如果狀態碼不是 200，會拋出 HTTPError
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
        return None


def get_full_url(route: str):
    return f"{base_url}{route}"


# 2. 定義格式化邏輯
def format_date_custom(date_obj):
    """格式化單個日期為 M/DD"""
    month = date_obj.month  # 月份 (數字，不補零)
    # 使用 f-string 的格式化功能 :02d 確保日期 (day) 永遠補零到兩位數
    day_formatted = f"{date_obj.day:02d}"

    # 組合結果
    return f"{month}/{day_formatted}"


def get_today_and_yesterday_dates_custom():
    """
    取得今天和昨天的日期，並格式化為 'M/DD' 字串 (月份不補零，日期補零)。

    回傳:
        tuple: (today_date, yesterday_date)
               例如: ('10/01', '9/30')
    """
    # 1. 取得日期物件
    today = date.today()
    yesterday = today - timedelta(days=1)

    # 3. 應用格式化
    today_formatted = format_date_custom(today)
    yesterday_formatted = format_date_custom(yesterday)

    return (today_formatted, yesterday_formatted)


def get_ptt_free_articles():
    current_dt_utc = datetime.datetime.now(timezone.utc)
    today_str, yesterday_str = get_today_and_yesterday_dates_custom()

    print(f"TO {today_str}; YE {yesterday_str}")

    url = get_full_url("/bbs/Steam/index.html")

    article_list: List[Article] = []

    is_continue = True

    while is_continue:
        print(f"爬取網址 {url}")

        soup = get_soup(url)
        articles = soup.select(".r-list-container .r-ent")

        if len(articles) == 0:
            print("文章數量為 0")
            is_continue = False
            break

        print(f"取得 {len(articles)} 個文章，開始解析")
        tmp_list: List[Article] = []

        for article in articles:
            # print(article.prettify(), end="\r\n")

            # 過濾符合條件的文章
            date_element = article.find(class_="date")
            if not date_element:
                print("找不到日期 html tag")
                continue

            date_str = date_element.text.strip()
            if not date_str:
                print("找不到日期文字")
                continue

            if date_str != today_str and date_str != yesterday_str:
                # DEBUG 用
                # print(f"非兩天內的遊戲文章 {date_str} {today_str} {yesterday_str}")
                continue

            title_element = article.find(class_="title")
            title_str = "無標題"
            if title_element:
                title_str = title_element.text.strip()

            # DEBUG 用
            # if "限免" not in title_str or "Re:" in title_str:
            #     print(f"[非限免遊戲] {date_str} - {title_str}")
            #     continue

            # select = document.querySelectorAll 回傳 list
            # select_one = document.querySelector 回傳一個 node 節點
            aTag = article.select_one(".title a")
            url = "no-url-available"

            if aTag:
                href = aTag.get("href")
                url = get_full_url(href)

            # DEBUG 用
            # print(f"[遊戲] {date_str} - {title_str}")

            tmp_list.insert(
                0,
                {
                    "title": title_str,
                    "date": date_str,
                    "url": url,
                    "queryAt": current_dt_utc,
                },
            )

        if len(tmp_list) != 0:
            target_list = [
                item
                for item in tmp_list
                if "限免" in item["title"] and "Re:" not in item["title"]
            ]

            # DEBUG 用
            # print([i["title"] for i in target_list])

            article_list.extend(target_list)

            pre_btn_element = soup.select_one(".action-bar .btn.wide:nth-child(2)")
            if pre_btn_element:
                pre_url = pre_btn_element.get("href")
                url = get_full_url(pre_url)
                print(f"上一頁網址: {url}")
        else:
            is_continue = False

    return article_list
