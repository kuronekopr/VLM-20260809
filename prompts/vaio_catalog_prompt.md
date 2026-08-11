# VAIO ノートパソコンカタログ Index 用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に VAIO ノートパソコンのカタログ Index 画像（P.02）をアップロードし、以下のプロンプトをコピペして実行することで、**メーカー名・製品カテゴリー・液晶画面サイズ・カラーバリエーション・Copilot+PC属性付きの構造化JSON (catalog_models_pc_vaio.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **VAIO カタログの Index 画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい VAIO ノートパソコンの Index ページ画像を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`catalog_models_pc_vaio.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (VAIO ノートPC Index用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された VAIO ノートパソコンカタログの Index 画像から、掲載されているすべてのシリーズモデル（VAIO SX14-R, VAIO SX14, VAIO SX12, VAIO S13, VAIO F16, VAIO F14 など）について、以下の抽出ルールとJSONフォーマットに従って型番・シリーズ単位の構造化JSONを出力してください。

【抽出ルール】
1. 基本識別子 (manufacturer / product_category / brand_name):
   - manufacturer: "VAIO"
   - product_category: "ノートパソコン"
   - brand_name: "VAIO"
2. 型番・シリーズ名 (model_number / series_name):
   - 画像中のシリーズ型番表記（例: VAIO SX14-R, VAIO SX14 など）
3. 特徴分類記述 (category_description):
   - 型番の上に書かれている特徴テキスト（例: "ハイエンド軽量大画面モバイル", "ハイエンド大画面モバイル", "ハイエンドコンパクトモバイル", "アドバンスドモバイル", "スタンダード大画面ノート", "スタンダード大画面モバイル"）
4. 液晶サイズおよびカラー情報 (display_size / color_variations):
   - 画面サイズ（例: "14.0型ワイド", "12.5型ワイド", "13.3型ワイド", "16.0型ワイド"）
   - 各モデルの画像やカラーサンプルに合わせたカラーバリエーションリスト
5. 属性フラグ (copilot_plus_pc / catalog_page):
   - Copilot+PC アイコンの有無 (true / false)
   - 掲載ページ番号 ([P.3] などから数値のみ抽出)

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
    "category_description": "ハイエンド軽量大画面モバイル",
    "display_size": "14.0型ワイド",
    "color_variations": [
      "ディープエメラルド",
      "ファインブラック"
    ],
    "color_count": 2,
    "catalog_page": 3,
    "copilot_plus_pc": true,
    "processor_family": "インテル® Core™ Ultra 5 シリーズ 3 プロセッサー",
    "unique_selling_point": "ハイエンド軽量大画面モバイル (14.0型ワイド) Copilot+PC対応"
  }
]
```
```


---

## 追加取り込みカタログ画像・マージ履歴 ＆ 特殊レイアウト抽出定義
- 本プロンプトは既存のルール・フォーマット制約を保持したまま、以下の追加画像取り込みにスマートマージ更新されました。
- 画像: catalog_models_pc_vaio_202507.png

### 視覚要素・レイアウトパース定義
1. **おもなおすすめ機能 (`recommended_features`)**:
   - 「主な機能」ヘッダーの下に並ぶピクトグラム/アイコン（例: `VAIO TruePerformance`, `VAIO User Sensing`, `AIノイズキャンセリング`, `指紋認証`, `顔認証`, `Wi-Fi 7`, `ビデオチャット`, `品質試験`, `日本製` など）テキストラベルを配列として認識・抽出すること。
2. **分類キャッチコピー (`category_description`)**:
   - 画面上部または帯内の枠囲み強調テキスト（例: `ハイエンド軽量大画面モバイル 14.0型ワイド` など）を抽出すること。
3. **ユニークセリングポイント (USP: `unique_selling_point`)**:
   - カタログ本文内の水色テキストの見出し文章（例: `最大約14.5時間駆動の驚異的スタミナ`, `AI新時代の高性能CPUを搭載`, `天板と底面にカーボンを採用しより軽く、強く、美しく`, `VAIOならではのスマート機能がもっと便利に、使いやすく`, `高精細で見やすい大画面`, `いろいろ繋がる豊富なインターフェース` など）を配列として認識・抽出すること。


- 画像: catalog_models_pc_vaio_202507.png

- 画像: catalog_models_pc_vaio_202507.png

- 画像: catalog_models_pc_vaio_202507.png
