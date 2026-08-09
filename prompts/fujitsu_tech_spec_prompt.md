# 富士通 (FMV) パソコン仕様一覧表用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に 富士通 FMV パソコンの仕様一覧表画像（FMV Lineup P.01〜P.04など）をアップロードし、以下のプロンプトをコピペして実行することで、**CPU・NPU・メモリ・質量・Copilot+ PCフラグ付きの標準仕様JSON (technical_specifications_fujitsu.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **富士通 FMV の仕様一覧画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい FMV パソコンの仕様一覧表画像（P.01-04など）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`technical_specifications_fujitsu.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (富士通 FMV 仕様一覧用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された 富士通 FMV パソコンの仕様一覧表画像から、掲載されているすべてのシリーズ（Note U, Note, Note M, Note C, Note P, Note A, Desktop F など）について、以下の抽出ルールとJSONフォーマットに従って構造化JSONを出力してください。

【抽出ルール】
1. 基本識別子 (manufacturer / brand_name / product_category / series_name / model_number):
   - manufacturer: "富士通"
   - brand_name: "FMV"
   - product_category: "ノートパソコン" または "一体型デスクトップ"
   - series_name: シリーズ名 (例: "Note U (UA-K1)", "Desktop F (F77-L1)")
   - model_number: 型番 (例: "FMVUASK1BA")
2. 属性フラグ (copilot_plus_pc / made_in_japan):
   - Copilot+ PC アイコンの有無 (true / false)
   - MADE IN JAPAN 日本製 アイコンの有無 (true / false)
3. パソコン基本性能 (cpu / npu / gpu / memory / storage):
   - CPUプロセッサー詳細
   - NPU性能 (最大47TOPS / 最大50TOPS / 最大12TOPSなど)
   - GPUグラフィックス名
   - メモリ容量・規格 (32GB / 16GB, LPDDR5X-8533など)
   - ストレージ規格・容量 (SSD PCIe Gen4 512GBなど)
4. ディスプレイ・通信・インターフェース (display / wireless / lan / interfaces):
   - 画面サイズ, 解像度, 表面処理, タッチ有無
   - Wi-Fi 7/6E, Bluetooth
   - ポート構成 (Thunderbolt 4, USB 3.2, HDMIなど)
5. バッテリー・外形寸法・質量 (battery_life_hours / dimensions_mm / weight_g):
   - 動画再生時間 / アイドル駆動時間
   - 外形寸法 (幅 × 奥行 × 高さ mm)
   - 本体質量 (g) （例: 848, 634, 908など）

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "manufacturer": "富士通",
    "brand_name": "FMV",
    "product_category": "ノートパソコン",
    "series_name": "Note U (UA-K1)",
    "model_number": "FMVUASK1BA",
    "copilot_plus_pc": true,
    "made_in_japan": true,
    "os": "Windows 11 Home",
    "bundled_office": "Microsoft 365 Basic + Office Home & Business 2024",
    "display": {
      "size": "14.0型ワイド (狭額縁)",
      "resolution": "1920×1200ドット (WUXGA)",
      "finish": "ノングレア液晶 (高輝度・高色純度・広視野角)",
      "touch": false
    },
    "cpu": "インテル® Core™ Ultra 7 プロセッサー 258V (Pコア最大4.8GHz / 低消費電力Eコア最大3.7GHz)",
    "npu": "インテル® AI Boost (最大47TOPS)",
    "gpu": "インテル® Arc™ グラフィックス 140V",
    "memory": "32GB (LPDDR5X-8533, 増設・交換不可)",
    "storage": "約512GB SSD (PCIe Gen4)",
    "wireless": "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
    "lan": "1000BASE-T/100BASE-TX/10BASE-T準拠",
    "interfaces": [
      "Thunderbolt™ 4 USB4 (Gen3)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
      "USB 3.2 (Gen1)×2 (うち1つは電源オフUSB充電機能付)",
      "HDMI出力端子×1",
      "microSDメモリーカードスロット"
    ],
    "camera": "フルHD Webカメラ (プライバシーカメラシャッター付, 有効画素数約207万画素)",
    "audio": "Dolby Atmos®",
    "battery_life_hours": {
      "video_playback": 15.5,
      "idle": 36.0
    },
    "dimensions_mm": {
      "width": 308.8,
      "depth": 209,
      "height_min": 15.8,
      "height_max": 17.3
    },
    "weight_g": 848
  }
]
```
```
