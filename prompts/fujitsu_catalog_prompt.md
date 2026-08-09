# 富士通 (FMV) パソコンカタログ概要 Lineup 用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に 富士通 FMV パソコンの Lineup 概要画像（Copilot+ PC Lineup P.05-06など）をアップロードし、以下のプロンプトをコピペして実行することで、**メーカー名・型番・分類・Copilot+ PC機能ハイライト付きの構造化JSON (catalog_models_pc_fujitsu.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **富士通 FMV のカタログ概要画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい FMV パソコンの Lineup 概要画像（P.05-06など）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`catalog_models_pc_fujitsu.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (富士通 FMV カタログ概要用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された 富士通 FMV パソコンのカタログ概要画像から、掲載されている各シリーズ（UQ-L1, UA-K1, U59-L1, A79-L1, F77-L1 など）について、以下の抽出ルールとJSONフォーマットに従って構造化JSONを出力してください。

【抽出ルール】
1. 基本識別子 (manufacturer / brand_name / product_category / model_number / series_name):
   - manufacturer: "富士通"
   - brand_name: "FMV"
   - product_category: "ノートパソコン" または "一体型デスクトップ"
   - model_number: 型番 (例: "UQ-L1", "UA-K1", "A79-L1", "F77-L1")
   - series_name: シリーズ名 (例: "FMV Note U", "FMV Note A", "FMV Desktop F")
2. 分類・CPU・画面サイズ (category_description / processor_family / display_size):
   - 型番下のキャッチコピー分類 (例: "長時間駆動モバイルノート", "ハイスペックモバイルノート", "タッチ対応モバイルノート", "大画面プレミアムノート", "大画面オールインワンデスクトップ")
   - CPUファミリ表記 (例: "Snapdragon® X 搭載", "Intel® Core™ Ultra 7 搭載", "AMD Ryzen™ AI 7 搭載")
   - 画面サイズ (例: "14.0型ワイド", "16.0型ワイド", "27.0型ワイド")
3. 属性フラグ・掲載ページ (copilot_plus_pc / catalog_page):
   - Copilot+ PC ロゴの有無 (true / false)
   - カタログ参照ページ (例: 7, 11, 15, "別冊カタログ")
4. Copilot+ PC おすすめ機能ハイライト (recommended_features):
   - 下部カード記載のAI機能群 (例: ["ライブキャプション", "Windows 検索の改善", "リスタイルイメージ", "写真の超解像度", "Click to Do (プレビュー)", "コクリエーター", "生成フィル", "リコール (プレビュー)"])

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "manufacturer": "富士通",
    "brand_name": "FMV",
    "product_category": "ノートパソコン",
    "model_number": "UA-K1",
    "series_name": "FMV Note U",
    "category_description": "ハイスペックモバイルノート",
    "display_size": "14.0型ワイド",
    "processor_family": "Intel® Core™ Ultra 7 搭載",
    "copilot_plus_pc": true,
    "catalog_page": 7,
    "recommended_features": [
      "ライブキャプション",
      "Windows 検索の改善",
      "リスタイルイメージ",
      "写真の超解像度",
      "Click to Do (プレビュー)",
      "コクリエーター",
      "生成フィル",
      "リコール (プレビュー)"
    ],
    "unique_selling_point": "ハイスペックモバイルノート (14.0型 Intel Core Ultra 7搭載) Copilot+ PC対応"
  }
]
```
```
