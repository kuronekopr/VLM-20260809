# VAIO ノートパソコン製品詳細カタログ用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に VAIO ノートパソコンの見開き製品詳細カタログ画像（例: P.03-04 SX14-R詳細ページ）をアップロードし、以下のプロンプトをコピペして実行することで、**USP・便利機能 (recommended_features)・本文機能説明付きの構造化JSON (product_series_details_pc_vaio_sx14r.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **VAIO カタログの製品詳細画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい VAIO ノートパソコンの見開き製品詳細カタログ画像（P.03-04）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`product_series_details_pc_vaio_sx14r.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (VAIO 製品詳細用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された VAIO ノートパソコンの製品詳細カタログ画像から、以下の抽出ルールとJSONフォーマットに従って詳細構造化JSONを出力してください。

【抽出ルール】
1. 基本識別子 (manufacturer / product_category / brand_name / model_number / series_name):
   - manufacturer: "VAIO"
   - product_category: "ノートパソコン"
   - brand_name: "VAIO"
   - model_number: 型番 (例: "VAIO SX14-R")
   - series_category: 分類見出し (例: "ハイエンド軽量大画面モバイル")
2. Unique Selling Point (unique_selling_point):
   - 型番下のキャッチコピー文章テキスト（例: "毎日持ち選べる軽さと充実のパフォーマンス、すべてにおいて妥協したくない人へ。"）
3. 便利機能アイコン群 (recommended_features):
   - 添付1相当: 「主な機能」ヘッダー下に並ぶアイコン・ピクトグラム（例: ["VAIO TruePerformance", "VAIO User Sensing", "AIノイズキャンセリング", "指紋認証", "顔認証", "Wi-Fi 7", "ビデオチャット", "品質試験", "日本製"]）
4. 分類キャッチコピー (category_description):
   - 添付2相当: グレー帯枠囲み内の分類テキスト（例: "ハイエンド軽量大画面モバイル 14.0型ワイド"）
5. Unique Selling Point 見出し集 (unique_selling_point):
   - 添付3相当: カタログ内の水色テキストで書かれた主要なアピール見出し文章の一覧リスト（例: ["最大約14.5時間駆動の驚異的スタミナ", "AI新時代の高性能CPUを搭載", "天板と底面にカーボンを採用しより軽く、強く、美しく", "VAIOならではのスマート機能がもっと便利に、使いやすく", "高精細で見やすい大画面", "いろいろ繋がる豊富なインターフェース"]）
6. ハードウェアスペック (display_spec / processor / storage / weight_g / battery_life / toughness / interfaces):
   - ディスプレイサイズ・アスペクト比
   - CPUプロセッサー名およびNPU性能
   - ストレージ規格 (PCIe 5.0対応 SSDなど)
   - 本体重量 (g) および 駆動時間 (動画再生/アイドル 時間)
   - 耐久性規格 (MIL-STD-810Hなど)
   - インターフェース端子一覧
5. 製品説明セクション本文 (product_description_features):
   - カタログ右ページの各見出し番号（01, 02, 03）ごとに記載されている特徴文言をリスト化して抽出してください。

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "manufacturer": "VAIO",
    "product_category": "ノートパソコン",
    "brand_name": "VAIO",
    "model_number": "VAIO SX14-R",
    "series_name": "SX14-R",
    "series_category": "ハイエンド軽量大画面モバイル",
    "unique_selling_point": "毎日持ち選べる軽さと充実のパフォーマンス、すべてにおいて妥協したくない人へ。",
    "recommended_features": [
      "VAIO User Sensing",
      "AI ノイズキャンセリング",
      "Copilot+PC",
      "指紋認証",
      "顔認証",
      "Wi-Fi 7",
      "ビデオチャット",
      "品質試験",
      "JAPAN 日本製"
    ],
    "display_spec": {
      "size": "14.0型ワイド",
      "aspect_ratio": "16:10"
    },
    "processor": {
      "name": "インテル® Core™ Ultra 5 シリーズ 3 プロセッサー",
      "npu_performance": "最大47TOPS"
    },
    "storage": "第五世代ハイスピードSSD (PCIe 5.0対応 NVMe SSD)",
    "weight_g": 967,
    "battery_life": {
      "video_playback_hours": 15.0,
      "idle_hours": 27.0
    },
    "toughness": "アメリカ国防総省制定MIL規格準拠 (MIL-STD-810H)",
    "interfaces": ["USB Type-C", "USB Type-A", "HDMI", "有線LAN", "ヘッドホン端子"],
    "color_variations": ["ディープエメラルド", "ファインブラック"],
    "product_description_features": {
      "01_パワー_スリムボディ": [
        "AI新時代の高性能CPUを搭載 (インテル Core Ultra 5 シリーズ3 NPU47TOPS)",
        "天板と底面にカーボンを採用し、軽く、強く、美しく (約967g, MIL-STD 810H準拠)",
        "第五世代ハイスピードSSD搭載 (PCIe 5.0対応)",
        "モバイル利用に応える長時間駆動 (動画再生約15.0時間/アイドル約27.0時間)",
        "14.0型ワイドディスプレイの見やすい大画面と、静かで快適に使えるキーボード (アスペクト比16:10)"
      ],
      "02_Copilot_Plus_PC": [
        "Copilot+ PC対応でAI活用がもっと便利に (コクリエーター, リコールプレビュー)"
      ],
      "03_利便性_インターフェース": [
        "VAIOならではのスマート機能がもっと便利に、使いやすく (AIノイズキャンセリング, VAIO User Sensing)",
        "いろいろ繋がる、豊富なインターフェース (USB Type-C, USB Type-A, HDMI, 有線LAN, ヘッドホン端子)"
      ]
    }
  }
]
```
```


---

## 追加取り込みカタログ画像・マージ履歴 ＆ 特殊レイアウト抽出定義
- 本プロンプトは既存のルール・フォーマット制約を保持したまま、以下の追加画像取り込みにスマートマージ更新されました。
- 画像: スクリーンショット 2026-08-11 100907.png

### 視覚要素・レイアウトパース定義
1. **おもなおすすめ機能 (`recommended_features`)**:
   - 「主な機能」ヘッダーの下に並ぶピクトグラム/アイコン（例: `VAIO TruePerformance`, `VAIO User Sensing`, `AIノイズキャンセリング`, `指紋認証`, `顔認証`, `Wi-Fi 7`, `ビデオチャット`, `品質試験`, `日本製` など）テキストラベルを配列として認識・抽出すること。
2. **分類キャッチコピー (`category_description`)**:
   - 画面上部または帯内の枠囲み強調テキスト（例: `ハイエンド軽量大画面モバイル 14.0型ワイド` など）を抽出すること。
3. **ユニークセリングポイント (USP: `unique_selling_point`)**:
   - カタログ本文内の水色テキストの見出し文章（例: `最大約14.5時間駆動の驚異的スタミナ`, `AI新時代の高性能CPUを搭載`, `天板と底面にカーボンを採用しより軽く、強く、美しく`, `VAIOならではのスマート機能がもっと便利に、使いやすく`, `高精細で見やすい大画面`, `いろいろ繋がる豊富なインターフェース` など）を配列として認識・抽出すること。

