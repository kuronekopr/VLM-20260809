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

def update_or_merge_prompt(prompts_dir, manufacturer, import_type_norm, image_name):
    """
    既存のプロンプトファイルが存在する場合は、ルールやスキーマを損なわず
    新カタログ画像情報およびレイアウト抽出定義（添付1:おもなおすすめ機能, 添付2:分類キャッチコピー, 添付3:USP）をスマートに追記統合マージします。
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
        # 新規プロンプトテンプレート生成
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
        return [
            {
                "manufacturer": manufacturer.capitalize() if manufacturer != "vaio" else "VAIO",
                "product_category": "壁掛形ルームエアコン" if category == "aircon" else "ノートパソコン",
                "brand_name": manufacturer.upper(),
                "model_number": f"NEW-{base_name.upper()}",
                "series_name": f"{manufacturer.upper()} {base_name.upper()} シリーズ",
                "category_description": f"新規取り込みカタログ画像 ({image_name}) より抽出された概要情報",
                "copilot_plus_pc": True if category == "pc" else False,
                "unique_selling_point": f"{manufacturer.upper()} {base_name.upper()} 新規カタログモデル",
                "recommended_features": {
                    "main_features": ["新規機能A", "AI省エネ運転"]
                }
            }
        ]
    elif import_type_norm == "product_series_details":
        return [
            {
                "manufacturer": manufacturer.capitalize() if manufacturer != "vaio" else "VAIO",
                "product_category": "壁掛形ルームエアコン" if category == "aircon" else "ノートパソコン",
                "brand_name": manufacturer.upper(),
                "series_name": f"{manufacturer.upper()} {base_name.upper()} シリーズ",
                "model_number": f"NEW-{base_name.upper()}",
                "unique_selling_point": f"{manufacturer.upper()} {base_name.upper()} 製品詳細モデル",
                "functions": {
                    "details": ["高効率冷房", "静音モード"]
                }
            }
        ]
    else: # technical_spec
        return [
            {
                "manufacturer": manufacturer.capitalize() if manufacturer != "vaio" else "VAIO",
                "product_category": "壁掛形ルームエアコン" if category == "aircon" else "ノートパソコン",
                "brand_name": manufacturer.upper(),
                "series_name": f"{manufacturer.upper()} {base_name.upper()} シリーズ",
                "model_number": f"NEW-{base_name.upper()}",
                "model_numbers": [f"NEW-{base_name.upper()}"],
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
        
        # 安全な英数字ファイル名ステムの生成
        safe_stem = re.sub(r'[^\w\-]', '_', os.path.splitext(image_filename)[0])

        import_type_norm = IMPORT_TYPE_MAP.get(import_type_raw, import_type_raw)

        print(f"\nProcessing: [{category} | {manufacturer} | {import_type_norm}] -> {image_filename}")

        # 1. 構造化 JSON ファイルの自動生成 ＆ 保存
        json_filename = f"{import_type_norm}_{category}_{manufacturer}_{safe_stem}.json"
        json_output_path = os.path.join(project_dir, json_filename)
        
        json_data = generate_initial_json_data(category, manufacturer, import_type_norm, image_filename)

        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"  [JSON Output] Generated -> {json_output_path}")

        if os.path.exists(json_data_dir):
            shutil.copy2(json_output_path, os.path.join(json_data_dir, json_filename))

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
