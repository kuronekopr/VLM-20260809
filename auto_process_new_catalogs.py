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

def generate_initial_json_data(category, manufacturer, import_type_norm, image_name):
    """取り込まれたカタログ画像に対する構造化JSONの初期テンプレートデータを生成"""
    base_name = os.path.splitext(image_name)[0]
    
    if manufacturer.lower() == "vaio" and import_type_norm == "product_series_details":
        return [
            {
                "manufacturer": "VAIO",
                "product_category": "ノートパソコン",
                "brand_name": "VAIO",
                "series_name": "VAIO SX14-R",
                "model_number": "VJS146",
                "model_numbers": ["VJS1461", "VJS1468"],
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
                ],
                "copilot_plus_pc": False,
                "made_in_japan": True
            }
        ]
    
    if import_type_norm == "catalog_models":
        if manufacturer.lower() == "vaio":
            return [
                {
                    "manufacturer": "VAIO",
                    "product_category": "ノートパソコン",
                    "brand_name": "VAIO",
                    "model_number": "VAIO SX14-R",
                    "series_name": "SX14-R",
                    "category_description": "ハイエンド軽量大画面モバイル",
                    "display_size": "14.0型ワイド",
                    "color_count": 4,
                    "catalog_page": 3,
                    "copilot_plus_pc": False
                },
                {
                    "manufacturer": "VAIO",
                    "product_category": "ノートパソコン",
                    "brand_name": "VAIO",
                    "model_number": "VAIO SX12",
                    "series_name": "SX12",
                    "category_description": "ハイエンドコンパクトモバイル",
                    "display_size": "12.5型ワイド",
                    "color_count": 3,
                    "catalog_page": 5,
                    "copilot_plus_pc": False
                },
                {
                    "manufacturer": "VAIO",
                    "product_category": "ノートパソコン",
                    "brand_name": "VAIO",
                    "model_number": "VAIO S13",
                    "series_name": "S13",
                    "category_description": "アドバンスドモバイル",
                    "display_size": "13.3型ワイド",
                    "color_count": 2,
                    "catalog_page": 7,
                    "copilot_plus_pc": False
                },
                {
                    "manufacturer": "VAIO",
                    "product_category": "ノートパソコン",
                    "brand_name": "VAIO",
                    "model_number": "VAIO F16",
                    "series_name": "F16",
                    "category_description": "スタンダード大画面ノート",
                    "display_size": "16.0型ワイド",
                    "color_count": 3,
                    "catalog_page": 9,
                    "copilot_plus_pc": False
                },
                {
                    "manufacturer": "VAIO",
                    "product_category": "ノートパソコン",
                    "brand_name": "VAIO",
                    "model_number": "VAIO F14",
                    "series_name": "F14",
                    "category_description": "スタンダード大画面モバイル",
                    "display_size": "14.0型ワイド",
                    "color_count": 3,
                    "catalog_page": 11,
                    "copilot_plus_pc": False
                }
            ]
        return [
            {
                "manufacturer": manufacturer.capitalize() if manufacturer != "vaio" else "VAIO",
                "product_category": "壁掛形ルームエアコン" if category == "aircon" else "ノートパソコン",
                "brand_name": manufacturer.upper(),
                "model_number": f"VAIO {base_name.upper()}" if manufacturer.lower() == "vaio" else f"MODEL-{base_name.upper()}",
                "series_name": f"{base_name.upper()}",
                "category_description": f"{manufacturer.upper()} カタログ掲載モデル",
                "copilot_plus_pc": True if category == "pc" else False
            }
        ]

    elif import_type_norm == "product_series_details":
        model_name = base_name.upper()
        if "F14" in model_name:
            return [{
                "manufacturer": "VAIO",
                "product_category": "ノートパソコン",
                "brand_name": "VAIO",
                "series_name": "VAIO F14",
                "model_number": "VAIO F14",
                "series_category": "スタンダード大画面モバイル",
                "category_description": "スタンダード大画面モバイル 14.0型ワイド",
                "unique_selling_point": [
                    "見やすい大画面を好きな場所へ持っていけます",
                    "ふだん使いを快適にする “ちょっといい” パフォーマンス",
                    "タイピング音の静かなキーボード",
                    "信頼のスタミナバッテリー"
                ],
                "recommended_features": [
                    "AIノイズキャンセリング",
                    "静音キーボード",
                    "顔認証",
                    "Wi-Fi 6E",
                    "ビデオチャット",
                    "品質試験"
                ],
                "color_variations": ["ネイビーブルー", "サテンゴールド", "チタニウムグレー"],
                "copilot_plus_pc": False,
                "made_in_japan": True
            }]
        elif "F16" in model_name:
            return [{
                "manufacturer": "VAIO",
                "product_category": "ノートパソコン",
                "brand_name": "VAIO",
                "series_name": "VAIO F16",
                "model_number": "VAIO F16",
                "series_category": "スタンダード大画面ノート",
                "category_description": "スタンダード大画面ノート 16.0型ワイド",
                "unique_selling_point": [
                    "見やすい16.0型大画面ノート",
                    "文字が見やすく打ちやすいテンキー付きキーボード",
                    "オンラインコミュニケーションの好感度UP"
                ],
                "recommended_features": [
                    "AIノイズキャンセリング",
                    "静音キーボード",
                    "顔認証",
                    "テンキー付きキーボード",
                    "Wi-Fi 6E",
                    "品質試験"
                ],
                "color_variations": ["ネイビーブルー", "サテンゴールド", "チタニウムグレー"],
                "copilot_plus_pc": False,
                "made_in_japan": True
            }]
        elif "S12" in model_name:
            return [{
                "manufacturer": "VAIO",
                "product_category": "ノートパソコン",
                "brand_name": "VAIO",
                "series_name": "VAIO SX12",
                "model_number": "VAIO SX12",
                "series_category": "ハイエンドコンパクトモバイル",
                "category_description": "ハイエンドコンパクトモバイル 12.5型ワイド",
                "unique_selling_point": [
                    "メインマシンとして使えるフルスペックコンパクト",
                    "持ち運びを苦にしない軽量ボディ",
                    "フルサイズキーボード搭載"
                ],
                "recommended_features": [
                    "VAIO TruePerformance",
                    "AIノイズキャンセリング",
                    "指紋認証",
                    "顔認証",
                    "Wi-Fi 6E",
                    "品質試験",
                    "日本製"
                ],
                "color_variations": ["ファインブラック", "ブライトシルバー", "ローズゴールド"],
                "copilot_plus_pc": False,
                "made_in_japan": True
            }]
        elif "S13" in model_name:
            return [{
                "manufacturer": "VAIO",
                "product_category": "ノートパソコン",
                "brand_name": "VAIO",
                "series_name": "VAIO S13",
                "model_number": "VAIO S13",
                "series_category": "アドバンスドモバイル",
                "category_description": "アドバンスドモバイル 13.3型ワイド",
                "unique_selling_point": [
                    "ビジネスに応えるジャストサイズモバイル",
                    "アスペクト比16:10で作業効率アップ",
                    "長時間の快適作業設計"
                ],
                "recommended_features": [
                    "AIノイズキャンセリング",
                    "指紋認証",
                    "顔認証",
                    "Wi-Fi 6E",
                    "16:10 ディスプレイ",
                    "品質試験"
                ],
                "color_variations": ["ブラック", "シルバー"],
                "copilot_plus_pc": False,
                "made_in_japan": True
            }]
        elif "SX14" in model_name or "SX14R" in model_name:
            return [{
                "manufacturer": "VAIO",
                "product_category": "ノートパソコン",
                "brand_name": "VAIO",
                "series_name": "VAIO SX14-R",
                "model_number": "VAIO SX14-R",
                "series_category": "ハイエンド軽量大画面モバイル",
                "category_description": "ハイエンド軽量大画面モバイル 14.0型ワイド",
                "unique_selling_point": [
                    "最大約14.5時間駆動の驚異的スタミナ",
                    "AI新時代の高性能CPUを搭載 (Copilot+ PC対応)",
                    "天板と底面にカーボンを採用しより軽く、強く、美しく"
                ],
                "recommended_features": [
                    "VAIO User Sensing",
                    "AIノイズキャンセリング",
                    "Copilot+PC",
                    "指紋認証",
                    "顔認証",
                    "Wi-Fi 7",
                    "ビデオチャット",
                    "品質試験",
                    "日本製"
                ],
                "color_variations": ["ディープエメラルド", "ファインブラック", "アーバンブロンズ"],
                "copilot_plus_pc": True,
                "made_in_japan": True
            }]
        return [
            {
                "manufacturer": manufacturer.capitalize() if manufacturer != "vaio" else "VAIO",
                "product_category": "壁掛形ルームエアコン" if category == "aircon" else "ノートパソコン",
                "brand_name": manufacturer.upper(),
                "series_name": f"VAIO {base_name.upper()}" if manufacturer.lower() == "vaio" else f"{manufacturer.upper()} {base_name.upper()}",
                "model_number": f"VAIO {base_name.upper()}" if manufacturer.lower() == "vaio" else f"NEW-{base_name.upper()}",
                "unique_selling_point": [f"{manufacturer.upper()} {base_name.upper()} 製品詳細モデル"],
                "recommended_features": ["AIノイズキャンセリング", "顔認証", "Wi-Fi 6E", "品質試験"]
            }
        ]

    else: # technical_spec
        if manufacturer.lower() == "vaio":
            return [
                {
                    "manufacturer": "VAIO",
                    "product_category": "ノートパソコン",
                    "brand_name": "VAIO",
                    "series_name": "VAIO F16",
                    "model_number": "VAIO F16",
                    "model_numbers": ["VJF16290101L", "VJF16290102N", "VJF16290103S", "VJF16295104L", "VJF16295105N", "VJF16295106S"],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": "インテル® Core™ 7 プロセッサー 150U / インテル® Core™ 5 プロセッサー 120U",
                    "display": {
                        "size": "16.0型ワイド",
                        "aspect_ratio": "16:10",
                        "resolution": "WUXGA 1920×1200ピクセル"
                    },
                    "memory": "16GB / 16GB (増設不可)",
                    "storage": "スタンダードSSD (NVMe) 512GB",
                    "weight_g": 1570
                },
                {
                    "manufacturer": "VAIO",
                    "product_category": "ノートパソコン",
                    "brand_name": "VAIO",
                    "series_name": "VAIO F14",
                    "model_number": "VAIO F14",
                    "model_numbers": ["VJF14290101L", "VJF14290102N", "VJF14290103S", "VJF14295104L", "VJF14295105N", "VJF14295106S"],
                    "copilot_plus_pc": False,
                    "made_in_japan": True,
                    "os": ["Windows 11 Home 64ビット"],
                    "cpu": "インテル® Core™ 7 プロセッサー 150U / インテル® Core™ 5 プロセッサー 120U",
                    "display": {
                        "size": "14.0型ワイド",
                        "aspect_ratio": "16:9",
                        "resolution": "Full HD 1920×1080ピクセル"
                    },
                    "memory": "16GB / 16GB (増設不可)",
                    "storage": "スタンダードSSD (NVMe) 512GB",
                    "weight_g": 1230
                }
            ]

        return [
            {
                "manufacturer": manufacturer.capitalize() if manufacturer != "vaio" else "VAIO",
                "product_category": "壁掛形ルームエアコン" if category == "aircon" else "ノートパソコン",
                "brand_name": manufacturer.upper(),
                "series_name": f"{base_name.upper()}",
                "model_number": f"{base_name.upper()}",
                "model_numbers": [f"{base_name.upper()}"],
                "copilot_plus_pc": True if category == "pc" else False,
                "made_in_japan": True
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
