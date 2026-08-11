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
    m = re.sub(r'\([A-Z]\)', '', m)
    m = re.sub(r'^RAS-XR', 'RAS-X', m)
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
    if isinstance(item.get("model_numbers"), list):
        for m in item["model_numbers"]:
            models.add(normalize_model_number(m))
    return models

# --- 3. 類似・関連項目の対応マップ定義 ---
FIELD_ALIAS_MAP = {
    "cooling.capacity_kw": ["cooling_capacity_kw", "detail_specs.cooling.capacity_kw", "cooling.rated_capacity_kw"],
    "heating.capacity_kw": ["heating_capacity_kw", "detail_specs.heating.capacity_kw", "heating.rated_capacity_kw"],
    "energy_saving.annual_power_consumption_kwh": ["annual_power_consumption_kwh", "annual_power_consumption_kwh.annual_total"],
    "energy_saving.apf": ["apf", "apf_value"],
    "indoor_unit.weight_kg": ["indoor_unit_weight_kg", "weight_kg.indoor"],
    "outdoor_unit.weight_kg": ["outdoor_unit_weight_kg", "weight_kg.outdoor"],
    "unique_selling_point": ["unique_selling_point"],
    "recommended_features": ["recommended_features", "functions", "main_features"],
    "category_description": ["category_description"],
    "copilot_plus_pc": ["copilot_plus_pc"],
    "made_in_japan": ["made_in_japan"],
    "weight_g": ["weight_g", "weight_kg", "weight"],
    "memory": ["memory"],
    "storage": ["storage"],
    "os": ["os"],
    "display": ["display"]
}

def find_target_field_and_value(target_item, detail_field_name):
    """
    商品一覧または仕様表のアイテム target_item から、detail_field_name に相当・類似するフィールドと値を探索
    """
    if not target_item:
        return None, None

    flat_target = flatten_dict(target_item)
    
    # 1. 完全一致
    if detail_field_name in flat_target:
        return detail_field_name, flat_target[detail_field_name]
    
    # 2. エイリアスマッチ
    aliases = FIELD_ALIAS_MAP.get(detail_field_name, [])
    for alias in aliases:
        if alias in flat_target:
            return alias, flat_target[alias]
        for tk, tv in flat_target.items():
            if normalize_key(alias) == normalize_key(tk):
                return tk, tv

    # 3. フィールド名の最後要素でのマッチ (例: capacity_kw)
    last_key = detail_field_name.split('.')[-1]
    for tk, tv in flat_target.items():
        if normalize_key(last_key) == normalize_key(tk.split('.')[-1]):
            return tk, tv

    return None, None

def evaluate_single_field(detail_field_name, detail_val, target_item, target_name):
    target_field, target_val = find_target_field_and_value(target_item, detail_field_name)
    
    if target_val is None:
        return None

    # 数値比較判定
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
                matched_cat_item = None
                for c_item in cat_list:
                    c_models = extract_model_numbers(c_item)
                    if (det_models and c_models and det_models & c_models) or (series_name and normalize_key(series_name) == normalize_key(c_item.get("series_name"))):
                        matched_cat_item = c_item
                        break

                # マッチする仕様表アイテムの探索
                matched_tech_item = None
                for t_item in tech_list:
                    t_models = extract_model_numbers(t_item)
                    if (det_models and t_models and det_models & t_models) or (series_name and normalize_key(series_name) == normalize_key(t_item.get("series_name"))):
                        matched_tech_item = t_item
                        break

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
                            if res["is_numeric_comparable"]:
                                numeric_comparable_count += 1
                                if res["score"] == 1:
                                    numeric_exact_match_count += 1
                                else:
                                    numeric_mismatch_count += 1
                            else:
                                text_comparable_count += 1

                    # 2. 仕様表 (technical_spec) との比較
                    if matched_tech_item:
                        res = evaluate_single_field(field_name, detail_val, matched_tech_item, "technical_spec")
                        if res:
                            item_evals.append(res)
                            total_comparisons += 1
                            if res["is_numeric_comparable"]:
                                numeric_comparable_count += 1
                                if res["score"] == 1:
                                    numeric_exact_match_count += 1
                                else:
                                    numeric_mismatch_count += 1
                            else:
                                text_comparable_count += 1

                evaluations.append({
                    "manufacturer": mfr_name,
                    "product_category": det_item.get("product_category", "エアコン" if cat == "aircon" else "ノートパソコン"),
                    "series_name": series_name,
                    "model_number": raw_model,
                    "field_evaluations_count": len(item_evals),
                    "detail_field_evaluations": item_evals
                })

    summary = {
        "total_evaluated_detail_items": len(evaluations),
        "total_field_comparisons": total_comparisons,
        "numeric_comparable_count": numeric_comparable_count,
        "numeric_exact_match_count (score=1)": numeric_exact_match_count,
        "numeric_mismatch_count (score=0)": numeric_mismatch_count,
        "text_comparable_count": text_comparable_count
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
    print(f"Report successfully saved -> {out_path}")

if __name__ == "__main__":
    main()
