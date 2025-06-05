# Discord Community Utility Bot

## 📌 概要

このDiscord Botは、**自己紹介フォームの提出・編集**や、**チャンネル提案・投票機能**を通じて、コミュニティの活性化と管理の効率化をサポートします。ユーザー情報の管理、ロール自動付与、希望チャンネルの投票に基づく自動生成を提供します。

---

## ⚙️ 機能一覧

| コマンド              | 機能概要 |
|-----------------------|----------|
| `/intro`              | 自己紹介フォームの送信・編集 |
| `/user_info @user`    | 指定ユーザーのプロフィール確認 |
| `/suggest_channel`    | 新しいチャンネルを提案 |
| `/wanted_channes`     | 提案されたチャンネルに投票・自動作成 |
| `/say`                | Botが指定メッセージを発言 |

---

## 🗂 ディレクトリ構成

```plaintext
C:.
│  all_users.json              # ユーザー情報を保存するJSON
│  BOT_command.py              # Bot本体
│  config.py                   # 本番用設定ファイル（TOKENやID）
│  config_test.py              # テスト用設定ファイル（任意）
│  control.py                  # JSONファイルの読み書きユーティリティ
│  permission.py               # パーミッション設定
│  start.bat                   # 起動バッチファイル
│  suggest_control.py          # 提案チャンネル関連制御（オプション）
│  suggest_data.json           # チャンネル提案データ
│  wanted_channel.py           # 提案チャンネルの投票処理など
│
└─intro_from
      edit_UI.py              # 自己紹介の編集UI
      infoFrom.py             # 自己紹介の初回登録UI
      modal_required.py       # フォーム入力の定義
