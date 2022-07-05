import os
import nextcord
import requests
import unidecode
import unicodedata
import json
import numpy as np
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from nextcord.ext import commands


def main():
	client = commands.Bot(command_prefix = "#")

	load_dotenv()

	@client.event
	async def on_ready():
		print(f"{client.user.name} has connexted to Discord.")

	for file in os.listdir('./cogs'):
		if file.endswith('.py'):
			client.load_extension(f"cogs.{file[:-3]}")

	client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
	main()