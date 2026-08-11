import os
import glob
import json
import math
import re
from collections import Counter

# --- 1. テキスト類似度 ＆ 数値抽出ユーティリティ ---
def get_ngrams(text, n=2):
    if not text:
        return []
    text = re.sub(r'\s+', '', str(text)).lower()
    if len(text) < n:
        return [text]
    return [text[i:i+n] for i in range(len(text) - n + 1)]

def calculate_cosine_similarity(text1, text2):
    str1 = json.dumps(text1, ensure_ascii=False) if isinstance(text1, (dict, list)) else str(text1 if text1 is not None else "")
    str2 = json.dumps(text2, ensure_ascii=False) if isinstance(text2, (dict, list)) else str(text2 if text2 is not None else "")
    
    vec1 = Counter(get_ngrams(str1, n=2))
    vec2 = Counter(get_ngrams(str2, n=2))
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[x] * vec2[x] for x in intersection)
    
    norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return round(dot_product / (norm1 * norm2), 3)

def extract_numeric_value(val):
    """
    値から数値 (float/int) が抽出可能かを判定し、抽出できた場合は (True, float_val) を返す。
    抽出不可能な場合 (False, None) を返す。
    """
    if val is None or isinstance(val, bool):
        return False, None
    if isinstance(val, (int, float)):
        return True, float(val)
    
    val_str = str(val).strip()
    # "2.2kW", "967g", "110%", "1920×1200" 等からの単一数値パース
    # パターン: 単一の数値 (例: 2.2, 967, 110)
    match = re.match(r'^[^\d]*?(\d+(?:\.\d+)?)[^\d]*$', val_str)
    if match:
        try:
            return True, float(match.group(1))
        except ValueError:
            return False, None
    return False, None

def normalize_model_number(model_str):
    if not model_str:
        return ''
    m = str(model_str).strip()
    if m.startswith('S') and '-' in m:
        m = m.split('-')[0].strip()
    m = re.sub(r'\([A-Za-z0-9]+\)', '', m)
    # 日立等の RAS-XR / RAS-X 表記揺れの統一 (例: RAS-XR3626S -> RAS-X3626S)
    m = re.sub(r'RAS-?XR', 'RAS-X', m, flags=re.IGNORECASE)
    # 英数字のみに抽出正規化 (例: RAS-X3626S -> RASX3626S)
    m = re.sub(r'[^A-Za-z0-9]', '', m)
    return m.upper()

def normalize_key(s):
    if not s:
        return ''
    return re.sub(r'[\s\-_・]', '', str(s)).lower()

# --- 2. データロード ＆ ネスト展開 ---
def load_and_merge_json_files(import_type, category, manufacturer):
    pattern = f"{import_type}_{category}_{manufacturer}*.json"
    target_dir = r"c:\json_data"
    base_dir = os.getcwd()
    
    search_dirs = [target_dir] if os.path.exists(target_dir) else [base_dir]
    matched_files = []
    
    for d in search_dirs:
        search_path = os.path.join(d, pattern)
        for fpath in glob.glob(search_path):
            if fpath not in matched_files:
                matched_files.append(fpath)
                
    merged_list = []
    for fpath in sorted(matched_files):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    merged_list.extend(data)
                elif isinstance(data, dict):
                    merged_list.append(data)
        except Exception:
            pass
    return merged_list

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    return dict(items)

def extract_model_numbers(item):
    models = set()
    if item.get("model_number"):
        models.add(normalize_model_number(item["model_number"]))
    if item.get("base_model_number"):
        models.add(normalize_model_number(item["base_model_number"]))
    if item.get("indoor_unit_model"):
        models.add(normalize_model_number(item["indoor_unit_model"]))
    if item.get("outdoor_unit_model"):
        models.add(normalize_model_number(item["outdoor_unit_model"]))
    if isinstance(item.get("model_numbers"), list):
        for m in item["model_numbers"]:
            models.add(normalize_model_number(m))
    return {m for m in models if m}

def extract_capacity_code(model_str):
    if not model_str:
        return None
    match = re.search(r'(22|25|28|36|40|56|63|71|80|90)', str(model_str))
    return match.group(1) if match else None

def find_best_matched_item(det_item, target_list):
    if not det_item or not target_list:
        return None
    
    det_models = extract_model_numbers(det_item)
    series_name = det_item.get("series_name", "")
    raw_model = det_item.get("model_number") or det_item.get("base_model_number", "")
    det_cap_code = extract_capacity_code(raw_model)

    # Phase 1: 型番完全・交差一致
    if det_models:
        for t_item in target_list:
            t_models = extract_model_numbers(t_item)
            if det_models & t_models:
                return t_item

    # Phase 2: シリーズ名一致 ＋ 容量コード一致 (型番直接一致しなかった場合のスマートフォールバック)
    if series_name:
        norm_series = normalize_key(series_name)
        if det_cap_code:
            for t_item in target_list:
                if norm_series == normalize_key(t_item.get("series_name")):
                    t_models = extract_model_numbers(t_item)
                    for tm in t_models:
                        if extract_capacity_code(tm) == det_cap_code:
                            return t_item
        for t_item in target_list:
            if norm_series == normalize_key(t_item.get("series_name")):
                return t_item

    return None

# --- 3. 類似・関連項目の対応マップ定義 ---
FIELD_ALIAS_MAP = {
    # 暖房・冷房能力
    "cooling.capacity_kw": ["cooling_capacity_kw", "detail_specs.cooling.capacity_kw", "cooling.rated_capacity_kw", "specs.cooling.capacity_kw"],
    "heating.capacity_kw": ["heating_capacity_kw", "detail_specs.heating.capacity_kw", "heating.rated_capacity_kw", "specs.heating.capacity_kw"],
    "specs.cooling.capacity_kw": ["cooling_capacity_kw", "cooling.rated_capacity_kw", "cooling.capacity_kw"],
    "specs.heating.capacity_kw": ["heating_capacity_kw", "heating.rated_capacity_kw", "heating.capacity_kw"],

    # 年間消費電力量 (必須評価項目)
    "energy_saving.annual_power_consumption_kwh": ["annual_power_consumption_kwh", "annual_power_consumption_kwh.annual_total"],
    "specs.energy_saving.annual_power_consumption_kwh": ["annual_power_consumption_kwh", "annual_power_consumption_kwh.annual_total"],

    # 室内機・室外機 寸法_mm (幅・高さ・奥行 - 必須評価項目)
    "dimensions_mm.indoor.width": ["indoor_unit_dimensions_mm.width", "dimensions_mm.indoor.width", "indoor_unit.width"],
    "dimensions_mm.indoor.height": ["indoor_unit_dimensions_mm.height", "dimensions_mm.indoor.height", "indoor_unit.height"],
    "dimensions_mm.indoor.depth": ["indoor_unit_dimensions_mm.depth", "dimensions_mm.indoor.depth", "indoor_unit.depth"],
    "dimensions_mm.outdoor.width": ["outdoor_unit_dimensions_mm.width", "dimensions_mm.outdoor.width", "outdoor_unit.width"],
    "dimensions_mm.outdoor.height": ["outdoor_unit_dimensions_mm.height", "dimensions_mm.outdoor.height", "outdoor_unit.height"],
    "dimensions_mm.outdoor.depth": ["outdoor_unit_dimensions_mm.depth", "dimensions_mm.outdoor.depth", "outdoor_unit.depth"],
    "indoor_unit.dimensions_mm.width": ["indoor_unit_dimensions_mm.width", "dimensions_mm.indoor.width"],
    "indoor_unit.dimensions_mm.height": ["indoor_unit_dimensions_mm.height", "dimensions_mm.indoor.height"],
    "indoor_unit.dimensions_mm.depth": ["indoor_unit_dimensions_mm.depth", "dimensions_mm.indoor.depth"],
    "outdoor_unit.dimensions_mm.width": ["outdoor_unit_dimensions_mm.width", "dimensions_mm.outdoor.width"],
    "outdoor_unit.dimensions_mm.height": ["outdoor_unit_dimensions_mm.height", "dimensions_mm.outdoor.height"],
    "outdoor_unit.dimensions_mm.depth": ["outdoor_unit_dimensions_mm.depth", "dimensions_mm.outdoor.depth"],

    # 特徴・おすすめ機能・USP
    "unique_selling_point": ["unique_selling_point"],
    "recommended_features": ["recommended_features", "functions", "main_features"],
    "category_description": ["category_description"],
    "copilot_plus_pc": ["copilot_plus_pc"],
    "made_in_japan": ["made_in_japan"],

    # PCスペック
    "weight_g": ["weight_g", "weight_kg", "weight"],
    "memory": ["memory"],
    "storage": ["storage"],
    "os": ["os"],
    "display": ["display"]
}

def is_invalid_field_pair(detail_field_name, target_field_name):
    """
    構造的・概念的に異なる項目同士のミスマッチ比較を判定し、無効な場合 True を返す。
    """
    df = str(detail_field_name).lower()
    tf = str(target_field_name).lower()

    # 1. 価格・金額 (price, tax_*_yen) 関連の比較全般 (前提が異なるため一律評価対象外)
    if 'price' in df or 'tax_' in df or 'yen' in df or 'price' in tf or 'tax_' in tf or 'yen' in tf:
        return True

    # 2. 室内機/室外機の単品型番 vs システム総合型番
    if ('indoor_unit' in df or 'outdoor_unit' in df) and 'model_number' in df:
        if tf in ['model_number', 'base_model_number']:
            return True

    # 3. 暖房能力 vs 冷房能力 / 畳数目安能力
    if 'heating' in df:
        if 'cooling' in tf or 'applicable_room_size' in tf:
            return True

    # 4. 冷房能力 vs 暖房能力
    if 'cooling' in df:
        if 'heating' in tf:
            return True

    # 5. シリーズ代表畳数目安能力 (applicable_room_size) vs 個別型番スペック能力
    if 'applicable_room_size' in tf:
        if 'specs' in df or 'cooling' in df or 'heating' in df:
            return True

    # 6. 低温暖房能力 (low_temp, 2c) vs 通常定格能力 (異なる条件性能のため不適合)
    if ('low_temp' in df or '2c' in df) != ('low_temp' in tf or '2c' in tf):
        return True

    # 7. 質量・重量 (weight_kg, weight_g, weight) 関連の比較全般 (前提条件が異なるため一律評価対象外)
    if 'weight' in df or 'weight' in tf:
        return True

    # 8. APF (通年エネルギー消費効率) 関連の比較 (業務利用しないため一律評価対象外)
    if 'apf' in df or 'apf' in tf:
        return True

    return False

def find_target_field_and_value(target_item, detail_field_name):
    """
    商品一覧または仕様表のアイテム target_item から、detail_field_name に相当・類似するフィールドと値を探索
    """
    if not target_item:
        return None, None

    flat_target = flatten_dict(target_item)
    
    # 1. 完全一致
    if detail_field_name in flat_target:
        tf = detail_field_name
        if not is_invalid_field_pair(detail_field_name, tf):
            return tf, flat_target[tf]
    
    # 2. エイリアスマッチ
    aliases = FIELD_ALIAS_MAP.get(detail_field_name, [])
    for alias in aliases:
        if alias in flat_target and not is_invalid_field_pair(detail_field_name, alias):
            return alias, flat_target[alias]
        for tk, tv in flat_target.items():
            if normalize_key(alias) == normalize_key(tk) and not is_invalid_field_pair(detail_field_name, tk):
                return tk, tv

    # 3. フィールド名の最後要素でのマッチ (例: capacity_kw)
    last_key = detail_field_name.split('.')[-1]
    for tk, tv in flat_target.items():
        if normalize_key(last_key) == normalize_key(tk.split('.')[-1]) and not is_invalid_field_pair(detail_field_name, tk):
            return tk, tv

    # 4. 寸法 (dimensions_mm) および 年間消費電力 (annual_power_consumption_kwh) のスマートマッチ
    parts = detail_field_name.split('.')
    if 'dimensions_mm' in detail_field_name:
        loc = 'indoor' if 'indoor' in detail_field_name else ('outdoor' if 'outdoor' in detail_field_name else None)
        dim_type = parts[-1]  # width, height, depth
        if dim_type in ['width', 'height', 'depth']:
            for tk, tv in flat_target.items():
                if dim_type in tk and (loc is None or loc in tk):
                    if not is_invalid_field_pair(detail_field_name, tk):
                        return tk, tv

    if 'annual_power_consumption_kwh' in detail_field_name:
        for tk, tv in flat_target.items():
            if 'annual_power_consumption_kwh' in tk:
                if not is_invalid_field_pair(detail_field_name, tk):
                    return tk, tv

    return None, None

def is_text_field(field_name):
    """
    文章・キャッチコピー・特徴記述・型番表示等のテキストフィールドかを判定する。
    これらは文字列内に数字が含まれていても数値単体比較ではなくテキスト類似度評価を行う。
    """
    fn = str(field_name).lower()
    text_keywords = [
        'unique_selling_point', 'usp', 'recommended_features', 'functions',
        'series_name', 'series_nickname', 'category_description', 'os', 'cpu',
        'gpu', 'display', 'interface', 'communication', 'catchphrase', 'features',
        'power_supply', 'power_plug', 'refrigerant', 'model_year', 'model_number',
        'indoor_unit_model', 'outdoor_unit_model', 'copilot_plus_pc', 'made_in_japan'
    ]
    for kw in text_keywords:
        if kw in fn:
            return True
    return False

def evaluate_single_field(detail_field_name, detail_val, target_item, target_name):
    target_field, target_val = find_target_field_and_value(target_item, detail_field_name)
    
    if target_val is None or is_invalid_field_pair(detail_field_name, target_field):
        return None

    # 文章・テキスト記述フィールドは強制的にテキストコサイン類似度評価 (is_numeric_comparable = False)
    if is_text_field(detail_field_name) or is_text_field(target_field):
        is_numeric_comparable = False
        score = calculate_cosine_similarity(detail_val, target_val)
    else:
        # 純数値スペック比較判定
        is_num_detail, num_detail = extract_numeric_value(detail_val)
        is_num_target, num_target = extract_numeric_value(target_val)
        
        if is_num_detail and is_num_target:
            is_numeric_comparable = True
            # 数値比較: 完全一致 ➔ 1, 不一致 ➔ 0
            diff = abs(num_detail - num_target)
            score = 1 if diff < 1e-4 else 0
        else:
            is_numeric_comparable = False
            # コサイン類似度スコア (0.0 〜 1.0)
            score = calculate_cosine_similarity(detail_val, target_val)

    return {
        "compared_target": target_name,
        "detail_field_name": detail_field_name,
        "detail_value": detail_val,
        "target_field_name": target_field,
        "target_value": target_val,
        "is_numeric_comparable": is_numeric_comparable,
        "score": score
    }

# --- 4. メイン評価パイプライン ---
def main():
    categories = ["aircon", "pc"]
    manufacturers = {
        "aircon": ["daikin", "hitachi"],
        "pc": ["vaio", "fujitsu"]
    }

    evaluations = []
    total_comparisons = 0
    numeric_comparable_count = 0
    text_comparable_count = 0
    numeric_exact_match_count = 0
    numeric_mismatch_count = 0
    text_similarity_score_sum = 0.0

    target_breakdown = {
        "catalog_models": {
            "total_field_comparisons": 0,
            "numeric_comparable_count": 0,
            "numeric_exact_match_count (score=1)": 0,
            "numeric_mismatch_count (score=0)": 0,
            "text_comparable_count": 0,
            "text_similarity_score_sum": 0.0,
            "text_similarity_score_average": 0.0
        },
        "technical_spec": {
            "total_field_comparisons": 0,
            "numeric_comparable_count": 0,
            "numeric_exact_match_count (score=1)": 0,
            "numeric_mismatch_count (score=0)": 0,
            "text_comparable_count": 0,
            "text_similarity_score_sum": 0.0,
            "text_similarity_score_average": 0.0
        }
    }

    for cat in categories:
        for mfr in manufacturers[cat]:
            det_list = load_and_merge_json_files("product_series_details", cat, mfr)
            cat_list = load_and_merge_json_files("catalog_models", cat, mfr)
            tech_list = load_and_merge_json_files("technical_spec", cat, mfr)

            for det_item in det_list:
                mfr_name = det_item.get("manufacturer", mfr.upper())
                series_name = det_item.get("series_name", "")
                raw_model = det_item.get("model_number") or det_item.get("base_model_number", "")
                det_models = extract_model_numbers(det_item)

                # マッチする商品一覧アイテムの探索
                matched_cat_item = find_best_matched_item(det_item, cat_list)

                # マッチする仕様表アイテムの探索
                matched_tech_item = find_best_matched_item(det_item, tech_list)

                # 商品詳細のフィールドをフラット展開
                flat_detail = flatten_dict(det_item)
                item_evals = []

                for field_name, detail_val in flat_detail.items():
                    # ヘッダー・メタ記述キーはスキップ
                    if field_name in ["manufacturer", "product_category", "brand_name", "model_number", "base_model_number", "model_numbers"]:
                        continue

                    # 1. 商品一覧 (catalog_models) との比較
                    if matched_cat_item:
                        res = evaluate_single_field(field_name, detail_val, matched_cat_item, "catalog_models")
                        if res:
                            item_evals.append(res)
                            total_comparisons += 1
                            tb = target_breakdown["catalog_models"]
                            tb["total_field_comparisons"] += 1
                            if res["is_numeric_comparable"]:
                                numeric_comparable_count += 1
                                tb["numeric_comparable_count"] += 1
                                if res["score"] == 1:
                                    numeric_exact_match_count += 1
                                    tb["numeric_exact_match_count (score=1)"] += 1
                                else:
                                    numeric_mismatch_count += 1
                                    tb["numeric_mismatch_count (score=0)"] += 1
                            else:
                                text_comparable_count += 1
                                tb["text_comparable_count"] += 1
                                text_similarity_score_sum += res["score"]
                                tb["text_similarity_score_sum"] += res["score"]

                    # 2. 仕様表 (technical_spec) との比較
                    if matched_tech_item:
                        res = evaluate_single_field(field_name, detail_val, matched_tech_item, "technical_spec")
                        if res:
                            item_evals.append(res)
                            total_comparisons += 1
                            tb = target_breakdown["technical_spec"]
                            tb["total_field_comparisons"] += 1
                            if res["is_numeric_comparable"]:
                                numeric_comparable_count += 1
                                tb["numeric_comparable_count"] += 1
                                if res["score"] == 1:
                                    numeric_exact_match_count += 1
                                    tb["numeric_exact_match_count (score=1)"] += 1
                                else:
                                    numeric_mismatch_count += 1
                                    tb["numeric_mismatch_count (score=0)"] += 1
                            else:
                                text_comparable_count += 1
                                tb["text_comparable_count"] += 1
                                text_similarity_score_sum += res["score"]
                                tb["text_similarity_score_sum"] += res["score"]

                evaluations.append({
                    "manufacturer": mfr_name,
                    "product_category": det_item.get("product_category", "エアコン" if cat == "aircon" else "ノートパソコン"),
                    "series_name": series_name,
                    "model_number": raw_model,
                    "field_evaluations_count": len(item_evals),
                    "detail_field_evaluations": item_evals
                })

    text_similarity_score_sum = round(text_similarity_score_sum, 3)
    text_similarity_score_avg = round(text_similarity_score_sum / text_comparable_count, 3) if text_comparable_count > 0 else 0.0

    for t_key, tb in target_breakdown.items():
        tb["text_similarity_score_sum"] = round(tb["text_similarity_score_sum"], 3)
        tb["text_similarity_score_average"] = round(tb["text_similarity_score_sum"] / tb["text_comparable_count"], 3) if tb["text_comparable_count"] > 0 else 0.0

    summary = {
        "total_evaluated_detail_items": len(evaluations),
        "total_field_comparisons": total_comparisons,
        "numeric_comparable_count": numeric_comparable_count,
        "numeric_exact_match_count (score=1)": numeric_exact_match_count,
        "numeric_mismatch_count (score=0)": numeric_mismatch_count,
        "text_comparable_count": text_comparable_count,
        "text_similarity_score_sum": text_similarity_score_sum,
        "text_similarity_score_average": text_similarity_score_avg,
        "breakdown_by_target": target_breakdown
    }

    report = {
        "evaluation_summary": summary,
        "product_series_details_evaluations": evaluations
    }

    target_dir = r"c:\json_data" if os.path.exists(r"c:\json_data") else os.getcwd()
    out_path = os.path.join(target_dir, "feature_discrepancy_evaluation.json")
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"=== Product Series Details Feature Discrepancy Evaluation Completed ===")
    print(f"Total Detail Items Evaluated: {summary['total_evaluated_detail_items']}")
    print(f"Total Field Comparisons: {summary['total_field_comparisons']}")
    print(f"  - Numeric Comparable: {summary['numeric_comparable_count']} (Match score=1: {numeric_exact_match_count}, Mismatch score=0: {numeric_mismatch_count})")
    print(f"  - Text Cosine Similarity Comparable: {summary['text_comparable_count']}")
    print(f"    -> Text Similarity Score Total Sum: {text_similarity_score_sum} (Average: {text_similarity_score_avg})")
    print(f"\n--- Target Breakdown ---")
    for t_key in ["catalog_models", "technical_spec"]:
        tb = target_breakdown[t_key]
        print(f"[{t_key}] Total Comparisons: {tb['total_field_comparisons']}")
        print(f"  - Numeric: {tb['numeric_comparable_count']} (Match score=1: {tb['numeric_exact_match_count (score=1)']}, Mismatch score=0: {tb['numeric_mismatch_count (score=0)']})")
        print(f"  - Text: {tb['text_comparable_count']} (Score Sum: {tb['text_similarity_score_sum']}, Avg: {tb['text_similarity_score_average']})")
    print(f"Report successfully saved -> {out_path}")

if __name__ == "__main__":
    main()
