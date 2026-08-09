# 製品詳細カタログ画像用 Gemini チャットプロンプト (Product_Series_Details)

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に製品詳細カタログ画像（シリーズ別詳細ページ）をアップロードし、以下のプロンプトをコピペして実行することで、**型番ごとの寸法・質量・詳細スペック・機能付き構造化JSON (Product_Series_Details)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **詳細カタログ画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したいエアコンの製品詳細カタログ画像（P.15〜P.16のような型番別スペックカードと右側機能一覧があるページ）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`product_series_details.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (製品詳細カタログ用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付されたエアコンの製品詳細カタログ画像から、掲載されている各型番について、型番ごとの寸法、質量、配管、電源規格、冷暖房スペック、機能一覧を含めた構造化JSONを出力してください。

【抽出ルール】
1. 型番 (model_number): 掲載されているすべての型番（例: S22ATRS-W(-C), S40ATRP-W(-C) 等）を漏れなく抽出してください。
2. 室内機・室外機個別仕様 (indoor_unit / outdoor_unit):
   - 室内機・室外機それぞれの「個別の型番」「質量(kg)」「価格(税込/税抜)」を抽出してください。
3. エアコンのサイズ・寸法 (dimensions_mm):
   - 室内機の幅、高さ、奥行き (mm)
   - 室外機の幅、突起幅、奥行き、突起奥行き、高さ (mm)
4. 電源・配管スペック (power_supply / piping):
   - 電源規格 (単相/三相、100V/200V、20A等)、室外電源フラグ
   - 配管径 (液径mm/ガス径mm)、最大長(m)、チャージレス長(m)、最大高低差(m)
5. 冷暖房・省エネ能力スペック (specs):
   - 暖房: 畳数目安、能力(kW/範囲)、消費電力(W/範囲)
   - 冷房: 畳数目安、能力(kW/範囲)、消費電力(W/範囲)
   - 省エネ: 期間消費電力量(kWh)、目標年度、省エネ基準達成率(%)、通年エネルギー消費効率(APF)、低温暖房能力(kW)
6. 右側機能リスト (functions):
   - ページの右側にある機能別チェックリスト（基本運転、しつど制御、自動運転、気流制御、清潔、快適温度制御、生活便利、タイマー機能等）で選択されている機能を抽出し、各カテゴリ配列に格納してください。

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "model_number": "型番文字列 (例: S22ATRS-W(-C))",
    "series_name": "シリーズ名",
    "series_nickname": "愛称またはnull",
    "model_year": "2026年モデル",
    "unique_selling_point": "キャッチコピー",
    "color_variations": ["カラー1", "カラー2"],
    "price_total": {
      "is_open_price": false,
      "tax_included_yen": 517000,
      "tax_excluded_yen": 470000
    },
    "indoor_unit": {
      "model_number": "F22ATRS-W(-C)",
      "weight_kg": 16,
      "tax_included_yen": 209000,
      "tax_excluded_yen": 190000
    },
    "outdoor_unit": {
      "model_number": "R22ARS",
      "weight_kg": 43,
      "tax_included_yen": 308000,
      "tax_excluded_yen": 280000
    },
    "power_supply": {
      "phase": "単相",
      "voltage_v": 100,
      "current_a": 20,
      "is_outdoor_power_supply": false
    },
    "piping": {
      "liquid_mm": 6.4,
      "gas_mm": 9.5,
      "max_length_m": 15,
      "chargeless_length_m": 15,
      "max_height_difference_m": 12
    },
    "dimensions_mm": {
      "indoor": {
        "width": 798,
        "height": 295,
        "depth": 370,
        "compact_type": "半間コンパクト"
      },
      "outdoor": {
        "width": 795,
        "width_margin": 78,
        "depth": 300,
        "depth_margin": 42,
        "height": 728,
        "note": null
      }
    },
    "specs": {
      "heating": {
        "tatami_range": "6〜7畳",
        "area_m2": "9〜11㎡",
        "capacity_kw": 2.5,
        "capacity_range_kw": [0.6, 6.2],
        "power_w": 440,
        "power_range_w": [75, 1820]
      },
      "cooling": {
        "tatami_range": "6〜9畳",
        "area_m2": "10〜15㎡",
        "capacity_kw": 2.2,
        "capacity_range_kw": [0.5, 3.3],
        "power_w": 390,
        "power_range_w": [75, 850]
      },
      "energy_saving": {
        "annual_power_consumption_kwh": 603,
        "target_year": 2027,
        "achievement_rate_pct": 104,
        "apf": 6.9,
        "low_temp_heating_capacity_kw": 4.5
      }
    },
    "functions": {
      "基本運転": ["機能名"],
      "しつど制御": ["機能名"],
      "自動運転": ["機能名"],
      "気流制御": ["機能名"],
      "清潔": ["機能名"],
      "快適温度制御": ["機能名"],
      "生活便利": ["機能名"],
      "タイマー_機能": ["機能名"]
    }
  }
]
```
```
