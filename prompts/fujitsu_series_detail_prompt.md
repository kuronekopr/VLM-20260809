# 富士通 (FMV) パソコン製品詳細カタログ用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に 富士通 FMV パソコンの上下2段製品詳細カタログ画像（P.07など）をアップロードし、以下のプロンプトをコピペして実行することで、**左側テキスト(USP) ＆ 右側スペック表 (recommended_features) 付き構造化JSON (product_series_details_fujitsu.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **富士通 FMV の製品詳細画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい FMV パソコンの製品詳細画像（P.07上下2段レイアウト）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`product_series_details_fujitsu.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (富士通 FMV 製品詳細用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された 富士通 FMV パソコンの製品詳細カタログ画像から、上下に並んでいる各製品モデル（上段 UA-K1, 下段 UX-K3 など）について、以下の抽出ルールとJSONフォーマットに従って構造化JSONを出力してください。

【抽出ルール】
1. 基本識別子 (manufacturer / brand_name / product_category / series_name / model_number / product_code):
   - manufacturer: "富士通"
   - brand_name: "FMV"
   - product_category: "ノートパソコン"
   - series_name: シリーズ名 (例: "FMV Note U")
   - model_number: 型番 (例: "UA-K1", "UX-K3")
   - product_code: 製品コード (例: "FMVUASK1BA", "FMVUX5K3BA")
   - layout_position: レイアウト位置 ("上段" または "下段")
2. ユニークセリングポイント (unique_selling_point):
   - 画像左側のキャッチコピー・特徴・数値テキスト文言（例: "ハイスペックCopilot+ PC (最大47TOPS / 動画再生約15.5時間・アイドル約36.0時間 / 約848g)", "世界最軽量モバイルノート 約634g"）
3. 主要推奨スペック表 (recommended_features):
   - 画像右側のスペック表から、OS, Office, 画面, CPU, NPU, メモリ, SSD, 無線, 駆動時間, 質量をキーバリューで抽出してください。

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "manufacturer": "富士通",
    "brand_name": "FMV",
    "product_category": "ノートパソコン",
    "series_name": "FMV Note U",
    "model_number": "UA-K1",
    "product_code": "FMVUASK1BA",
    "color_name": "ピクトブラック",
    "catalog_page": 7,
    "layout_position": "上段",
    "copilot_plus_pc": true,
    "unique_selling_point": "ハイスペックCopilot+ PC (最大47TOPS / 動画再生約15.5時間・アイドル約36.0時間 / 約848g)",
    "recommended_features": {
      "os": "Windows 11 Home",
      "office": "Microsoft 365 Basic + Office Home & Business 2024",
      "display": "14.0型ワイド WUXGA",
      "cpu": "インテル® Core™ Ultra 7 プロセッサー 258V",
      "npu": "インテル® AI Boost (最大47TOPS)",
      "memory": "32GB LPDDR5X-8533",
      "ssd": "約512GB",
      "wireless": "Wi-Fi 7",
      "battery_life": "動画再生時:約15.5時間 / アイドル時:約36.0時間",
      "weight": "約848g"
    },
    "security_features": "電源ボタンにはWindows Hello対応指紋センサーを搭載。Webカメラにはプライバシーカメラシャッター搭載で使わない時にも安心。"
  }
]
```
```
