import os
import sys
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

def evaluate_discrepancies():
    current_dir = os.getcwd()
    target_dir = r"c:\json_data"
    
    # 比較ソースファイルのパス
    daikin_cat_path = os.path.join(current_dir, "catalog_models.json")
    daikin_det_path = os.path.join(current_dir, "product_series_details_rx.json")
    hitachi_cat_path = os.path.join(current_dir, "catalog_models_hitachi.json")
    hitachi_det_path = os.path.join(current_dir, "product_series_details_hitachi_x.json")
    
    # ファイル読み込み
    with open(daikin_cat_path, 'r', encoding='utf-8') as f:
        daikin_cat = json.load(f)
    with open(daikin_det_path, 'r', encoding='utf-8') as f:
        daikin_det = json.load(f)
    with open(hitachi_cat_path, 'r', encoding='utf-8') as f:
        hitachi_cat = json.load(f)
    with open(hitachi_det_path, 'r', encoding='utf-8') as f:
        hitachi_det = json.load(f)
        
    catalog_models_map = {}
    details_models_map = {}
    
    # ダイキンデータマッピング
    for item in daikin_cat:
        key = f"DAIKIN_{normalize_model_number(item.get('model_number', ''))}"
        catalog_models_map[key] = {
            "manufacturer": "ダイキン",
            "model_number": item.get("model_number"),
            "base_model": normalize_model_number(item.get("model_number", "")),
            "features": item.get("recommended_features", {})
        }
        
    for item in daikin_det:
        key = f"DAIKIN_{normalize_model_number(item.get('model_number', ''))}"
        details_models_map[key] = {
            "manufacturer": "ダイキン",
            "model_number": item.get("model_number"),
            "base_model": normalize_model_number(item.get("model_number", "")),
            "functions": item.get("functions", {})
        }
        
    # 日立データマッピング
    for item in hitachi_cat:
        key = f"HITACHI_{normalize_model_number(item.get('model_number', ''))}"
        catalog_models_map[key] = {
            "manufacturer": "日立",
            "model_number": item.get("model_number"),
            "base_model": normalize_model_number(item.get("model_number", "")),
            "features": item.get("recommended_features", {})
        }
        
    for item in hitachi_det:
        key = f"HITACHI_{normalize_model_number(item.get('model_number', ''))}"
        details_models_map[key] = {
            "manufacturer": "日立",
            "model_number": item.get("model_number"),
            "base_model": normalize_model_number(item.get("model_number", "")),
            "functions": item.get("functions", {})
        }

    # 両方のソースに存在する型番キー
    target_keys = sorted(list(set(catalog_models_map.keys()) & set(details_models_map.keys())))
    
    evaluation_results = []
    total_models_evaluated = len(target_keys)
    discrepancy_models_count = 0
    
    for key in target_keys:
        cat_info = catalog_models_map[key]
        det_info = details_models_map[key]
        
        cat_feats = cat_info["features"] or {}
        det_funcs = det_info["functions"] or {}
        
        all_categories = sorted(list(set(cat_feats.keys()) | set(det_funcs.keys())))
        categories_eval = []
        model_has_discrepancy = False
        
        for category in all_categories:
            cat_list = sorted(list(set(cat_feats.get(category, []))))
            det_list = sorted(list(set(det_funcs.get(category, []))))
            
            cat_set = set(cat_list)
            det_set = set(det_list)
            
            missing_in_detail = sorted(list(cat_set - det_set))
            missing_in_catalog = sorted(list(det_set - cat_set))
            
            cat_has_discrepancy = (len(missing_in_detail) > 0) or (len(missing_in_catalog) > 0)
            if cat_has_discrepancy:
                model_has_discrepancy = True
                
            categories_eval.append({
                "category_name": category,
                "has_discrepancy": cat_has_discrepancy,
                "catalog_values": cat_list,
                "detail_values": det_list,
                "missing_in_detail": missing_in_detail,
                "missing_in_catalog": missing_in_catalog
            })
            
        if model_has_discrepancy:
            discrepancy_models_count += 1
            
        evaluation_results.append({
            "manufacturer": cat_info["manufacturer"],
            "base_model_number": cat_info["base_model"],
            "full_model_number_catalog": cat_info["model_number"],
            "full_model_number_detail": det_info["model_number"],
            "overall_has_discrepancy": model_has_discrepancy,
            "discrepant_category_count": sum(1 for c in categories_eval if c["has_discrepancy"]),
            "categories_eval": categories_eval
        })

    # カレントディレクトリへの保存
    output_filename = "feature_discrepancy_evaluation.json"
    output_path = os.path.join(current_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, ensure_ascii=False, indent=2)
        
    print(f"Saved evaluation result to {output_path}")
    
    # c:\json_data へのコピー保存
    if os.path.exists(target_dir):
        target_path = os.path.join(target_dir, output_filename)
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(evaluation_results, f, ensure_ascii=False, indent=2)
        print(f"Saved copy to {target_path}")

    print("\n--- 評価サマリー ---")
    print(f"総評価対象モデル数: {total_models_evaluated}")
    print(f"機能齟齬検出モデル数: {discrepancy_models_count}")
    print(f"完全一致モデル数: {total_models_evaluated - discrepancy_models_count}")

if __name__ == "__main__":
    evaluate_discrepancies()
