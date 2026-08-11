import os
import json
import re
import glob

def normalize_model_number(model_str):
    if not model_str:
        return ''
    m = model_str.strip()
    if m.startswith('S') and '-' in m:
        m = m.split('-')[0].strip()
    m = re.sub(r'\([A-Z]\)', '', m)
    m = re.sub(r'^RAS-XR', 'RAS-X', m)
    return m

def extract_recommended_features_flat(rec_dict):
    features = set()
    if not rec_dict:
        return features
    for category, item_list in rec_dict.items():
        if isinstance(item_list, list):
            for item in item_list:
                features.add(item)
    return features

def extract_detail_functions_flat(func_dict):
    functions = set()
    if not func_dict:
        return functions
    for group_name, sub_groups in func_dict.items():
        if isinstance(sub_groups, dict):
            for sub_name, func_list in sub_groups.items():
                if isinstance(func_list, list):
                    for f in func_list:
                        functions.add(f)
        elif isinstance(sub_groups, list):
            for f in sub_groups:
                functions.add(f)
    return functions

def load_and_merge_json_files(base_dir, import_type, category, manufacturer):
    pattern = f"{import_type}_{category}_{manufacturer}*.json"
    search_path = os.path.join(base_dir, pattern)
    matched_files = glob.glob(search_path)
    
    target_dir = r"c:\json_data"
    if os.path.exists(target_dir):
        alt_search_path = os.path.join(target_dir, pattern)
        for fpath in glob.glob(alt_search_path):
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

def main():
    base_dir = os.getcwd()
    
    # 動的マルチファイルロード (エアコン)
    cat_daikin = load_and_merge_json_files(base_dir, "catalog_models", "aircon", "daikin")
    det_daikin = load_and_merge_json_files(base_dir, "product_series_details", "aircon", "daikin")
    
    cat_hitachi = load_and_merge_json_files(base_dir, "catalog_models", "aircon", "hitachi")
    det_hitachi = load_and_merge_json_files(base_dir, "product_series_details", "aircon", "hitachi")

    # 1. カタログ一覧機能のマップ化 (型番 -> おすすめ機能集合)
    catalog_map = {}
    for item in cat_daikin + cat_hitachi:
        raw_m = item.get("model_number", "")
        norm_m = normalize_model_number(raw_m)
        rec_feat = extract_recommended_features_flat(item.get("recommended_features", {}))
        m_key = f"{item.get('manufacturer', 'DAIKIN')}_{norm_m}"
        catalog_map[m_key] = {
            "raw_model": raw_m,
            "manufacturer": item.get("manufacturer", "ダイキン"),
            "series_name": item.get("series_name", ""),
            "recommended_features": rec_feat
        }

    # 2. 製品詳細機能のマップ化 (型番 -> 詳細機能集合)
    details_map = {}
    for item in det_daikin + det_hitachi:
        raw_m = item.get("model_number", "")
        norm_m = normalize_model_number(raw_m)
        det_func = extract_detail_functions_flat(item.get("functions", {}))
        m_key = f"{item.get('manufacturer', 'DAIKIN')}_{norm_m}"
        details_map[m_key] = {
            "raw_model": raw_m,
            "manufacturer": item.get("manufacturer", "ダイキン"),
            "series_name": item.get("series_name", ""),
            "detail_functions": det_func
        }

    # 3. 機能一覧と詳細の乖離判定評価
    evaluations = []
    all_keys = set(catalog_map.keys()) | set(details_map.keys())

    matched_count = 0
    discrepancy_count = 0

    for m_key in sorted(list(all_keys)):
        cat_info = catalog_map.get(m_key, {})
        det_info = details_map.get(m_key, {})

        raw_m = cat_info.get("raw_model") or det_info.get("raw_model", "")
        mfr = cat_info.get("manufacturer") or det_info.get("manufacturer", "")
        series = cat_info.get("series_name") or det_info.get("series_name", "")

        cat_feat = cat_info.get("recommended_features", set())
        det_func = det_info.get("detail_functions", set())

        in_cat_only = sorted(list(cat_feat - det_func))
        in_det_only = sorted(list(det_func - cat_feat))
        common = sorted(list(cat_feat & det_func))

        has_discrepancy = len(in_cat_only) > 0 or len(in_det_only) > 0

        if has_discrepancy:
            discrepancy_count += 1
        else:
            matched_count += 1

        evaluations.append({
            "manufacturer": mfr,
            "model_number": raw_m,
            "series_name": series,
            "has_discrepancy": has_discrepancy,
            "discrepancy_details": {
                "in_catalog_only_count": len(in_cat_only),
                "in_catalog_only": in_cat_only,
                "in_details_only_count": len(in_det_only),
                "in_details_only": in_det_only,
                "common_matched_count": len(common),
                "common_matched": common
            },
            "comparison_pair": {
                "catalog_recommended_features": sorted(list(cat_feat)),
                "details_functions": sorted(list(det_func))
            }
        })

    summary = {
        "total_evaluated_models": len(all_keys),
        "matched_models_count": matched_count,
        "discrepancy_models_count": discrepancy_count,
        "discrepancy_rate_percent": round((discrepancy_count / len(all_keys) * 100), 2) if all_keys else 0.0
    }

    result_report = {
        "evaluation_summary": summary,
        "model_evaluations": evaluations
    }

    out_path = os.path.join(os.getcwd(), "feature_discrepancy_evaluation.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result_report, f, ensure_ascii=False, indent=2)

    print(f"Feature discrepancy evaluation completed.")
    print(f"Total Models Evaluated: {summary['total_evaluated_models']}")
    print(f"Discrepancy Models Count: {summary['discrepancy_models_count']} ({summary['discrepancy_rate_percent']}%)")
    print(f"Evaluation report saved -> {out_path}")

if __name__ == "__main__":
    main()
