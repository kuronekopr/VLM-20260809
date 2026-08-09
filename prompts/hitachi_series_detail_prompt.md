# 日立エアコン「白くまくん Xシリーズ詳細」カタログ用 Gemini チャットプロンプト

非エンジニアやビジネスユーザーが **Gemini Web UI (gemini.google.com)** や **Google AI Studio** のチャット画面に日立エアコンの製品詳細カタログ画像（例: P.20 Xシリーズ詳細ページ）をアップロードし、以下のプロンプトをコピペして実行することで、**メーカー名・製品カテゴリー・寸法・電気特性付きの構造化JSON (product_series_details_hitachi_x.json)** を出力できます。

---

## 📋 使い方手順 (ビジネスユーザー向け)

1. **Gemini チャットUIを開く**
   - [Gemini](https://gemini.google.com) または [Google AI Studio](https://aistudio.google.com) にアクセスします。
2. **日立エアコンの製品詳細カタログ画像をアップロードする**
   - ＋ボタンや画像添付から、抽出したい日立エアコンの製品詳細カタログ画像（「ルームエアコン Xシリーズ」詳細ページ）を添付します。
3. **プロンプトをコピペして送信する**
   - 下記の「コピペ用プロンプト」を全文コピーしてプロンプト入力欄に貼り付け、送信します。
4. **JSONデータをコピーして保存する**
   - 出力された JSON コードブロックの右上にある **「コピー」ボタン** をクリックし、`product_series_details_hitachi_x.json` として保存します。

---

## 💬 コピペ用プロンプトテンプレート (日立エアコン詳細用)

> 以下の点線内をすべてコピーして Gemini に送信してください。

```text
添付された日立エアコン「白くまくん Xシリーズ」の製品詳細カタログ画像から、掲載されているすべての型番（RAS-X2226S, RAS-XR4026Dなど）について、以下の抽出ルールとJSONフォーマットに従って型番単位の詳細構造化JSONを出力してください。

【抽出ルール】
1. 基本識別子 (manufacturer / product_category / brand_name):
   - manufacturer: "日立"
   - product_category: "壁掛形ルームエアコン"
   - brand_name: "白くまくん"
2. 型番および個別ユニット型番 (model_number / indoor_unit / outdoor_unit):
   - 型番 (例: RAS-X2226S, RAS-XR4026D)
   - 室外機型番 (例: RAC-XR2226S, RAC-XR4026D)
3. 寸法情報 (dimensions_mm):
   - 室内機寸法 (幅, 高さ, 奥行 mm)
   - 室外機寸法 (幅, 幅マージン, 奥行, 奥行マージン, 高さ mm)
4. 電気・配管スペック (power_supply / piping):
   - 電源: 単相 100V / 200V, 容量 20A
   - 配管: 液管 6.4mm, ガス管 9.5mm, 最大長 20m, チャージレス 20m, 高低差 10m
5. 詳細仕様 (specs):
   - 暖房・冷房の畳数目安、能力(kW)、可変能力範囲(kW)、消費電力(W)、可変消費電力範囲(W)
   - 省エネ: 期間消費電力量 (kWh), 2027年度達成率 (%), APF, 低温暖房能力 (kW)
6. 右側機能フラグ (functions):
   - 右側カラムに並んでいるすべての機能項目（Premiumプラズマ空清, 凍結洗浄 ヒートプラス, ファンお掃除ロボ, カビバスター, くらしセンサー, つつみこみ暖房, カラっと除湿など）を分類抽出してください。

【出力フォーマット】
解説や挨拶文は不要です。以下のJSON構造のコードブロック（```json ... ```）のみを出力してください。

```json
[
  {
    "manufacturer": "日立",
    "product_category": "壁掛形ルームエアコン",
    "brand_name": "白くまくん",
    "model_number": "RAS-X2226S",
    "series_name": "Xシリーズ",
    "series_nickname": "白くまくん",
    "model_year": "2026年モデル",
    "unique_selling_point": "[LA自慢]・[凍結洗浄 ヒートプラス]・[ファンお掃除ロボ]・[Premiumプラズマ空清]・[凍結洗浄 クリーナー] 搭載プレミアムモデル",
    "color_variations": ["スターホワイト(W)"],
    "recommendation_tags": ["東北電力推薦 暖房エアコン", "ZEHにもおすすめ", "フロンラベル A", "日本製"],
    "price_total": {
      "is_open_price": true,
      "energy_saving_achievement_pct": 110,
      "raw_text": "オープン価格 (省エネ達成率 110%)"
    },
    "indoor_unit": {
      "model_number": "RAS-X2226S",
      "weight_kg": null,
      "is_open_price": true
    },
    "outdoor_unit": {
      "model_number": "RAC-XR2226S",
      "weight_kg": null,
      "is_open_price": true
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
      "max_length_m": 20,
      "chargeless_length_m": 20,
      "max_height_difference_m": 10
    },
    "dimensions_mm": {
      "indoor": { "width": 798, "height": 295, "depth": 385 },
      "outdoor": { "width": 799, "width_margin": 97, "depth": 299, "depth_margin": 68, "height": 629 }
    },
    "specs": {
      "heating": { "tatami_range": "6〜7畳", "area_m2": "9〜11㎡", "capacity_kw": 2.5, "capacity_range_kw": [0.3, 6.0], "power_w": 430, "power_range_w": [110, 1490] },
      "cooling": { "tatami_range": "6〜9畳", "area_m2": "10〜15㎡", "capacity_kw": 2.2, "capacity_range_kw": [0.4, 3.5], "power_w": 400, "power_range_w": [115, 900] },
      "energy_saving": { "annual_power_consumption_kwh": 570, "target_year": 2027, "achievement_rate_pct": 110, "apf": 7.3, "low_temp_heating_capacity_kw": 4.5 }
    },
    "functions": {
      "空気清浄": ["Premiumプラズマ空清", "凍結洗浄 クリーナー", "プラス換気ユニット (別売)"],
      "室外お掃除": ["室外熱交換器 凍結洗浄"],
      "熱交換器_清潔": ["ヒートプラス (熱交換器高温加熱)", "不在時に自動洗浄"],
      "ファン清潔": ["ファンお掃除ロボ (ファンの汚れを自動お掃除)"],
      "エアコン内部清潔": ["ステンレス・クリーン システム", "カビバスター (エアコン内部クリーン)"],
      "センサー_自動": ["くらしセンサー (人感・日射センサー)", "eco運転"],
      "快適_気流": ["風よけエリアセレクト", "上下スイング", "左右スイング"],
      "除湿_冷房": ["カラっと除湿 <再熱方式>", "健康冷房 [涼快]"],
      "暖房": ["つつみこみ暖房", "スピード暖房", "温風プラス"],
      "スマホ連携": ["白くまくんアプリ (無線LAN機能内蔵)"]
    }
  }
]
```
```
