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
    base_dir = r"c:\json_data"
    
    # 統一命名規則に基づくファイルパス指定
    catalog_path = os.path.join(base_dir, "catalog_models_aircon_daikin.json")
    details_path = os.path.join(base_dir, "product_series_details_aircon_daikin_rx.json")
    
    hitachi_cat_path = os.path.join(base_dir, "catalog_models_aircon_hitachi.json")
    hitachi_det_path = os.path.join(base_dir, "product_series_details_aircon_hitachi_x.json")
    
    # ダイキンデータの読み込み
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog_daikin = json.load(f)
    with open(details_path, 'r', encoding='utf-8') as f:
        details_daikin = json.load(f)
        
    # 日立データの読み込み (存在する場合)
    catalog_hitachi = []
    details_hitachi = []
    if os.path.exists(hitachi_cat_path):
        with open(hitachi_cat_path, 'r', encoding='utf-8') as f:
            catalog_hitachi = json.load(f)
    if os.path.exists(hitachi_det_path):
        with open(hitachi_det_path, 'r', encoding='utf-8') as f:
            details_hitachi = json.load(f)

    # 1. カタログ一覧機能のマップ化 (型番 -> おすすめ機能集合)
    catalog_map = {}
    for item in catalog_daikin + catalog_hitachi:
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
    for item in details_daikin + details_hitachi:
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

    # 3. 機能別の比較評価
    evaluation_results = []
    all_keys = sorted(list(set(catalog_map.keys()) | set(details_map.keys())))
    
    total_models = len(all_keys)
    discrepancy_count = 0
    match_count = 0

    for m_key in all_keys:
        cat_info = catalog_map.get(m_key, {})
        det_info = details_map.get(m_key, {})
        
        raw_model = cat_info.get("raw_model") or det_info.get("raw_model") or m_key
        mfr = cat_info.get("manufacturer") or det_info.get("manufacturer") or "ダイキン"
        series = cat_info.get("series_name") or det_info.get("series_name") or ""
        
        cat_features = cat_info.get("recommended_features", set())
        det_functions = det_info.get("detail_functions", set())
        
        in_catalog_only = sorted(list(cat_features - det_functions))
        in_details_only = sorted(list(det_functions - cat_features))
        common_features = sorted(list(cat_features & det_functions))
        
        has_discrepancy = len(in_catalog_only) > 0 or len(in_details_only) > 0
        if has_discrepancy:
            discrepancy_count += 1
        else:
            match_count += 1

        evaluation_results.append({
            "manufacturer": mfr,
            "model_number": raw_model,
            "series_name": series,
            "has_discrepancy": has_discrepancy,
            "discrepancy_details": {
                "in_catalog_only_count": len(in_catalog_only),
                "in_catalog_only": in_catalog_only,
                "in_details_only_count": len(in_details_only),
                "in_details_only": in_details_only
            },
            "comparison_pair": {
                "catalog_recommended_features": sorted(list(cat_features)),
                "detail_functions": sorted(list(det_functions)),
                "common_features": common_features
            }
        })

    summary = {
        "total_evaluated_models": total_models,
        "matched_models_count": match_count,
        "discrepancy_models_count": discrepancy_count,
        "discrepancy_rate_percent": round((discrepancy_count / total_models) * 100, 2) if total_models > 0 else 0
    }

    output_payload = {
        "evaluation_summary": summary,
        "model_evaluations": evaluation_results
    }

    output_path = os.path.join(base_dir, "feature_discrepancy_evaluation.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)

    print(f"Successfully ran feature discrepancy evaluation across {total_models} models.")
    print(f"Summary: Matched={match_count}, Discrepancies={discrepancy_count} ({summary['discrepancy_rate_percent']}%)")
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    main()
