import os

import dotenv
from discord.ext import commands
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://free.v36.cm/v1/",
    default_headers={"x-foo": "true"},
)


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = 1301161921868730388

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.target_channel_id and not message.author.bot:
            print(message.content)
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages={"content": message.content, "role": "user"},
                    max_tokens=100,
                )
            except Exception as e:
                print(e)
                return
            print(response.choices[0].text)
            await message.channel.send(response.choices[0].message.content)


async def setup(bot):
    await bot.add_cog(Chat(bot))
