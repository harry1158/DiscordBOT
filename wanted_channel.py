import discord
from discord import PermissionOverwrite
import control
from config import *
from permission import overwrite

class ChannelSelect(discord.ui.Select):
    def __init__(self, channel_list:dict):
        self.channel_list = channel_list
        options = []
        for msg_id  in list(channel_list.keys()):
            option = discord.SelectOption(
                label=channel_list[msg_id]["channel_name"][:25],
                description=f"{channel_list[msg_id]['channel_description'][:50]}",
                value=msg_id
            )
            options.append(option)
        super().__init__(
            placeholder="チャンネルを選択してください",
            options=options
        )
        self.channel_list = channel_list
    
    async def callback(self, interaction:discord.Interaction):
        msg_id = self.values[0]
        ch = self.channel_list[msg_id]
        await interaction.response.send_message(content=f"## **{ch['channel_name']}**\n\n**{ch['channel_description']}**\n-# 現在賛同してるメンバーは{len(self.channel_list[msg_id]['vote_member'])}人です",
                                                ephemeral=True,
                                                view=ChannelSubmitBtn(msg_id))

class ChannelSubmitBtn(discord.ui.View):
    def __init__(self,msg_id:str):
        super().__init__(timeout=None)
        self.msg_id = msg_id
        
    @discord.ui.button(label="投票する",style=discord.ButtonStyle.green) 
    async def submit_selected(self,interaction:discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_message(content="投票しました。\n(既定の人数を超えてる場合自動的にチャンネルが追加されます。)",ephemeral=True)
        data              = await control.read("suggest_data.json")
        user_id           = (interaction.user.id)
        vote_members:list = data[self.msg_id]["vote_member"]
        vote_members.append(user_id)
        vote_members                     = list(set(vote_members))
        data[self.msg_id]["vote_member"] = list(set(vote_members))
        print(len(vote_members))
        guild = interaction.guild
        read_role = guild.get_role(role_id["read"])
        if len(vote_members) >= 3:
            if data[self.msg_id]["has_enough_members"] == False:
                # 新ロール作成
                role = await guild.create_role(name=f"{data[self.msg_id]['channel_name']}")
                # カテゴリー取得
                category = guild.get_channel(categories["text_group"])
                # 新チャンネル作成（権限設定付き）
                channel = await guild.create_text_channel(
                    name=f"{data[self.msg_id]['channel_name']}",
                    category=category,
                    overwrites={
                        guild.default_role: PermissionOverwrite(read_messages=False),
                        role: PermissionOverwrite(read_messages=True, send_messages=True)
                    }  
                )
                overwrite.read_message_history = True
                overwrite.view_channel = True
                for channel in category.channels:
                    await channel.set_permissions(read_role, overwrite=overwrite)
            else:
                role = guild.get_role(data[self.msg_id]["role_id"])
            link = channel.jump_url
            users = set(vote_members)
            # 対象ユーザー全員にロールを付与
            for user in users:
                member = guild.get_member(user)
                await member.add_roles(role)
                if member is not  None and data[self.msg_id]["has_enough_members"] == False:
                    await member.send(f"## お知らせ\n\n [{data[self.msg_id]['channel_name']}]({link})チャンネルが作成されました")
            # チャンネル作成済みフラグをTrueに
            data[self.msg_id]["has_enough_members"] = True
            data[self.msg_id]["role_id"] = role.id
            data[self.msg_id]["channel_id"] = channel.id
        
        # 変更をファイルに保存
        await control.main(data, self.msg_id, "suggest_data.json")
#----------------------------------------------------------------------    

class ChannelSelectBtn(discord.ui.View): #ボタンの機能 セレクトメニューをメッセージで表示
    def __init__(self):
        super().__init__(timeout=None)
        

    @discord.ui.button(label="チャンネル一覧を見る", style=discord.ButtonStyle.green)
    async def show_select(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_list = await control.read("suggest_data.json")
        await interaction.response.send_message(
            content="チャンネル案から選択してください",
            view=ChannelSelectView(channel_list),
            ephemeral=True
        )

class ChannelSelectView(discord.ui.View): #ボタンの表示
    def __init__(self, channel_list):
        super().__init__(timeout=None)
        self.add_item(ChannelSelect(channel_list))