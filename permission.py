# PermissionOverwriteで権限を明示的に設定
import discord


overwrite = discord.PermissionOverwrite()
# チャンネルの招待作成権限を拒否
overwrite.create_instant_invite = False  

# メンバーをキックする権限を拒否
overwrite.kick_members = False               

# メンバーをバンする権限を拒否
overwrite.ban_members = False                

# 管理者権限を拒否（すべての権限を持つことを許可しない）
overwrite.administrator = False              

# チャンネルの管理権限を拒否（チャンネルを作成・削除・変更できない）
overwrite.manage_channels = False            

# サーバー設定の管理権限を拒否（サーバー設定の変更を許可しない）
overwrite.manage_guild = False              

# メッセージにリアクションを追加する権限を拒否
overwrite.add_reactions = False             

# 監査ログを閲覧する権限を拒否
overwrite.view_audit_log = False            

# ボイスチャンネルで優先発言をする権限を拒否
overwrite.priority_speaker = False          

# ストリーミングを開始する権限を拒否
overwrite.stream = False                    

# メッセージを読む権限を拒否
overwrite.read_messages = False             

# チャンネルを閲覧する権限を拒否
overwrite.view_channel = False              

# メッセージを送信する権限を拒否
overwrite.send_messages = False             

# TTS（テキスト読み上げメッセージ）の送信を拒否
overwrite.send_tts_messages = False         

# メッセージを管理する権限（削除、編集など）を拒否
overwrite.manage_messages = False            

# 埋め込みリンクを送信する権限を拒否
overwrite.embed_links = False               

# ファイルを添付する権限を拒否
overwrite.attach_files = False              

# メッセージ履歴を閲覧する権限を拒否
overwrite.read_message_history = False       

# @everyone を使ったメンションを許可しない
overwrite.mention_everyone = False          

# 外部絵文字を使用する権限を拒否
overwrite.external_emojis = False            

# 外部絵文字を使用する権限を拒否（絵文字の管理を許可しない）
overwrite.use_external_emojis = False        

# サーバーのインサイトを閲覧する権限を拒否
overwrite.view_guild_insights = False        

# ボイスチャンネルに接続する権限を拒否
overwrite.connect = False                    

# ボイスチャンネルで話す権限を拒否
overwrite.speak = False                      

# ボイスチャンネル内でメンバーをミュートにする権限を拒否
overwrite.mute_members = False              

# ボイスチャンネル内でメンバーを聴覚遮断する権限を拒否
overwrite.deafen_members = False             

# ボイスチャンネル内でメンバーを移動する権限を拒否
overwrite.move_members = False              

# 音声活動（VAD）を使用する権限を拒否
overwrite.use_voice_activation = False       

# 自分のニックネームを変更する権限を拒否
overwrite.change_nickname = False            

# 他のユーザーのニックネームを変更する権限を拒否
overwrite.manage_nicknames = False          

# ロールの管理権限を拒否（ロールの作成・削除・変更ができない）
overwrite.manage_roles = False              

# チャンネルやロールの権限を管理する権限を拒否
overwrite.manage_permissions = False         

# Webhookの管理権限を拒否（Webhookを作成・削除できない）
overwrite.manage_webhooks = False            

# 絵文字やスタンプの管理権限を拒否
overwrite.manage_expressions = False         

# 絵文字の管理権限を拒否（カスタム絵文字を作成・削除できない）
overwrite.manage_emojis = False             

# 絵文字やスタンプの管理権限を拒否（絵文字とスタンプ両方）
overwrite.manage_emojis_and_stickers = False

# アプリケーションコマンドを使用する権限を拒否
overwrite.use_application_commands = False   

# スピーカーとして話すリクエストをする権限を拒否
overwrite.request_to_speak = False          

# イベントの管理権限を拒否（イベントの作成・管理など）
overwrite.manage_events = False             

# スレッドを管理する権限を拒否（スレッド作成・管理など）
overwrite.manage_threads = False            

# 公開スレッドの作成権限を拒否
overwrite.create_public_threads = False      

# 非公開スレッドの作成権限を拒否
overwrite.create_private_threads = False     

# スレッド内でメッセージを送信する権限を拒否
overwrite.send_messages_in_threads = False   

# 外部ステッカーを使用する権限を拒否
overwrite.external_stickers = False         

# 外部ステッカーを使用する権限を拒否
overwrite.use_external_stickers = False      

# 埋め込まれたアクティビティを使用する権限を拒否
overwrite.use_embedded_activities = False    

# メンバーをモデレートする権限を拒否（不正行為の防止）
overwrite.moderate_members = False          

# サウンドボードを使用する権限を拒否
overwrite.use_soundboard = False            

# 外部サウンドを使用する権限を拒否
overwrite.use_external_sounds = False        

# 音声メッセージの送信を拒否
overwrite.send_voice_messages = False        

# エクスプレッション（表情）の作成権限を拒否
overwrite.create_expressions = False         

# イベントを作成する権限を拒否
overwrite.create_events = False             

# ポールを送信する権限を拒否
overwrite.send_polls = False                 

# ポールを作成する権限を拒否
overwrite.create_polls = False              

# 外部アプリケーションの使用を拒否
overwrite.use_external_apps = False          


