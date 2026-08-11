# VAIO ノートパソコン仕様一覧表用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に VAIO ノートパソコンの仕様一覧表画像（仕様一覧① P.25-26、仕様一覧③ P.29-30など）をアップロードし、以下のプロンプトをコピペして実行することで、**CPU・メモリ・ストレージ・駆動時間・寸法質量付きの標準仕様JSON (technical_spec_pc_vaio.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **VAIO カタログの仕様一覧画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい VAIO ノートパソコンの仕様一覧表画像（P.25-26, P.29-30など）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`technical_spec_pc_vaio.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (VAIO 仕様一覧用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された VAIO ノートパソコンの仕様一覧表画像から、掲載されている各シリーズ（VAIO SX14-R, VAIO S13, VAIO F16, VAIO F14 など）について、以下の抽出ルールとJSONフォーマットに従って構造化JSONを出力してください。

【抽出ルール】
1. 基本情報 (manufacturer / product_category / brand_name / series_name):
   - manufacturer: "VAIO"
   - product_category: "ノートパソコン"
   - brand_name: "VAIO"
   - series_name: シリーズ名 (例: "VAIO SX12")
2. 型番一覧 ＆ カラム別サブモデルの分割認識 (model_numbers / model_number):
   - 同一シリーズ名の下に複数の型番（例: 左カラム `VJS12690111B` / 右カラム `VJS12690112B`, `VJS12690113T`, `VJS12690114P`）が並び、CPUやストレージ容量（SSD 512GB vs 256GB）が異なる場合は、**型番サブモデルごとに別々のJSONオブジェクトとして分割抽出**すること。
3. システム・CPU情報 (os / cpu):
   - OSバージョン
   - 各型番カラムに対応するCPUプロセッサー (例: Core i7-1360P / Core i5-1340P)
4. ディスプレイ・メモリ・ストレージ (display / memory / storage / camera):
   - 画面サイズ, アスペクト比, 解像度, 表面処理
   - メモリ容量
   - 各型番カラムに対応するストレージ容量 (例: 第四世代 ハイスピードSSD 512GB / 256GB)
   - カメラ画素数
5. 無線・インターフェース (wireless / interfaces / biometrics):
   - Wi-Fi規格, Bluetoothバージョン
   - 搭載端子ポート構成
   - 生体認証方式
6. バッテリー・寸法・質量 (battery_life_hours / dimensions_mm / weight_kg):
   - 動画再生時間 / アイドル駆動時間
   - 外形寸法 (幅 × 高さmin〜max × 奥行 mm)
   - 本体質量 (kg / g)


【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "manufacturer": "VAIO",
    "product_category": "ノートパソコン",
    "brand_name": "VAIO",
    "series_name": "VAIO SX14-R",
    "model_numbers": [
      "VJS14R19011B",
      "VJS14R19021B"
    ],
    "os": [
      "Windows 11 Home 64ビット",
      "Windows 11 Pro 64ビット"
    ],
    "cpu_options": [
      "インテル® Core™ Ultra 7 155H プロセッサー (16コア/22スレッド, TDP 28W)",
      "インテル® Core™ Ultra 5 125H プロセッサー (14コア/18スレッド, TDP 28W)",
      "インテル® Core™ Ultra 5 325U プロセッサー (12コア/14スレッド, NPU最大47TOPS, TDP 15W) Copilot+PC対応"
    ],
    "display": {
      "size": "14.0型ワイド",
      "aspect_ratio": "16:10",
      "resolution": "WUXGA 1920×1200ピクセル",
      "finish": "アンチグレア",
      "touch": false
    },
    "memory": "16GB / 32GB (増設不可)",
    "storage": "第四世代 / 第五世代 ハイスピードSSD (NVMe 暗号化機能付き) 512GB",
    "camera": "921万画素",
    "wireless": {
      "wifi": "IEEE 802.11a/b/g/n/ac/ax/be準拠, Wi-Fi 7適合, WPA3対応",
      "bluetooth": "Bluetooth® 5.4準拠"
    },
    "interfaces": [
      "USB Type-C×2 (Thunderbolt 4, USB Power Delivery, USB4, USB 3.2, DisplayPort 2.1)",
      "USB 3.0×1",
      "HDMI (出力)×1"
    ],
    "keyboard_touchpad": "バックライト付 (キーピッチ約19mm, キーストローク約1.5mm, テンキー無), 高精度タッチパッド (ジェスチャー機能, 2ボタン付き)",
    "biometrics": [
      "指紋認証",
      "顔認証"
    ],
    "battery_life_hours": {
      "video_playback": "約10.5時間〜15.0時間",
      "idle": "約26.0時間〜35.0時間"
    },
    "dimensions_mm": {
      "width": 312.0,
      "height_min": 13.9,
      "height_max": 18.9,
      "depth": 226.4
    },
    "weight_kg": {
      "min_kg": 0.967,
      "max_kg": 1.067
    },
    "bundled_office": "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
    "warranty": "1年"
  }
]
```
```


---

## 追加取り込みカタログ画像・マージ履歴 ＆ 特殊レイアウト抽出定義
- 本プロンプトは既存のルール・フォーマット制約を保持したまま、以下の追加画像取り込みにスマートマージ更新されました。
- 画像: spec_v1.png

### 視覚要素・レイアウトパース定義
1. **おもなおすすめ機能 (`recommended_features`)**:
   - 「主な機能」ヘッダーの下に並ぶピクトグラム/アイコン（例: `VAIO TruePerformance`, `VAIO User Sensing`, `AIノイズキャンセリング`, `指紋認証`, `顔認証`, `Wi-Fi 7`, `ビデオチャット`, `品質試験`, `日本製` など）テキストラベルを配列として認識・抽出すること。
2. **分類キャッチコピー (`category_description`)**:
   - 画面上部または帯内の枠囲み強調テキスト（例: `ハイエンド軽量大画面モバイル 14.0型ワイド` など）を抽出すること。
3. **ユニークセリングポイント (USP: `unique_selling_point`)**:
   - カタログ本文内の水色テキストの見出し文章（例: `最大約14.5時間駆動の驚異的スタミナ`, `AI新時代の高性能CPUを搭載`, `天板と底面にカーボンを採用しより軽く、強く、美しく`, `VAIOならではのスマート機能がもっと便利に、使いやすく`, `高精細で見やすい大画面`, `いろいろ繋がる豊富なインターフェース` など）を配列として認識・抽出すること。


- 画像: technical_spec_pc_vaio_202507 (2).png

- 画像: technical_spec_pc_vaio_202507.png

- 画像: technical_spec_pc_vaio_202507 (2).png

- 画像: technical_spec_pc_vaio_202507.png

- 画像: technical_spec_pc_vaio_202507 (2).png

- 画像: technical_spec_pc_vaio_202507.png

- 画像: technical_spec_pc_vaio_202507 (2).png

- 画像: technical_spec_pc_vaio_202507.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png

- 画像: technical_spec_pc_vaio_202406(2).png

- 画像: technical_spec_pc_vaio_202406.png
