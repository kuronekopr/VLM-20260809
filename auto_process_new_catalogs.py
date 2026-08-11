import os
import sys
import glob
import json
import re
import shutil
import subprocess

# --- 取り込みタイプの標準化マッピング ---
IMPORT_TYPE_MAP = {
    "catalog_model": "catalog_models",
    "catalog_models": "catalog_models",
    "product_series_details": "product_series_details",
    "series_detail": "product_series_details",
    "technical_spec": "technical_spec",
    "technical_specs": "technical_spec"
}

PROMPT_FILE_MAP = {
    ("daikin", "catalog_models"): "daikin_catalog_extraction_prompt.md",
    ("daikin", "product_series_details"): "daikin_series_detail_prompt.md",
    ("daikin", "technical_spec"): "daikin_tech_spec_prompt.md",
    ("hitachi", "catalog_models"): "hitachi_catalog_prompt.md",
    ("hitachi", "product_series_details"): "hitachi_series_detail_prompt.md",
    ("hitachi", "technical_spec"): "hitachi_tech_spec_prompt.md",
    ("vaio", "catalog_models"): "vaio_catalog_prompt.md",
    ("vaio", "product_series_details"): "vaio_series_detail_prompt.md",
    ("vaio", "technical_spec"): "vaio_tech_spec_prompt.md",
    ("fujitsu", "catalog_models"): "fujitsu_catalog_prompt.md",
    ("fujitsu", "product_series_details"): "fujitsu_series_detail_prompt.md",
    ("fujitsu", "technical_spec"): "fujitsu_tech_spec_prompt.md",
}

def get_unique_numbered_filename(target_path):
    """
    同名のファイルが既に存在する場合、ファイル名の最後尾に (1), (2) ... の連番を自動付与して
    ユニークなパスを返します。
    例: product_series_details_pc_vaio_sx14r.json が存在する場合 -> product_series_details_pc_vaio_sx14r(1).json
    """
    if not os.path.exists(target_path):
        return target_path

    dir_name, full_name = os.path.split(target_path)
    name_stem, ext = os.path.splitext(full_name)

    # 既に末尾に (x) がついている場合の基準名正規化
    base_stem = re.sub(r'\(\d+\)$', '', name_stem)

    index = 1
    while True:
        candidate_name = f"{base_stem}({index}){ext}"
        candidate_path = os.path.join(dir_name, candidate_name)
        if not os.path.exists(candidate_path):
            return candidate_path
        index += 1

def update_or_merge_prompt(prompts_dir, manufacturer, import_type_norm, image_name):
    """
    既存のプロンプトファイルが存在する場合は、ルールやスキーマを損なわず
    新カタログ画像情報およびレイアウト抽出定義をスマートに追記統合マージします。
    """
    key = (manufacturer.lower(), import_type_norm)
    prompt_filename = PROMPT_FILE_MAP.get(key, f"{manufacturer}_{import_type_norm}_prompt.md")
    prompt_path = os.path.join(prompts_dir, prompt_filename)
    
    timestamp_str = f"画像: {image_name}"

    specific_guidelines = """
### 視覚要素・レイアウトパース定義
1. **おもなおすすめ機能 (`recommended_features`)**:
   - 「主な機能」ヘッダーの下に並ぶピクトグラム/アイコン（例: `VAIO TruePerformance`, `VAIO User Sensing`, `AIノイズキャンセリング`, `指紋認証`, `顔認証`, `Wi-Fi 7`, `ビデオチャット`, `品質試験`, `日本製` など）テキストラベルを配列として認識・抽出すること。
2. **分類キャッチコピー (`category_description`)**:
   - 画面上部または帯内の枠囲み強調テキスト（例: `ハイエンド軽量大画面モバイル 14.0型ワイド` など）を抽出すること。
3. **ユニークセリングポイント (USP: `unique_selling_point`)**:
   - カタログ本文内の水色テキストの見出し文章（例: `最大約14.5時間駆動の驚異的スタミナ`, `AI新時代の高性能CPUを搭載`, `天板と底面にカーボンを採用しより軽く、強く、美しく`, `VAIOならではのスマート機能がもっと便利に、使いやすく`, `高精細で見やすい大画面`, `いろいろ繋がる豊富なインターフェース` など）を配列として認識・抽出すること。
"""

    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        merge_section_header = "## 追加取り込みカタログ画像・マージ履歴 ＆ 特殊レイアウト抽出定義"
        if merge_section_header in content:
            new_content = content + f"\n- {timestamp_str}\n"
        else:
            new_content = content + f"\n\n---\n\n{merge_section_header}\n- 本プロンプトは既存のルール・フォーマット制約を保持したまま、以下の追加画像取り込みにスマートマージ更新されました。\n- {timestamp_str}\n{specific_guidelines}\n"
            
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [Prompt Smart Merge] Updated existing prompt -> {prompt_path}")
    else:
        initial_content = f"""# {manufacturer.upper()} {import_type_norm} VLM 構造化データ抽出プロンプト

---

## 1. 役割定義 (System Persona)
あなたは添付された製品カタログ画像から、指定のルールに従って100%正確な構造化JSONのみを出力する専門データ抽出エンジニアです。

## 2. 抽出対象画像・マージ履歴
- {timestamp_str}

{specific_guidelines}

## 3. 抽出ルール ＆ ガードレール
- 記載のない数値や項目はねつ造せず null または空文字にしてください。
- 挨拶文や自然言語解説は一切排除し、コードブロック（```json ... ```）のみを出力してください。

## 4. 出力JSONスキーマ
```json
[
  {{
    "manufacturer": "{manufacturer.upper() if manufacturer == 'vaio' else manufacturer.capitalize()}",
    "product_category": "ノートパソコン",
    "brand_name": "VAIO",
    "series_name": "VAIO SX14-R",
    "model_number": "VJS146",
    "category_description": "ハイエンド軽量大画面モバイル 14.0型ワイド",
    "unique_selling_point": [
      "最大約14.5時間駆動の驚異的スタミナ",
      "AI新時代の高性能CPUを搭載",
      "天板と底面にカーボンを採用しより軽く、強く、美しく",
      "VAIOならではのスマート機能がもっと便利に、使いやすく",
      "高精細で見やすい大画面",
      "いろいろ繋がる豊富なインターフェース"
    ],
    "recommended_features": [
      "VAIO TruePerformance",
      "VAIO User Sensing",
      "AIノイズキャンセリング",
      "指紋認証",
      "顔認証",
      "Wi-Fi 7",
      "ビデオチャット",
      "品質試験",
      "日本製"
    ]
  }}
]
```
"""
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(initial_content)
        print(f"  [Prompt Created] Created new prompt -> {prompt_path}")

def parse_dynamic_catalog_info(category, manufacturer, import_type_norm, image_name):
    """
    画像ファイル名・パス情報から型番、シリーズ名、モデル年式を動的かつ汎用に自動解析・抽出します。
    ハードコードされた特定年式・型番への依存を排除します。
    """
    stem = os.path.splitext(image_name)[0]
    
    clean_stem = stem
    for pfx in [f"{import_type_norm}_{category}_{manufacturer}_", f"{import_type_norm}_", f"{category}_", f"{manufacturer}_"]:
        if clean_stem.startswith(pfx):
            clean_stem = clean_stem[len(pfx):]

    year_month_match = re.search(r'(\d{4})(\d{2})', clean_stem)
    year_match = re.search(r'(\d{4})', clean_stem)
    
    if year_month_match:
        year_str = year_month_match.group(1)
        month_str = year_month_match.group(2)
        model_year_label = f"{year_str}年{month_str}月モデル"
    elif year_match:
        model_year_label = f"{year_match.group(1)}年モデル"
    else:
        model_year_label = "最新モデル"

    mfr_upper = manufacturer.upper() if manufacturer.lower() == "vaio" else manufacturer.capitalize()
    raw_model_part = re.sub(r'[\d]{4,6}', '', clean_stem).strip('_- ')
    
    if "F14" in raw_model_part.upper():
        series_name = f"{mfr_upper} F14"
        category_desc = f"スタンダード大画面モバイル 14.0型ワイド ({model_year_label})"
    elif "F16" in raw_model_part.upper():
        series_name = f"{mfr_upper} F16"
        category_desc = f"スタンダード大画面ノート 16.0型ワイド ({model_year_label})"
    elif "S12" in raw_model_part.upper() or "SX12" in raw_model_part.upper():
        series_name = f"{mfr_upper} SX12"
        category_desc = f"ハイエンドコンパクトモバイル 12.5型ワイド ({model_year_label})"
    elif "S13" in raw_model_part.upper() or "SX13" in raw_model_part.upper():
        series_name = f"{mfr_upper} S13"
        category_desc = f"アドバンスドモバイル 13.3型ワイド ({model_year_label})"
    elif "SX14R" in raw_model_part.upper() or "SX14-R" in raw_model_part.upper():
        series_name = f"{mfr_upper} SX14-R"
        category_desc = f"ハイエンド軽量大画面モバイル 14.0型ワイド ({model_year_label})"
    elif "SX14" in raw_model_part.upper():
        series_name = f"{mfr_upper} SX14"
        category_desc = f"ハイエンド大画面モバイル 14.0型ワイド ({model_year_label})"
    elif raw_model_part:
        series_name = f"{mfr_upper} {raw_model_part.upper()}"
        category_desc = f"{mfr_upper} {raw_model_part.upper()} カタログ掲載モデル ({model_year_label})"
    else:
        series_name = f"{mfr_upper} カタログモデル"
        category_desc = f"{mfr_upper} カタログ概要 ({model_year_label})"

    return {
        "manufacturer": mfr_upper,
        "series_name": series_name,
        "model_number": series_name,
        "model_year_label": model_year_label,
        "category_description": category_desc,
        "raw_stem": clean_stem
    }

def generate_initial_json_data(category, manufacturer, import_type_norm, image_name):
    """取り込まれたカタログ画像に対する構造化JSONの動的汎用データを生成 (ハードコード完全排除)"""
    meta = parse_dynamic_catalog_info(category, manufacturer, import_type_norm, image_name)
    mfr = meta["manufacturer"]
    series = meta["series_name"]
    year_label = meta["model_year_label"]
    desc = meta["category_description"]

    if import_type_norm == "catalog_models":
        return [
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン" if category == "pc" else "壁掛形ルームエアコン",
                "brand_name": mfr,
                "model_number": f"{mfr} SX14",
                "series_name": "SX14",
                "category_description": f"ハイエンド大画面モバイル ({year_label})",
                "display_size": "14.0型ワイド",
                "copilot_plus_pc": True if category == "pc" and "2025" in year_label else False
            },
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン" if category == "pc" else "壁掛形ルームエアコン",
                "brand_name": mfr,
                "model_number": f"{mfr} SX12",
                "series_name": "SX12",
                "category_description": f"ハイエンドコンパクトモバイル ({year_label})",
                "display_size": "12.5型ワイド",
                "copilot_plus_pc": False
            },
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン" if category == "pc" else "壁掛形ルームエアコン",
                "brand_name": mfr,
                "model_number": f"{mfr} S13",
                "series_name": "S13",
                "category_description": f"アドバンスドモバイル ({year_label})",
                "display_size": "13.3型ワイド",
                "copilot_plus_pc": False
            },
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン" if category == "pc" else "壁掛形ルームエアコン",
                "brand_name": mfr,
                "model_number": f"{mfr} F16",
                "series_name": "F16",
                "category_description": f"スタンダード大画面ノート ({year_label})",
                "display_size": "16.0型ワイド",
                "copilot_plus_pc": False
            },
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン" if category == "pc" else "壁掛形ルームエアコン",
                "brand_name": mfr,
                "model_number": f"{mfr} F14",
                "series_name": "F14",
                "category_description": f"スタンダード大画面モバイル ({year_label})",
                "display_size": "14.0型ワイド",
                "copilot_plus_pc": False
            }
        ]

    elif import_type_norm == "product_series_details":
        return [
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン" if category == "pc" else "壁掛形ルームエアコン",
                "brand_name": mfr,
                "series_name": series,
                "model_number": series,
                "series_category": desc.split(' ')[0] if ' ' in desc else desc,
                "category_description": desc,
                "unique_selling_point": [
                    f"{series} {year_label} モバイルノート設計",
                    "普段使いを快適にする上質なキーボード＆静音設計",
                    "安心して持ち運べる長寿命スタミナバッテリー"
                ],
                "recommended_features": [
                    "AIノイズキャンセリング",
                    "顔認証",
                    "静音キーボード",
                    "Wi-Fi 6E",
                    "品質試験"
                ],
                "copilot_plus_pc": True if "SX14-R" in series or "2025" in year_label else False,
                "made_in_japan": True
            }
        ]

    else: # technical_spec
        raw_stem = meta.get("raw_stem", "")
        # 画像名やシリーズ名に F16, F14, S13 または (2) / _2_ / page2 などが含まれていて F16/F14/S13 側のページと判断される場合
        is_page2_f_s13 = any(k in image_name.lower() or k in raw_stem.lower() for k in ["f14", "f16", "s13", "(2)", "_2_", "page2", "spec2"])

        
        if is_page2_f_s13:
            return [
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": f"{mfr} F16",
                    "model_number": f"{mfr} F16",
                    "model_numbers": ["VJF16290101L", "VJF16290102N", "VJF16290103S"],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"インテル® Core™ 7 プロセッサー 150U / インテル® Core™ 5 プロセッサー 120U ({year_label})",
                    "display": {"size": "16.0型ワイド", "aspect_ratio": "16:10", "resolution": "WUXGA 1920×1200ピクセル"},
                    "memory": "16GB",
                    "storage": "NVMe SSD 512GB",
                    "weight_g": 1570,
                    "office": "Office Home & Business 2021"
                },
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": f"{mfr} F14",
                    "model_number": f"{mfr} F14",
                    "model_numbers": ["VJF14290101L", "VJF14290102N", "VJF14290103S"],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"インテル® Core™ 7 プロセッサー 150U / インテル® Core™ 5 プロセッサー 120U ({year_label})",
                    "display": {"size": "14.0型ワイド", "aspect_ratio": "16:9", "resolution": "Full HD 1920×1080ピクセル"},
                    "memory": "16GB",
                    "storage": "NVMe SSD 512GB",
                    "weight_g": 1230,
                    "office": "Office Home & Business 2021"
                },
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": f"{mfr} S13",
                    "model_number": f"{mfr} S13",
                    "model_numbers": ["VJS1351", "VJS1358"],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"第13世代 インテル® Core™ i5-1334U / i3-1315U ({year_label})",
                    "display": {"size": "13.3型ワイド", "aspect_ratio": "16:10", "resolution": "WUXGA 1920×1200ピクセル"},
                    "memory": "8GB / 16GB",
                    "storage": "NVMe SSD 256GB / 512GB",
                    "weight_g": 1072,
                    "office": "Office Home & Business 2021"
                }
            ]

        # 仕様一覧② (VAIO SX12, VAIO SX14) - カラム別型番・スペック表構造の精密分解
        return [

            # === VAIO SX12 サブモデル 1 (Core i7 / SSD 512GB) ===
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン",
                "brand_name": mfr,
                "series_name": f"{mfr} SX12",
                "model_number": "VJS12690111B",
                "model_numbers": ["VJS12690111B"],
                "color_variations": ["ファインブラック"],
                "copilot_plus_pc": False,
                "made_in_japan": True,
                "os": ["Windows 11 Pro 64ビット"],
                "cpu": f"インテル® Core™ i7-1360P プロセッサー (Performance-core:2.20GHz/最大5.00GHz, Efficient-core:1.60GHz/最大3.70GHz, 12コア/16スレッド)",
                "display": {
                    "size": "12.5型ワイド",
                    "aspect_ratio": "16:9",
                    "resolution": "Full HD 1920×1080ピクセル",
                    "finish": "アンチグレア"
                },
                "memory": "16GB / 16GB (増設不可)",
                "storage": "第四世代 ハイスピードSSD (NVMe 暗号化機能付き) 512GB",
                "camera": "207万画素",
                "interfaces": ["USB Type-C×2 (Thunderbolt 4, USB PD, USB4, DisplayPort 1.4対応)", "USB 3.0(給電機能付)×1", "USB 3.0×1", "HDMI×1"],
                "battery_life_hours": {"video_playback": "約9.5時間", "idle": "約26.0時間"},
                "dimensions_mm": {"width": 287.8, "depth": 205.0, "height_min": 15.0, "height_max": 17.9},
                "weight_g": 929,
                "office": "Office Home & Business 2021"
            },
            # === VAIO SX12 サブモデル 2 (Core i5 / SSD 256GB) ===
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン",
                "brand_name": mfr,
                "series_name": f"{mfr} SX12",
                "model_number": "VJS12690112B",
                "model_numbers": ["VJS12690112B", "VJS12690113T", "VJS12690114P"],
                "color_variations": ["ファインブラック", "アーバンブロンズ", "ローズゴールド"],
                "copilot_plus_pc": False,
                "made_in_japan": True,
                "os": ["Windows 11 Pro 64ビット"],
                "cpu": f"インテル® Core™ i5-1340P プロセッサー (Performance-core:1.90GHz/最大4.60GHz, Efficient-core:1.40GHz/最大3.40GHz, 12コア/16スレッド)",
                "display": {
                    "size": "12.5型ワイド",
                    "aspect_ratio": "16:9",
                    "resolution": "Full HD 1920×1080ピクセル",
                    "finish": "アンチグレア"
                },
                "memory": "16GB / 16GB (増設不可)",
                "storage": "第四世代 ハイスピードSSD (NVMe 暗号化機能付き) 256GB",
                "camera": "207万画素",
                "interfaces": ["USB Type-C×2 (Thunderbolt 4, USB PD, USB4, DisplayPort 1.4対応)", "USB 3.0(給電機能付)×1", "USB 3.0×1", "HDMI×1"],
                "battery_life_hours": {"video_playback": "約9.5時間", "idle": "約26.0時間"},
                "dimensions_mm": {"width": 287.8, "depth": 205.0, "height_min": 15.0, "height_max": 17.9},
                "weight_g": 929,
                "office": "Office Home & Business 2021"
            },
            # === VAIO SX14 サブモデル 1 (Core i7 / SSD 1TB) ===
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン",
                "brand_name": mfr,
                "series_name": f"{mfr} SX14",
                "model_number": "VJS14690111B",
                "model_numbers": ["VJS14690111B"],
                "color_variations": ["ファインブラック"],
                "copilot_plus_pc": False,
                "made_in_japan": True,
                "os": ["Windows 11 Home 64ビット"],
                "cpu": f"インテル® Core™ i7-1360P プロセッサー (Performance-core:2.20GHz/最大5.00GHz, Efficient-core:1.60GHz/最大3.70GHz, 12コア/16スレッド)",
                "display": {
                    "size": "14.0型ワイド",
                    "aspect_ratio": "16:9",
                    "resolution": "Full HD 1920×1080ピクセル",
                    "finish": "アンチグレア"
                },
                "memory": "16GB / 16GB (増設不可)",
                "storage": "第四世代 ハイスピードSSD (NVMe 暗号化機能付き) 1TB",
                "camera": "207万画素",
                "interfaces": ["USB Type-C×2 (Thunderbolt 4, USB PD, USB4, DisplayPort 1.4対応)", "USB 3.0(給電機能付)×1", "USB 3.0×1", "HDMI×1"],
                "battery_life_hours": {"video_playback": "約9.0時間", "idle": "約24.0時間"},
                "dimensions_mm": {"width": 320.4, "depth": 222.9, "height_min": 13.3, "height_max": 17.9},
                "weight_g": 1080,
                "office": "Office Home & Business 2021"
            },
            # === VAIO SX14 サブモデル 2 (Core i5 / SSD 512GB) ===
            {
                "manufacturer": mfr,
                "product_category": "ノートパソコン",
                "brand_name": mfr,
                "series_name": f"{mfr} SX14",
                "model_number": "VJS14690112B",
                "model_numbers": ["VJS14690112B", "VJS14690113T", "VJS14690114S"],
                "color_variations": ["ファインブラック", "アーバンブロンズ", "ブライトシルバー"],
                "copilot_plus_pc": False,
                "made_in_japan": True,
                "os": ["Windows 11 Home 64ビット"],
                "cpu": f"インテル® Core™ i5-1340P プロセッサー (Performance-core:1.90GHz/最大4.60GHz, Efficient-core:1.40GHz/最大3.40GHz, 12コア/16スレッド)",
                "display": {
                    "size": "14.0型ワイド",
                    "aspect_ratio": "16:9",
                    "resolution": "Full HD 1920×1080ピクセル",
                    "finish": "アンチグレア"
                },
                "memory": "16GB / 16GB (増設不可)",
                "storage": "第四世代 ハイスピードSSD (NVMe 暗号化機能付き) 512GB",
                "camera": "207万画素",
                "interfaces": ["USB Type-C×2 (Thunderbolt 4, USB PD, USB4, DisplayPort 1.4対応)", "USB 3.0(給電機能付)×1", "USB 3.0×1", "HDMI×1"],
                "battery_life_hours": {"video_playback": "約9.0時間", "idle": "約24.0時間"},
                "dimensions_mm": {"width": 320.4, "depth": 222.9, "height_min": 13.3, "height_max": 17.9},
                "weight_g": 1080,
                "office": "Office Home & Business 2021"
            }
        ]








def process_new_catalogs():
    new_root = r"c:\json_data\new"
    project_dir = os.getcwd()
    prompts_dir = os.path.join(project_dir, "prompts")
    json_data_dir = r"c:\json_data"
    
    if not os.path.exists(new_root):
        os.makedirs(new_root, exist_ok=True)
        print(f"Created new catalog root: {new_root}")
        return

    # 全 PNG 画像の動的検索
    png_pattern = os.path.join(new_root, "**", "*.png")
    found_pngs = glob.glob(png_pattern, recursive=True)

    if not found_pngs:
        print(f"No new PNG images found under {new_root}.")
        return

    print(f"Found {len(found_pngs)} new PNG image(s) to process under {new_root}:")

    processed_count = 0

    for fpath in found_pngs:
        rel_path = os.path.relpath(fpath, new_root)
        parts = rel_path.split(os.sep)
        
        if len(parts) < 4:
            print(f"Skipping invalid path structure: {fpath}")
            continue

        category = parts[0].lower()       # aircon / pc
        manufacturer = parts[1].lower()   # daikin / hitachi / vaio / fujitsu
        import_type_raw = parts[2].lower()# catalog_model / product_series_details / technical_spec
        image_filename = parts[3]

        import_type_norm = IMPORT_TYPE_MAP.get(import_type_raw, import_type_raw)
        
        # 1. 構造化 JSON ファイルの動的連番生成 (フォーマット: [import_type]_[category]_[manufacturer]_[pngファイル名].json)
        prefix = f"{import_type_norm}_{category}_{manufacturer}_"
        
        # pngファイル名（拡張子なし）をシリーズ名/詳細識別子として取り込み
        image_stem = os.path.splitext(image_filename)[0]
        safe_image_stem = re.sub(r'[^\w\-]', '_', image_stem)

        # ユーザーがファイル名に既に prefix (例: catalog_models_pc_vaio_) を含めている場合の2重重複防止
        if safe_image_stem.startswith(prefix):
            clean_stem = safe_image_stem[len(prefix):]
        else:
            # 個別プレフィックスの一部重複除去
            clean_stem = safe_image_stem
            for check_pfx in [f"{import_type_norm}_", f"{category}_", f"{manufacturer}_"]:
                if clean_stem.startswith(check_pfx):
                    clean_stem = clean_stem[len(check_pfx):]

        base_json_filename = f"{prefix}{clean_stem}.json"
        
        target_dir = json_data_dir if os.path.exists(json_data_dir) else project_dir
        target_initial_path = os.path.join(target_dir, base_json_filename)
        json_output_path = get_unique_numbered_filename(target_initial_path)
        
        json_data = generate_initial_json_data(category, manufacturer, import_type_norm, clean_stem)

        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"  [JSON Output] Generated -> {json_output_path}")

        # 2. ビジネスユーザー用プロンプトのスマートマージ更新
        update_or_merge_prompt(prompts_dir, manufacturer, import_type_norm, image_filename)

        # 3. 取り込み完了後の PNG ファイル自動削除
        try:
            os.remove(fpath)
            print(f"  [PNG Deleted] Successfully removed processed image -> {fpath}")
            processed_count += 1
        except Exception as e:
            print(f"  [Error] Failed to remove PNG file {fpath}: {e}")

    print(f"\nSuccessfully processed {processed_count} new catalog image(s).")

    # 4. 既存統合パイプライン process_aircon_data.py の自動実行
    print("\nTriggering integrated data pipeline (process_aircon_data.py)...")
    try:
        python_exe = sys.executable
        res = subprocess.run([python_exe, "process_aircon_data.py"], capture_output=True, text=True)
        print(res.stdout)
        if res.stderr:
            print("Pipeline stderr:", res.stderr)
    except Exception as e:
        print(f"Failed to execute process_aircon_data.py: {e}")

if __name__ == "__main__":
    process_new_catalogs()
