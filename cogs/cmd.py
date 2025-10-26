import sys

from discord.ext import commands

from utils.bot import Bot


class Cmd(commands.Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        print("cmd init")

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")

    # 確保只有 Bot 的擁有者可以執行此指令 (推薦)
    # @commands.is_owner()
    @commands.command(name="shutdown", help="安全地關閉機器人")
    async def shutdown_command(self, ctx: commands.Context):
        await ctx.send("🤖 **正在執行安全關閉...**")
        await self.bot.close()
        sys.exit(0)

    @shutdown_command.error
    async def shutdown_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("🚫 錯誤：只有機器人的擁有者可以執行此指令。")
        else:
            await ctx.send(f"關閉時發生錯誤: {error}")


# cog 需要有 setup 函式才能載入
async def setup(bot: Bot):
    await bot.add_cog(Cmd(bot))
