import json
import asyncio
from discord import ChannelType,Client as DiscordClient

class Client(DiscordClient):
	def __init__(self,config,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.config=config
	async def on_ready(self):
		with open(config['outputFilename'],'w+',encoding='utf-8') as f:
			json.dump({
					c.id:{
						m.id:{
							'timestamp' : int(m.created_at.timestamp()*1000),
							'author'    : str(m.author.id),
							'content'   : m.content
						} for m in await c.history(limit=1000).flatten() if not m.author.bot
					} for c in self.guilds[0].channels if c.type==ChannelType.text
				},f,indent=4,ensure_ascii=False
			)
		await self.logout()

with open('config.json','r') as f:
	config=json.load(f)
client=Client(config)
client.run(config['clientToken'])
