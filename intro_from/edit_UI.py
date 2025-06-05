import discord
from intro_from.modal_required import required_flg, JAtoEN
import control
#from config_test import channels
from config import channels

# 編集項目を選択するためのセレクトメニュークラス
class EditSelect(discord.ui.Select):
    # セレクトメニューの初期化
    def __init__(self, integration: discord.Integration, data: dict[str, dict]):
        self.data = data
        user_id = str(integration.user.id)
        # ユーザーデータの各項目が空文字なら「未入力」としてセット
        for user in data[user_id]:
            if data[user_id][user] == "":
                data[user_id][user] = "未入力"
        # 選択肢リストを作成
        options = [
            discord.SelectOption(label="名前 (ニックネーム)", description=f"{data[user_id]['name']}"),
            discord.SelectOption(label="年齢", description=f"{data[user_id]['age']}"),
            discord.SelectOption(label="性別", description=f"{data[user_id]['gender']}"),
            discord.SelectOption(label="趣味", description=f"{data[user_id]['hobby']}"),
            discord.SelectOption(label="一言", description=f"{data[user_id]['comment']}"),
        ]
        # セレクトメニューの初期化
        super().__init__(
            placeholder="編集項目を選択してね。",
            min_values=1,
            max_values=1,
            options=options
        )

    # セレクトメニューで項目を選択したときの処理
    async def callback(self, interaction: discord.Interaction):
        # 選択された項目ごとにModal（編集フォーム）を表示
        await interaction.response.send_modal(
            SelectedItem(interaction=interaction, editLabel=self.values[0], data=self.data)  # self.values[0] は label
        )

# 編集内容を入力するModal（フォーム）クラス
class SelectedItem(discord.ui.Modal):
    # Modalの初期化
    def __init__(self, interaction: discord.Interaction, editLabel: str, data: dict, title="編集"):
        super().__init__(title=title)
        # テキスト入力欄（項目名ごとにラベルと必須指定を切替）
        self.editData = discord.ui.TextInput(label=editLabel, required=required_flg[editLabel])
        self.add_item(self.editData)
        self.data = data

    # Modalで送信されたときの処理
    async def on_submit(self, interaction: discord.Interaction):

        # 入力値が空の場合「未入力」とする
        SelectedValue = self.editData.value
        if SelectedValue == "":
            SelectedValue = "未入力"
        # 入力値をデータに反映
        self.data[str(interaction.user.id)][JAtoEN[self.editData.label]] = self.editData.value
        # 結果メッセージを表示
        await interaction.response.send_message(content=f"{self.editData.label}を{SelectedValue}に変更", ephemeral=True)

# 編集UIを表示するためのView（ボタン＋セレクト）のクラス
class Edit_btn(discord.ui.View):
    # Viewの初期化
    def __init__(self, integration: discord.Integration, data: dict):
        self.userid = str(integration.user.id)
        self.data = data

        super().__init__()
        # セレクトメニューをViewに追加
        self.add_item(EditSelect(integration, data))
        # 編集完了ボタンを作成してViewに追加
        complete_btn = discord.ui.Button(label="編集完了",
                                         style=discord.ButtonStyle.primary,
                                         custom_id="ok_btn")
        complete_btn.callback = self.complete_callback
        self.add_item(complete_btn)

    # 編集完了ボタンが押された時の処理
    async def complete_callback(self, interaction: discord.Interaction):
        # 完了時のユーザー情報まとめ
        text = (
            f"{interaction.user.mention}\n"
            f"【名前】{self.data[self.userid]['name']} \n"
            f"【年齢】{self.data[self.userid]['age']}\n"
            f"【趣味】{self.data[self.userid]['hobby']}\n"
            f"【一言】{self.data[self.userid]['comment']}\n"
            f"【性別】{self.data[self.userid]['gender']}"
        )
        # データ保存
        await control.main(user=self.data, user_id=str(interaction.user.id), filename="all_users.json")
        # サーバ上の紹介メッセージを編集
        guild = interaction.guild
        msg = await guild.get_channel(channels["self_intro"]).fetch_message(self.data[self.userid]["msg_id"])
        await msg.edit(content=await self.self_induction(interaction=interaction))
        # 完了メッセージ表示
        await interaction.response.send_message(f"編集を完了しました！\n\n{text}", ephemeral=True)

    # 自己紹介文を組み立てる関数
    async def self_induction(self, interaction: discord.Interaction):
        text = (
            f"{interaction.user.mention}\n"
            f"【名前】{self.data[self.userid]['name']} \n"
            f"【年齢】{self.data[self.userid]['age']}\n"
            f"【趣味】{self.data[self.userid]['hobby']}\n"
            f"【一言】{self.data[self.userid]['comment']}\n"
        )
        # 性別が非公開（末尾0）でなければ表示
        if self.data[self.userid]["gender"][-1] != "0":
            text += f"【性別】{self.data[self.userid]['gender']}"
        return text
