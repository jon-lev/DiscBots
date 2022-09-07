//Simple bot to play with APIs
//Playing with Steam API to determine what game our friend 'Gordo' was playing

const Discord = require('discord.js');
const cron = require('node-cron');
const client = new Discord.Client();
const SteamAPI = require('steamapi');
const steamapi = require('steamapi');
//removed API key for safety
const steam = new SteamAPI('------------------');
const data = ["", "", ""];

//Write to console once bot is online and running
client.once('ready', () =>
{
    console.log("GordoBOT online!");
})

//If the message doesn't start with the command prefix '$' then ignore the message
client.on('message', message =>
{
    if(!message.content.startsWith("$") || message.author.bot) return
});

//Main logic for checking with Steam API
client.on('message',message =>
{
    console.log(data[0]);
    //Get the bot channel to not spam general chat
    var botChan = client.channels.cache.get("745874445054509127");

    //If we run the '$check' command
    if(message.content == "$check")
    {
        //use steam API to getUserSummary of Gordo
        steam.getUserSummary('76561198008560141').then(summary => {
            //console.log(summary);
            //If we are given the game info
            if(summary.gameExtraInfo != undefined && summary.gameServerIP != undefined)
            {
                //Send in the bot channel the game Gordo is playing and what server he is playing on
                botChan.send("Gordo is playing " + summary.gameExtraInfo + " on " + summary.gameServerIP);  
            }
           else
           {
               //They are not playing on any servers
               botChan.send("Gordo is NOT playing any games!")
           }
            
        });
    }
})

// Keep at end
//removed api key for safety
client.login('----------------------');
