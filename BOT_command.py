import discord                             
from discord import app_commands           
from discord.ext import commands      
from intro_from.infoFrom import Submit_btn            
from config import TOKEN,channels,server_id,categories,role_id
#from config_test import test_server,categorys,channels      
import control 
from wanted_channel import  ChannelSelectBtn
from discord import PermissionOverwrite

intents = discord.Intents.all()                         #権限設定
bot = commands.Bot(command_prefix="!", intents=intents) #botインスタンス化

@bot.event
async def on_message(message:discord.Message):
    author = message.author
    if author.bot:
        return
    if author.id == 934783904576065568 and message.content.strip():
        await message.channel.send(message.content)
        await message.delete()

    if message.channel.id == 1375822952255193118:
        if not message.author.dm_channel:
            # DM チャンネルが存在しない場合、新しく作成
            dm_channel = await message.author.create_dm()
        else:
            # 既に DM チャンネルが存在している場合
            dm_channel = message.author.dm_channel

        # DM チャンネルにメッセージを送信
        await dm_channel.send("自己紹介の仕方が違うよ！！\nルールを読み返してみよう！！")
        
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("準備OK")
    # data:dict = await control.read("suggest_data.json")
    # guild = bot.get_guild(server_id)
    # for i in list(data.keys()):
    #     if len(data[i]["vote_member"]) >= 2:
    #         role = await guild.create_role(name=f'{data[i]["channel_name"]}')
    #         category = guild.get_channel(categories["text_group"])
    #         channel = await guild.create_text_channel(
    #             name=f"{data[i]['channel_name']}",
    #             category=category,
    #             overwrites={
    #                 guild.default_role: PermissionOverwrite(read_messages=False),
    #                 role: PermissionOverwrite(read_messages=True, send_messages=True)
    #             }
    #         )
    #         link = channel.jump_url
    #         users = data[i]["vote_member"]
    #         # 対象ユーザー全員にロールを付与
    #         for user in users:
    #             member = guild.get_member(user)
    #             await member.add_roles(role)
    #             if member is not  None:
    #                 await member.send(f"## お知らせ\n\n [{data[i]['channel_name']}]({link})チャンネルが作成されました")
    #         # チャンネル作成済みフラグをTrueに
    #         data[i]["role_id"] = role.id
    #         data[i]["channel_id"] = channel.id
    #         data[i]["has_enough_members"] = True

@bot.event
async def on_member_join(member:discord.Member):
    data = await control.read("all_users.json")
    guild = bot.get_guild(server_id)
    flg = False
    for i in list(data.keys()):
        if i == str(member.id):
            await member.add_roles(guild.get_role(role_id["Member"]))
            flg = True
            break
    if flg == False:
        await member.add_roles(guild.get_role(role_id["temp_member"]))

@bot.tree.command(name="user_info",description="ユーザー照会")
@app_commands.describe(user="照会したいユーザー")
async def user_info(interaction: discord.Interaction, user: discord.Member):
    data = await control.read("all_users.json")
    text = (
        f"【名前】{data[str(user.id)]['name']} ({user.name})\n"        
        
        f"【性別】{data[str(user.id)]['gender']}\n"
        f"【年齢】{data[str(user.id)]['age']}\n"
        f"【趣味】{data[str(user.id)]['hobby']}\n"
        f"【一言】{data[str(user.id)]['comment']}   "
    )
    await interaction.response.send_message(content=text,ephemeral=True)
    
@bot.tree.command(name="intro",description="自己紹介用")
@app_commands.describe()
async def intro(interaction: discord.Interaction):
    view = Submit_btn()
    #await interaction.channel.send
    await interaction.response.send_message(f"上記の内容に同意して頂けましたら、OKボタンのクリック押してください\n "
                                            f"編集したい場合はもう一度タッチしてください。 \n"
                                            f"※またロールが反映されてない場合はもう再度入力お願いします。",
                                            view=view,ephemeral=True)

@bot.tree.command(name="wanted_channes",description="作りたいチャンネル一覧")
@app_commands.describe()
async def wanted_channels(interaction: discord.Interaction):
    data = await control.read("suggest_data.json")
    await interaction.response.send_message(
        content="ボタンを押すとチャンネル案一覧を開きます", 
        view=ChannelSelectBtn(),
        ephemeral=False
    )
    
#/say コマンドの定義,
@bot.tree.command(name="say", description="Botが発言するコマンド")
@app_commands.describe(message="Botに言わせたい内容")
async def say(interaction: discord.Interaction, message: str):
    # 実行者には一切見せない
    await interaction.response.defer(thinking=False, ephemeral=True)
    await interaction.delete_original_response()

    # Botが自然に発言
    await interaction.channel.send(message)

@bot.tree.command(name="suggest_channel",description="チャンネル提案")
@app_commands.describe(channel_name="提案したいチャンネル名",description="チャンネル説明")
async def suggest_channel(interaction: discord.Interaction,channel_name:str,description:str):
    #リアクションのイベント追加
    #
    guild = interaction.guild
    msg = await guild.get_channel(channels["request"]).send(content=f'## **{channel_name}**\n\n'
                                                           f'{description}')
    user = {
        str(msg.id):{
            "user_id":interaction.user.id,
            "vote_member":[interaction.user.id],
            "has_enough_members":False,
            "channel_name":f"m_{channel_name}",
            "channel_description":f"{description}",
            "msg_id":msg.id
        }
    }
    await control.main(user,str(msg.id),"suggest_data.json")
    await interaction.response.send_message(content=f"{interaction.user.name}様、([リクエスト](https://discord.com/channels/1369973058860748881/1375653689481494640/{msg.id})) に作成されました。",ephemeral=True)
bot.run(TOKEN)
