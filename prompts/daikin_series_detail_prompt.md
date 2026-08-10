# 製品詳細カタログ用 Gemini チャットプロンプト (Product_Series_Details)

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に製品詳細カタログ画像（シリーズ別詳細ページ）をアップロードし、以下のプロンプトをコピペして実行することで、**寸法・質量・詳細スペック・個別機能が紐付いた構造化JSON (Product_Series_Details)** を出力できます。

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
添付されたエアコンの製品詳細カタログ画像から、掲載されているすべての型番（モデル番号）について、以下の抽出ルールと出力JSONフォーマットに従って詳細仕様付き構造化JSONを出力してください。

【詳細抽出ルール】
1. 型番 (model_number):
   - ページ内のすべての型番枠（例: S22ATRS-W(-C), S40ATRP-W(-C), S90ATRP-W(-C) など）を1つも漏らさずに抽出してください。
2. 室内機・室外機個別仕様 (indoor_unit / outdoor_unit):
   - 室内機・室外機それぞれの「個別の型番 (F22ATRS-W(-C) / R22ARS 等)」「質量 (kg)」「価格 (税込/税抜数値)」を抽出してください。
3. 電源・配管スペック (power_supply / piping):
   - 電源: 相 (単相/三相)、電圧 (100/200V)、電流 (20A等)、室外電源かどうか (is_outdoor_power_supply: true/false)。
   - 配管: 液径 (mm)、ガス径 (mm)、長尺配管最大長 (m)、チャージレス長 (m)、最大高低差 (m)。
4. 寸法サイズ (dimensions_mm):
   - 室内機: 幅 (mm)、高さ (mm)、奥行 (mm)、タイプ表記 (半間コンパクト 等)。
   - 室外機: 幅 (mm)、突起幅 (mm)、奥行 (mm)、突起奥行 (mm)、高さ (mm)。
5. 冷暖房・省エネ能力スペック (specs):
   - 暖房 / 冷房: 畳数目安、適用面積 (㎡)、能力 (kW) とその変動範囲 [最小, 最大]、消費電力 (W) とその変動範囲 [最小, 最大]。
   - 省エネ: 期間消費電力量 (kWh)、目標年度 (例: 2027)、省エネ基準達成率 (%)、APF (通年エネルギー消費効率)、低温暖房能力 (kW)。
6. 機能チェック一覧 (functions):
   - ページ右側にある機能別一覧表から、該当シリーズで背景色・チェック・文字記載がある項目を「基本運転」「しつど制御」「自動運転」「気流制御」「清潔」「快適温度制御」「生活便利」「タイマー_機能」のカテゴリごとに配列として抽出してください。

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "model_number": "S22ATRS-W(-C)",
    "series_name": "RX SERIES",
    "series_nickname": "うるさらX",
    "model_year": "2026年モデル",
    "unique_selling_point": "「2026年モデル」表記直下のキャッチコピーテキスト",
    "color_variations": ["ホワイト(-W) (N9.5)", "ベージュ(-C) (1Y 7.5/2)"],
    "recommendation_tags": ["北海道電力推薦 あったかエアコン", "ZEHにもおすすめ"],
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
      "基本運転": ["NEW プレミアムPIT制御", "プレミアム冷房"],
      "しつdo制御": ["うるる加湿 (無給水加湿)"],
      "自動運転": ["AI快適自動運転 (人・床・壁センサー/換気制御)"],
      "気流制御": ["垂直気流 (暖房・冷房)"],
      "清潔": ["給気換気／排気換気"],
      "快適温度制御": ["高温風モード (最大60℃吹出し)"],
      "生活便利": ["しつどクリーン"],
      "タイマー_機能": ["時刻設定入切タイマー (学習入タイマー)"]
    }
  }
]
```
```
