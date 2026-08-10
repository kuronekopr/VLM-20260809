# 標準仕様表 (JIS C 9612:2013) 用 Gemini チャットプロンプト (Technical_Specifications)

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に標準仕様表カタログ画像（P.61等のJIS規格仕様一覧表）をアップロードし、以下のプロンプトをコピペして実行することで、**電気特性・音響パワー・冷媒量・配管径・圧縮機出力が網羅された構造化JSON (Technical_Specifications)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **標準仕様表画像をアップロードする**
   - ＋ボタンや画像添付から、標準仕様表のカタログ画像（例: P.61「壁掛形 標準仕様」の細かい表）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`technical_specifications.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (標準仕様表用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付されたエアコンの標準仕様表画像（JIS C 9612:2013 準拠仕様表）から、掲載されているすべての型番について、以下の抽出ルールと出力JSONフォーマットに従って型番単位の技術仕様構造化JSONを出力してください。

【抽出ルール】
1. 機種・型番 (model_number, indoor_unit_model, outdoor_unit_model):
   - 親型番 (例: S22ATRS)、内機型番 (例: F22ATRS)、外機型番 (例: R22ARS) を漏れなく抽出してください。
2. 電源 (power_supply):
   - 単100V、単200V、単200V(直結/室外電源) など。
3. 暖房・冷房能力および電気特性 (heating / cooling):
   - 定格能力(kW)、能力変動範囲[最小, 最大](kW)
   - 低温暖房最大能力(kW)
   - 運転電流(A)および最大電流範囲[最小, 最大](A)
   - 消費電力(W)および最大消費電力範囲[最小, 最大](W)
   - 力率(%)、運転音音響パワーレベル(dB) [室内, 室外]
4. 機械・電気スペック:
   - 始動電流(A)、圧縮機出力(W)
   - 電源プラグ: 容量(A) と 形状コード (IL, II, エルバー 等)
   - 接続芯数、質量(kg) [室内, 室外]
   - 冷媒配管接続径 (mm) [液, ガス]
5. 消費電力量・冷媒スペック (annual_power_consumption_kwh / refrigerant):
   - 期間消費電力量 (kWh) [暖房期間, 冷房期間, 年間合計]
   - APF (通年エネルギー消費効率)
   - 冷媒種類 (R32)、冷媒封入量 (kg)、地球温暖化係数 GWP (675)

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "catalog_page": 15,
    "model_number": "S22ATRS",
    "indoor_unit_model": "F22ATRS",
    "outdoor_unit_model": "R22ARS",
    "power_supply": "単100V",
    "heating": {
      "rated_capacity_kw": 2.5,
      "capacity_range_kw": [0.6, 6.2],
      "low_temp_max_capacity_kw": 4.5,
      "electrical_properties": {
        "max_current_a": 4.6,
        "max_current_range_a": [18.0, 18.0],
        "max_power_w": 440,
        "max_power_range_w": [75, 1820],
        "power_factor_pct": 96
      },
      "sound_power_level_db": {
        "indoor": 59,
        "outdoor": 60
      }
    },
    "cooling": {
      "rated_capacity_kw": 2.2,
      "capacity_range_kw": [0.5, 3.3],
      "electrical_properties": {
        "max_current_a": 4.1,
        "max_current_range_a": [14.0, 14.0],
        "max_power_w": 390,
        "max_power_range_w": [75, 850],
        "power_factor_pct": 95
      },
      "sound_power_level_db": {
        "indoor": 57,
        "outdoor": 58
      }
    },
    "starting_current_a": 5.2,
    "compressor_output_w": 600,
    "power_plug": {
      "capacity_a": 20,
      "shape_code": "IL"
    },
    "connection_cores": 3,
    "weight_kg": {
      "indoor": 16,
      "outdoor": 43
    },
    "piping_diameter_mm": {
      "liquid": 6.4,
      "gas": 9.5
    },
    "annual_power_consumption_kwh": {
      "heating_total": 433,
      "cooling_total": 170,
      "annual_total": 603
    },
    "apf": 6.9,
    "refrigerant": {
      "type": "R32",
      "charge_amount_kg": 0.96,
      "gwp": 675
    }
  }
]
```
```
