const { SlashCommandBuilder } = require('@discordjs/builders');
const axios = require("axios");
const cheerio = require("cheerio");
const pretty = require("pretty");
const fs = require("fs");

const { list } = require("./blackwordlist.json");

async function scrape(){
	url = "https://notes.qoo-app.com/en";
	text = "";
	try{
		const {data} = await axios.get(url);

		const $ = cheerio.load(data);
		const listItems = $(".qoo-note-wrap");

		const violating_posts = [];
		const safe_posts = [];
		console.log(listItems.length);
		listItems.each((idx, el) => {

			const post = {title: "", content: ""};

			title = $(el).find('.qoo-note-view > .content-title').text().toLowerCase().trim();
			title = title.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
			title = title.replace(/3/g, 'e');
			title = title.replace(/4/g, 'a');
			content = $(el).find('.qoo-note-view > .description').text().toLowerCase().trim();
			content = content.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
			content = content.replace(/3/g, 'e');
			content = content.replace(/4/g, 'a');

			post.title = title;
			post.content = content;

			violating = false;
			for (let word of list){
				if (content.includes(word) || title.includes(word)){
					//post.userId = $(el).attr('data-user-id');
					text = text.concat("uid: ", post.userId, `\n`);
					//post.postLink = $(el).children('.link-wrap').attr('href');
					text = text.concat("link: ", post.postLink, `\n\n`);
					//text = text.concat("content: ", post.content, `\n\n`);
					violating = true;

					break;
				}
			}

			if (violating) {
				violating_posts.push(post);
			}else{
				safe_posts.push(post);
			}
		});

		//console.dir(posts);

		fs.writeFile("violating_posts.json", JSON.stringify(violating_posts, null, 2), (err) => {
			if (err){
				console.error(err);
				return;
			}
			console.log("successfully wrote file");
		});

		fs.writeFile("safe_posts.json", JSON.stringify(safe_posts, null, 2), (err) => {
			if (err){
				console.error(err);
				return;
			}
			console.log("successfully wrote file");
		});
		return text;
	} catch (err) {
		console.error(err);
	}
}

module.exports = {
	data: new SlashCommandBuilder()
		.setName('detect')
		.setDescription('Detecting recent violators'),
	async execute(interaction) {
		reply = await scrape();
		console.log(reply);
		if (reply === ""){
			reply = "No violators detected yet.";
		}
		await interaction.reply(reply);
	},
};