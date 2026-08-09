# 日立エアコン「仕様一覧表 (JIS C 9612:2013)」カタログ用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に日立エアコンの「冷・暖・除湿タイプ仕様一覧表 (JIS C 9612:2013)」カタログ画像をアップロードし、以下のプロンプトをコピペして実行することで、**メーカー名・製品カテゴリー・個別質量・電気・配管・冷媒封入量付きの構造化JSON (technical_specifications_hitachi.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **日立エアコンの仕様表カタログ画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい日立エアコンの「冷・暖・除湿タイプ仕様一覧表 (JIS C 9612:2013)」画像を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`technical_specifications_hitachi.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (日立仕様表用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された日立エアコンの「冷・暖・除湿タイプ仕様一覧表 (JIS C 9612:2013)」カタログ画像から、掲載されているすべての型番について、以下の抽出ルールとJSONフォーマットに従って型番単位の標準仕様構造化JSONを出力してください。

【抽出ルール】
1. 基本識別子 (manufacturer / product_category / brand_name):
   - manufacturer: "日立"
   - product_category: "壁掛形ルームエアコン"
   - brand_name: "白くまくん"
2. 型番および個別ユニット型番 (model_number / indoor_unit_model / outdoor_unit_model):
   - 室内機型番 (例: RAS-XR2226S, RAS-WR2226S)
   - 室外機型番 (例: RAC-XR2226S, RAC-WR2226S)
3. 性能値 (heating / cooling / compressor_output_w / starting_current_a):
   - 暖房: 定格能力 (kW), 定格消費電力 (W), 外気温2℃時能力 (kW) / 消費電力 (W)
   - 冷房: 定格能力 (kW), 定格消費電力 (W)
   - 圧縮機出力 (W), 始動電流 (A)
4. 物理・電気仕様 (weight_kg / power_plug / piping_diameter_mm):
   - 質量: 室内機質量 (kg), 室外機質量 (kg)
   - 電源プラグ: 15A / 20A
   - 配管径: 液管 (mm: 6.35), ガス管 (mm: 9.52 / 12.7)
5. 期間消費電力量 ＆ 省エネ区分 (annual_power_consumption_kwh / apf / energy_saving_class):
   - 期間消費電力量: 暖房 (kWh), 冷房 (kWh), 合計 (kWh)
   - APF (通年エネルギー消費効率)
   - 省エネ区分: I / II / III
6. 冷媒情報 (refrigerant):
   - 冷媒種類 (R32), 封入量 (kg), GWP (675)

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "manufacturer": "日立",
    "product_category": "壁掛形ルームエアコン",
    "brand_name": "白くまくん",
    "model_number": "RAS-XR2226S",
    "series_name": "Xシリーズ",
    "catalog_page": 20,
    "indoor_unit_model": "RAS-XR2226S",
    "outdoor_unit_model": "RAC-XR2226S",
    "power_supply": "単相100V",
    "heating": {
      "rated_capacity_kw": 2.5,
      "rated_power_w": 430,
      "low_temp_2c": { "capacity_kw": 4.5, "power_w": 1360 }
    },
    "cooling": {
      "rated_capacity_kw": 2.2,
      "rated_power_w": 400
    },
    "compressor_output_w": 600,
    "starting_current_a": 5.1,
    "weight_kg": { "indoor": 15.5, "outdoor": 31.0 },
    "power_plug": "15A",
    "piping_diameter_mm": { "liquid": 6.35, "gas": 9.52 },
    "annual_power_consumption_kwh": { "heating": 408, "cooling": 162, "annual_total": 570 },
    "apf": 7.3,
    "energy_saving_class": "I",
    "refrigerant": { "type": "R32", "charge_amount_kg": 1.08, "gwp": 675 }
  }
]
```
```
