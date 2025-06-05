import discord
import control
#from config_test import channels,role_ids
from config import *
from intro_from.edit_UI import Edit_btn

class InfoForm(discord.ui.Modal, title="自己紹介フォーム"):

    name             = discord.ui.TextInput(label="名前 (ニックネーム)",required=True)
    age              = discord.ui.TextInput(label="年齢",required=True)
    gender           = discord.ui.TextInput(label="性別",required=False)
    hobby            = discord.ui.TextInput(label="趣味",required=False)
    comment          = discord.ui.TextInput(label="一言",required=False)
    userInfo_Channel = channels["self_intro"]
    
    async def on_submit(self, interaction: discord.Interaction):
        text = (
            f"【名前】{self.name.value}\n"
            f"【年齢】{self.age.value}\n"
            f"【性別】{self.gender.value}\n"
            f"【趣味】{self.hobby.value}\n"
            f"【一言】{self.comment.value}"
        )
        user = {
            str(interaction.user.id):{
                "name"   : self.name.value,
                "age"    : self.age.value,
                "gender" : self.gender.value,
                "hobby"  : self.hobby.value,
                "comment": self.comment.value,
                "msg_id" : ""
            }
        }
        try:
            guild = interaction.guild
            role  = guild.get_role(role_id["Member"])
            read_role = guild.get_role(role_id["read"])
            temp_role = guild.get_role(role_id['temp_member'])
            await interaction.user.remove_roles(read_role)
            await interaction.user.remove_roles(temp_role)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(text,ephemeral=True)
            
            text   = await self.self_induction(interaction=interaction)
            msg    = await guild.get_channel(self.userInfo_Channel).send(text)
            msg_id = msg.id
            user[str(interaction.user.id)]["msg_id"] = msg_id
            await control.main(user,str(interaction.user.id),"all_users.json")
        except Exception as e:
            await interaction.response.send_message('大変申し訳ございません。エラーが発生してしまった為、再度お試しください。若しくは管理人に異議申し立てを行って下さい')
            await guild.get_channel(channels["admin"]).send(f'{e}')
    async def self_induction(self,interaction: discord.Interaction):
        text = (
            f"{interaction.user.mention}\n"
            f"【名前】{self.name.value} \n"
            f"【年齢】{self.age.value}\n"
            f"【趣味】{self.hobby.value}\n"
            f"【一言】{self.comment.value}\n"
            f"【性別】{self.gender.value}" 
        )
        return text
    

class Submit_btn(discord.ui.View):
    @discord.ui.button(label="OK", style=discord.ButtonStyle.green, custom_id="btn1")
    
    async def button_one(self, 
                         interaction: discord.Interaction,
                         button     : discord.ui.Button) : 
        
        data = await control.read("all_users.json")
        if str(interaction.user.id) in data:
            data = await control.read("all_users.json")
            await interaction.response.send_message(content="編集モード",view=Edit_btn(interaction,data),ephemeral=True)
        else:
            await interaction.response.send_modal(InfoForm())           