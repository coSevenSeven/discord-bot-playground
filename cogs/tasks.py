import datetime
import traceback
from datetime import timezone

import discord
from discord.ext import commands, tasks

from utils.bot import Bot
from utils.ptt import get_ptt_free_articles
from utils.settings import settings

notify_time = [
    datetime.time(hour=0),
    datetime.time(hour=12),
]
LAST_EXECUTION_TIME = max(notify_time)

# 定義一個時間容錯範圍 (例如 5 分鐘)
# 任務必須在這個時間容錯範圍內執行才算數
GUARD_TIME = datetime.timedelta(minutes=5)


class Task(commands.Cog):
    def __init__(self, bot: Bot):
        print("init task")

        self.bot = bot
        self.check_task.start()

    def cog_unload(self):
        self.check_task.cancel()

    @staticmethod
    def is_last_execution_time() -> bool:
        # 獲取當前的 UTC 時區感知 datetime 物件
        current_dt_utc = datetime.datetime.now(timezone.utc)

        # 獲取今天 (UTC) 最後執行時間的完整 datetime 物件
        last_exec_dt_utc = current_dt_utc.replace(
            hour=LAST_EXECUTION_TIME.hour,
            minute=LAST_EXECUTION_TIME.minute,
            second=0,
            microsecond=0,
        )

        # 定義一個時間範圍：從預期時間點前 5 分鐘，到預期時間點後 5 分鐘。
        # 這樣可以處理延遲啟動（+差值）和提前啟動（-差值）兩種情況。

        # 時間窗的開始點 (預期時間 - 緩衝)
        start_window = last_exec_dt_utc - GUARD_TIME

        # 時間窗的結束點 (預期時間 + 緩衝)
        end_window = last_exec_dt_utc + GUARD_TIME

        # 3. 檢查當前時間是否落在這個時間窗內
        return start_window <= current_dt_utc <= end_window

    @tasks.loop(time=notify_time)
    async def check_task(self):
        try:
            channel = self.bot.get_channel(int(settings.CHANNEL_ID))

            if not channel:
                print("no channel found.")
                return

            articles = get_ptt_free_articles()

            # 關鍵過濾邏輯：使用列表推導式
            existing_urls = self.bot.storage.ptt_articles.keys()

            new_articles = [
                article for article in articles if article["url"] not in existing_urls
            ]

            if len(new_articles) == 0:
                embed = discord.Embed(
                    title="沒有發現任何 PTT 免費遊戲文章", color=discord.Color.blue()
                )
                await channel.send(embed=embed)
            else:
                # 發送文章
                embed = discord.Embed(
                    title="📢 發現新的免費遊戲文章！",
                    color=discord.Color.green(),
                )
                for i in new_articles:
                    embed.add_field(
                        name=f"{i['title']} - {i['date']}",
                        value=f"[連結]({i['url']})",
                        inline=False,
                    )

                await channel.send(embed=embed)

            is_last_execute_time = self.is_last_execution_time()
            if is_last_execute_time:
                threshold_dt_utc = datetime.datetime.now(
                    datetime.timezone.utc
                ) - datetime.timedelta(days=2)

                print(f"截止時間 (threshold): {threshold_dt_utc.isoformat()}")
                print("-" * 20)

                current_articles = self.bot.storage.ptt_articles

                self.bot.storage.ptt_articles = {
                    article["url"]: article
                    for article in current_articles.values()
                    if article["queryAt"] >= threshold_dt_utc
                }
                print(f"清空文章暫存；目前數量 {len(self.bot.storage.ptt_articles)}")

            new_articles_dict = {article["url"]: article for article in new_articles}
            self.bot.storage.ptt_articles.update(new_articles_dict)
            print(f"更新暫存；目前數量 {len(self.bot.storage.ptt_articles)}")

        except Exception as e:
            # 錯誤處理區塊：捕捉並處理所有錯誤

            # 記錄詳細的錯誤堆棧
            error_info = traceback.format_exc()
            print(f"❌ 定時任務 check_task 執行失敗！錯誤類型: {e.__class__.__name__}")
            print(f"詳細錯誤堆棧：\n{error_info}")

            # 嘗試通知 Discord 頻道（確保在發生錯誤時發送，但這本身也可能失敗）
            try:
                channel = self.bot.get_channel(int(settings.CHANNEL_ID))
                # 嘗試發送到頻道，通知錯誤
                await channel.send(
                    f"🚨 **定時任務發生錯誤**：`{e.__class__.__name__}`。任務將在下次排程時間繼續嘗試。"
                )

                print(f"定時任務錯誤 `{e.__class__.__name__}`")
            except Exception as inner_error:
                # 避免錯誤處理程序本身又拋出錯誤導致 Task 停止
                print(f"發送 Discord 錯誤通知時再次發生錯誤。{inner_error}")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_task()

    @check_task.before_loop
    async def before_check_task(self):
        print("等待 bot 準備就緒...")
        await self.bot.wait_until_ready()
        print("Bot 準備完成，定時任務即將啟動。")


async def setup(bot: Bot):
    await bot.add_cog(Task(bot))
