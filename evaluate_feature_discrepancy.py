import os
import json
import re

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

def main():
    base_dir = os.getcwd()
    
    # 統一命名規則に基づくファイルパス指定 (ダイキン / 日立表記統一)
    daikin_cat_path = os.path.join(base_dir, "catalog_models_aircon_daikin.json")
    daikin_det_path = os.path.join(base_dir, "product_series_details_aircon_daikin_rx.json")
    
    hitachi_cat_path = os.path.join(base_dir, "catalog_models_aircon_hitachi.json")
    hitachi_det_path = os.path.join(base_dir, "product_series_details_aircon_hitachi_x.json")

    # c:\json_data へのフォールバック対応
    if not os.path.exists(daikin_cat_path):
        base_dir = r"c:\json_data"
        daikin_cat_path = os.path.join(base_dir, "catalog_models_aircon_daikin.json")
        daikin_det_path = os.path.join(base_dir, "product_series_details_aircon_daikin_rx.json")
        hitachi_cat_path = os.path.join(base_dir, "catalog_models_aircon_hitachi.json")
        hitachi_det_path = os.path.join(base_dir, "product_series_details_aircon_hitachi_x.json")

    # ダイキンデータの読み込み
    cat_daikin = []
    det_daikin = []
    if os.path.exists(daikin_cat_path):
        with open(daikin_cat_path, 'r', encoding='utf-8') as f:
            cat_daikin = json.load(f)
    if os.path.exists(daikin_det_path):
        with open(daikin_det_path, 'r', encoding='utf-8') as f:
            det_daikin = json.load(f)
        
    # 日立データの読み込み
    cat_hitachi = []
    det_hitachi = []
    if os.path.exists(hitachi_cat_path):
        with open(hitachi_cat_path, 'r', encoding='utf-8') as f:
            cat_hitachi = json.load(f)
    if os.path.exists(hitachi_det_path):
        with open(hitachi_det_path, 'r', encoding='utf-8') as f:
            det_hitachi = json.load(f)

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
