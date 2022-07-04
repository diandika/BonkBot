import nextcord
import requests
from setuptools import Command
import unidecode
import unicodedata
import json
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from nextcord.ext import commands

class detect_posts(commands.Cog, name="detect posts"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def normalize(self, s):
        new_s = unicodedata.normalize("NFKD", s.lower())
        #new_s = unidecode.unidecode(new_s)
        new_s = new_s.replace("1", "l")
        new_s = new_s.replace("4", "a")
        new_s = new_s.replace("3", "e")
        new_s = new_s.replace("0", "o")

        return new_s

    def get_page_sources(self, url):
        # driver = webdriver.Firefox()
        # driver.get(url)
        # time.sleep(2)
        # Keys.END
        # time.sleep(2)
        page = requests.get(url)
        return BeautifulSoup(page.text, "html.parser")

    def get_violating_post(self, post_list):
        with open("./cogs/blackwordlist.json", 'r', encoding='utf-8-sig') as file:
            word_list = json.load(file)["word_list"]
        
        violating_post = []
        for post in post_list:
            if any(word in post["title"] for word in word_list) or any(word in post["desc"] for word in word_list) :
                violating_post.append(post)
        
        return violating_post

    @commands.command()
    async def detect(self, ctx):
        post_info_list = []
        posts_list = []

        while (len(posts_list) == 0):
            page_source = self.get_page_sources('https://notes.qoo-app.com/en')
            
            posts_list = page_source.findAll("div", class_="qoo-note-view")
        
        for post in posts_list:
            post_info = {"user": "", "link": "", "title": "", "desc": ""}

            post_info["user"] = post.findAll("a", class_="artist")[0]["href"]
            post_info["link"] = post["data-href"]
            title = post.findAll("strong", class_="content-title")
            if len(title) > 0 :
                post_info["title"] = self.normalize(title[0].text)
            desc = post.findAll("cite", class_="description")
            if len(desc) > 0 :
                post_info["desc"] = self.normalize(desc[0].get_text(strip=True))

            post_info_list.append(post_info)
           
        violating_post = self.get_violating_post(post_info_list)
        
        reply = "Found " + str(len(violating_post)) + "/" + str(len(post_info_list)) + " violating posts" + "\n"
        for post in violating_post:
            reply = reply + post["link"] + '\n'
        
        if reply == "":
            reply = "No violators detected."
        reply = reply + '\n'
        #print(reply)
        
        await ctx.reply(reply)

    @commands.command()
    async def card(self, ctx, arg1 = ""):

        if arg1 != "":
            post_info_list = []
            posts_list = []

            while (len(posts_list) == 0):
                page_source = self.get_page_sources('https://apps.qoo-app.com/en/app-card/' + str(arg1))
                
                posts_list = page_source.findAll("div", class_="qoo-post-item")
                
            for post in posts_list:
                post_info = {"user": "", "link": "", "char_name": "", "guild_name": "", "desc": ""}
            
                post_info["user"] = post.select('a.icon.qoo-egg-view')[0]["href"]
                post_info["link"] = 'https://user.qoo-app.com/en/card/' + post["data-id"]
                td = post.findAll('td')
                if len(td)>0 :
                    post_info["char_name"] = self.normalize(td[1].get_text(strip=True))
                if len(td)>2 :
                    post_info["guild_name"] = self.normalize(td[3].get_text(strip=True))

                desc = post.findAll('p')
                if len(desc) > 1:
                    post_info["desc"] = self.normalize(desc[1].get_text(strip=True))

                post_info_list.append(post_info)
            
            with open("./cogs/blackwordlist.json", 'r', encoding='utf-8-sig') as file:
                word_list = json.load(file)["word_list"]
            
            violating_post = []
            for post in post_info_list:
                if any(word in post["char_name"] for word in word_list) or any(word in post["desc"] for word in word_list) or any(word in post["guild_name"] for word in word_list) :
                    violating_post.append(post)
            
            reply = "Found " + str(len(violating_post)) + "/" + str(len(post_info_list)) + " violating posts" + "\n"
            for post in violating_post:
                reply = reply + post["user"] + '\n'
                
            if reply != "":
                await ctx.send(reply)
            
        else:
            game_list = ["4847", "2519", "9038", "18337", "191", "11812", "7874", "10427", "19415"]
            for i in game_list:
                await self.card(ctx, i)

    @commands.command()
    async def notes(self, ctx, arg1 = ""):
        if arg1 != "":
            post_info_list = []
            posts_list = []

            while (len(posts_list) == 0):
                page_source = self.get_page_sources('https://apps.qoo-app.com/en/app-note/')
                print(page_source)
                posts_list = page_source.findAll("div", class_="qoo-note-view")
            
            for post in posts_list:
                post_info = {"user": "", "link": "", "title": "", "desc": ""}

                post_info["user"] = post.findAll("a", class_="artist")[0]["href"]
                post_info["link"] = post["data-href"]
                title = post.findAll("strong", class_="content-title")
                if len(title) > 0 :
                    post_info["title"] = self.normalize(title[0].text)
                desc = post.findAll("cite", class_="description")
                if len(desc) > 0 :
                    post_info["desc"] = self.normalize(desc[0].get_text(strip=True))

                post_info_list.append(post_info)
                
            with open("./cogs/blackwordlist.json", 'r', encoding='utf-8-sig') as file:
                word_list = json.load(file)["word_list"]
            
            violating_post = []
            for post in post_info_list:
                if any(word in post["char_name"] for word in word_list) or any(word in post["desc"] for word in word_list) or any(word in post["guild_name"] for word in word_list) :
                    violating_post.append(post)
            
            reply = "Found " + str(len(violating_post)) + "/" + str(len(post_info_list)) + " violating posts" + "\n"
            for post in violating_post:
                reply = reply + post["user"] + '\n'
                
            if reply != "":
                await ctx.send(reply)
            
        else:
            game_list = ["4847", "2519", "191", "11812", "7874", "10427", "19415"]
            for i in game_list:
                await self.notes(ctx, i)

def setup(bot: commands.Bot):
    bot.add_cog(detect_posts(bot))
