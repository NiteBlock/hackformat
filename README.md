# hackformat
This is a multifunctional dicsord bot that was made for hackweek!

**How to run the bot**

1. download [python](https://python.org) and [git](https://git.com)

2. Install discord.py. `pip install discord.py` or for the tested and built version `pip install discord.py==1.2.1`

3. Clone the git `git clone https://github.com/Niteblock/hackformat.git`

4. Go to the folder `cd level-system-drew`

5. Configure the files in the config.json file like this

**Config.txt**

```json
{
"defaultprefix" : "+"
"token" : "INSERT BOT TOKEN",
}
```



6. Run the bot `[sudo] python bot.py`
*sudo must be used if you dont have permissions to write files*

**DO NOT REUSE**


**How it works**
basicly our bot.py file goes though each file in the cogs folders and adds them to the bot itself so that they can be used. The way we create embeds? its simple our cogs files `from utils.embed import ce` which allows us to use ce to make embeds faster! Now im sure you have many other questions! simply contact Nite#0001 on discord!
