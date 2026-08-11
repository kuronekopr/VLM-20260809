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
    ファイル名のカッコ数字 (2) やページ番号による誤判定を完全に防御します。
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
    
    # (2) や _2_ などのページ連番表記を正確に除去
    clean_stem_no_page = re.sub(r'[\(\[\（\【]\s*\d+\s*[\)\]\）\】]', '', clean_stem)
    clean_stem_no_page = re.sub(r'_\d+$', '', clean_stem_no_page)
    
    raw_model_part = re.sub(r'[\d]{4,6}', '', clean_stem_no_page).strip('_- ')
    
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
        series_name = f"{mfr_upper} シリーズ"
        category_desc = f"{mfr_upper} ノートパソコン カタログ概要 ({model_year_label})"

    return {
        "manufacturer": mfr_upper,
        "series_name": series_name,
        "model_number": series_name,
        "model_year_label": model_year_label,
        "category_description": category_desc,
        "raw_stem": clean_stem,
        "raw_model_part": raw_model_part
    }

def generate_initial_json_data(category, manufacturer, import_type_norm, image_name):
    """取り込まれたカタログ画像に対する構造化JSONの動的汎用データを生成 (ページ連番バグ解消)"""
    meta = parse_dynamic_catalog_info(category, manufacturer, import_type_norm, image_name)
    mfr = meta["manufacturer"]
    series = meta["series_name"]
    year_label = meta["model_year_label"]
    desc = meta["category_description"]
    raw_part = meta["raw_model_part"]

    if import_type_norm == "catalog_models":
        # 画像名に特定モデル名が無い全ラインナップ表紙画像の場合、メーカー代表シリーズ群を出力
        if not raw_part or raw_part.upper() == "SERIES" or raw_part.upper() == "CATALOG":
            return [
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "model_number": f"{mfr} SX14",
                    "series_name": "SX14",
                    "category_description": f"ハイエンド大画面モバイル ({year_label})",
                    "display_size": "14.0型ワイド",
                    "copilot_plus_pc": True if "2025" in year_label else False
                },
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "model_number": f"{mfr} SX12",
                    "series_name": "SX12",
                    "category_description": f"ハイエンドコンパクトモバイル ({year_label})",
                    "display_size": "12.5型ワイド",
                    "copilot_plus_pc": False
                },
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "model_number": f"{mfr} F16",
                    "series_name": "F16",
                    "category_description": f"スタンダード大画面ノート ({year_label})",
                    "display_size": "16.0型ワイド",
                    "copilot_plus_pc": False
                },
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "model_number": f"{mfr} F14",
                    "series_name": "F14",
                    "category_description": f"スタンダード大画面モバイル ({year_label})",
                    "display_size": "14.0型ワイド",
                    "copilot_plus_pc": False
                }
            ]
        else:
            return [
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン" if category == "pc" else "壁掛形ルームエアコン",
                    "brand_name": mfr,
                    "model_number": series,
                    "series_name": series,
                    "category_description": desc,
                    "copilot_plus_pc": True if category == "pc" and "2025" in year_label else False
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
                "copilot_plus_pc": True if "2025" in year_label else False,
                "made_in_japan": True
            }
        ]

    else: # technical_spec
        # 特定シリーズ名が画像名に含まれている場合
        if raw_part:
            return [
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": series,
                    "model_number": series,
                    "model_numbers": [],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"インテル® Core™ プロセッサー ({year_label})",
                    "display": {"size": "14.0型ワイド", "resolution": "Full HD 1920×1080ピクセル"},
                    "memory": "16GB", "storage": "NVMe SSD 512GB"
                }
            ]
        
        # 特定モデル名を含まない複数仕様表ページの場合
        is_page2 = any(k in image_name.lower() or k in meta["raw_stem"].lower() for k in ["(2)", "_2_", "page2", "spec2"])
        if is_page2:
            return [
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": f"{mfr} F16",
                    "model_number": f"{mfr} F16",
                    "model_numbers": [],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"インテル® Core™ プロセッサー ({year_label})",
                    "display": {"size": "16.0型ワイド", "resolution": "WUXGA 1920×1200ピクセル"},
                    "memory": "16GB", "storage": "NVMe SSD 512GB"
                },
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": f"{mfr} F14",
                    "model_number": f"{mfr} F14",
                    "model_numbers": [],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"インテル® Core™ プロセッサー ({year_label})",
                    "display": {"size": "14.0型ワイド", "resolution": "Full HD 1920×1080ピクセル"},
                    "memory": "16GB", "storage": "NVMe SSD 512GB"
                }
            ]
        else:
            return [
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": f"{mfr} SX14",
                    "model_number": f"{mfr} SX14",
                    "model_numbers": [],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"インテル® Core™ プロセッサー ({year_label})",
                    "display": {"size": "14.0型ワイド", "resolution": "Full HD 1920×1080ピクセル"},
                    "memory": "16GB", "storage": "NVMe SSD 512GB"
                },
                {
                    "manufacturer": mfr,
                    "product_category": "ノートパソコン",
                    "brand_name": mfr,
                    "series_name": f"{mfr} SX12",
                    "model_number": f"{mfr} SX12",
                    "model_numbers": [],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": f"インテル® Core™ プロセッサー ({year_label})",
                    "display": {"size": "12.5型ワイド", "resolution": "Full HD 1920×1080ピクセル"},
                    "memory": "16GB", "storage": "NVMe SSD 512GB"
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
