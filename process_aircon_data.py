import os
import sys
import json
import re
import csv
import math
import shutil
from collections import Counter

# --- 1. N-gram 文字ベクトルによるコサイン類似度算出関数 ---
def get_ngrams(text):
    cleaned = re.sub(r'\s+', '', str(text)).lower()
    if len(cleaned) < 2:
        return Counter([cleaned])
    return Counter([cleaned[i:i+2] for i in range(len(cleaned) - 1)])

def calculate_cosine_similarity(str1, str2):
    if str1 is None or str2 is None:
        return 0.0
    s1, s2 = str(str1), str(str2)
    if s1 == s2:
        return 1.0
    
    vec1 = get_ngrams(s1)
    vec2 = get_ngrams(s2)
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[x] * vec2[x] for x in intersection)
    
    norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return round(dot_product / (norm1 * norm2), 3)

def get_similarity_scores_for_list(val_list):
    if not val_list or len(val_list) <= 1:
        return [1.0]
    scores = []
    for i in range(len(val_list) - 1):
        for j in range(i + 1, len(val_list)):
            v1 = json.dumps(val_list[i], ensure_ascii=False) if isinstance(val_list[i], dict) else str(val_list[i])
            v2 = json.dumps(val_list[j], ensure_ascii=False) if isinstance(val_list[j], dict) else str(val_list[j])
            scores.append(calculate_cosine_similarity(v1, v2))
    return scores

# --- 2. 型番の正規化関数 (ダイキン: S22ATRS-W(-C) -> S22ATRS, 日立: RAS-XR2226S -> RAS-X2226S) ---
def normalize_model_number(model_str):
    if not model_str:
        return ''
    m = model_str.strip()
    if m.startswith('S') and '-' in m:
        m = m.split('-')[0].strip()
    m = re.sub(r'\([A-Z]\)', '', m)
    m = re.sub(r'^RAS-XR', 'RAS-X', m)
    return m

def get_heating_power(item):
    if item.get("detail_specs") and item["detail_specs"].get("heating"):
        return item["detail_specs"]["heating"].get("power_w", "")
    if item.get("technical_specifications") and item["technical_specifications"].get("heating"):
        h = item["technical_specifications"]["heating"]
        if "rated_power_w" in h:
            return h["rated_power_w"]
        if "electrical_properties" in h and "max_power_w" in h["electrical_properties"]:
            return h["electrical_properties"]["max_power_w"]
    return ""

def get_cooling_power(item):
    if item.get("detail_specs") and item["detail_specs"].get("cooling"):
        return item["detail_specs"]["cooling"].get("power_w", "")
    if item.get("technical_specifications") and item["technical_specifications"].get("cooling"):
        c = item["technical_specifications"]["cooling"]
        if "rated_power_w" in c:
            return c["rated_power_w"]
        if "electrical_properties" in c and "max_power_w" in c["electrical_properties"]:
            return c["electrical_properties"]["max_power_w"]
    return ""

def main():
    target_dir = r"c:\json_data"
    current_dir = os.getcwd()
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"Created directory: {target_dir}")
    
    # コピー対象 JSON ファイル群 (新統一命名規則準拠)
    json_files = [
        "catalog_models_aircon_daikin.json",
        "product_series_details_aircon_daikin_rx.json",
        "technical_spec_aircon_daikin.json",
        "catalog_models_aircon_hitachi.json",
        "product_series_details_aircon_hitachi_x.json",
        "technical_spec_aircon_hitachi.json",
        "catalog_models_pc_vaio.json",
        "product_series_details_pc_vaio_sx14r.json",
        "technical_spec_pc_vaio.json",
        "technical_spec_pc_fujitsu.json",
        "catalog_models_pc_fujitsu.json",
        "product_series_details_pc_fujitsu_ua-k1_ux-k3.json"
    ]
    
    for filename in json_files:
        src = os.path.join(current_dir, filename)
        dst = os.path.join(target_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {filename} -> {dst}")

    # エアコンデータの読み込み (新命名規則)
    path_catalog = os.path.join(target_dir, "catalog_models_aircon_daikin.json")
    path_details = os.path.join(target_dir, "product_series_details_aircon_daikin_rx.json")
    path_tech = os.path.join(target_dir, "technical_spec_aircon_daikin.json")
    path_hitachi_cat = os.path.join(target_dir, "catalog_models_aircon_hitachi.json")
    path_hitachi_det = os.path.join(target_dir, "product_series_details_aircon_hitachi_x.json")
    path_hitachi_tech = os.path.join(target_dir, "technical_spec_aircon_hitachi.json")
    
    with open(path_catalog, 'r', encoding='utf-8') as f:
        catalog_daikin = json.load(f)
    with open(path_details, 'r', encoding='utf-8') as f:
        details_daikin = json.load(f)
    with open(path_tech, 'r', encoding='utf-8') as f:
        tech_daikin = json.load(f)
    with open(path_hitachi_cat, 'r', encoding='utf-8') as f:
        catalog_hitachi = json.load(f)
    with open(path_hitachi_det, 'r', encoding='utf-8') as f:
        details_hitachi_x = json.load(f)
    with open(path_hitachi_tech, 'r', encoding='utf-8') as f:
        tech_hitachi = json.load(f)
        
    merged_map = {}
    
    # --- A. ダイキン catalog_models_aircon_daikin.json の統合 ---
    for item in catalog_daikin:
        base_key = f"DAIKIN_{normalize_model_number(item.get('model_number', ''))}"
        if base_key not in merged_map:
            merged_map[base_key] = {
                "manufacturer": "ダイキン",
                "product_category": "壁掛形ルームエアコン",
                "brand_name": item.get("series_nickname") or "ダイキン エアコン",
                "base_model_number": normalize_model_number(item.get("model_number", "")),
                "full_model_numbers": set([item["model_number"]]),
                "series_name": item.get("series_name"),
                "series_nickname": item.get("series_nickname"),
                "model_year": item.get("model_year"),
                "applicable_room_size": item.get("applicable_room_size"),
                "unique_selling_point_sources": [item.get("unique_selling_point")],
                "price_sources": [{"source": "catalog_models_aircon_daikin", **item.get("price", {})}],
                "recommended_features": item.get("recommended_features")
            }
        else:
            entry = merged_map[base_key]
            entry["full_model_numbers"].add(item["model_number"])
            if item.get("unique_selling_point"):
                entry["unique_selling_point_sources"].append(item.get("unique_selling_point"))
            if item.get("price"):
                entry["price_sources"].append({"source": "catalog_models_aircon_daikin", **item.get("price")})
                
    # --- B. ダイキン product_series_details_aircon_daikin_rx.json の統合 ---
    for item in details_daikin:
        base_key = f"DAIKIN_{normalize_model_number(item.get('model_number', ''))}"
        if base_key in merged_map:
            entry = merged_map[base_key]
            entry["full_model_numbers"].add(item["model_number"])
            if item.get("unique_selling_point"):
                entry["unique_selling_point_sources"].append(item.get("unique_selling_point"))
            if item.get("price_total"):
                entry["price_sources"].append({"source": "product_series_details_aircon_daikin_rx", **item.get("price_total")})
            entry["indoor_unit"] = item.get("indoor_unit")
            entry["outdoor_unit"] = item.get("outdoor_unit")
            entry["power_supply_detail"] = item.get("power_supply")
            entry["piping_detail"] = item.get("piping")
            entry["dimensions_mm"] = item.get("dimensions_mm")
            entry["detail_specs"] = item.get("specs")
            entry["detail_functions"] = item.get("functions")
            entry["color_variations"] = item.get("color_variations")
            entry["recommendation_tags"] = item.get("recommendation_tags")

    # --- C. ダイキン technical_spec_aircon_daikin_.json の統合 ---
    for item in tech_daikin:
        base_key = f"DAIKIN_{normalize_model_number(item.get('model_number', ''))}"
        if base_key in merged_map:
            entry = merged_map[base_key]
            entry["full_model_numbers"].add(item["model_number"])
            entry["technical_specifications"] = item

    # --- D. 日立 catalog_models_aircon_hitachi.json の統合 ---
    for item in catalog_hitachi:
        base_key = f"HITACHI_{normalize_model_number(item.get('model_number', ''))}"
        if base_key not in merged_map:
            merged_map[base_key] = {
                "manufacturer": "日立",
                "product_category": "壁掛形ルームエアコン",
                "brand_name": item.get("brand_name", "白くまくん"),
                "base_model_number": normalize_model_number(item.get("model_number", "")),
                "full_model_numbers": set([item["model_number"]]),
                "series_name": item.get("series_name"),
                "series_nickname": item.get("series_nickname"),
                "model_year": item.get("model_year"),
                "applicable_room_size": item.get("applicable_room_size"),
                "unique_selling_point_sources": [item.get("unique_selling_point")],
                "price_sources": [{"source": "catalog_models_aircon_hitachi", **item.get("price", {})}],
                "recommended_features": item.get("recommended_features")
            }

    # --- E. 日立 product_series_details_aircon_hitachi_x.json の統合 ---
    for item in details_hitachi_x:
        base_key = f"HITACHI_{normalize_model_number(item.get('model_number', ''))}"
        if base_key in merged_map:
            entry = merged_map[base_key]
            entry["full_model_numbers"].add(item["model_number"])
            if item.get("unique_selling_point"):
                entry["unique_selling_point_sources"].append(item.get("unique_selling_point"))
            if item.get("price_total"):
                entry["price_sources"].append({"source": "product_series_details_aircon_hitachi_x", **item.get("price_total")})
            entry["indoor_unit"] = item.get("indoor_unit")
            entry["outdoor_unit"] = item.get("outdoor_unit")
            entry["power_supply_detail"] = item.get("power_supply")
            entry["piping_detail"] = item.get("piping")
            entry["dimensions_mm"] = item.get("dimensions_mm")
            entry["detail_specs"] = item.get("specs")
            entry["detail_functions"] = item.get("functions")
            entry["color_variations"] = item.get("color_variations")
            entry["recommendation_tags"] = item.get("recommendation_tags")

    # --- F. 日立 technical_spec_aircon__hitachi.json の統合 ---
    for item in tech_hitachi:
        base_key = f"HITACHI_{normalize_model_number(item.get('model_number', ''))}"
        if base_key in merged_map:
            entry = merged_map[base_key]
            entry["full_model_numbers"].add(item["model_number"])
            entry["technical_specifications"] = item
        else:
            merged_map[base_key] = {
                "manufacturer": "日立",
                "product_category": "壁掛形ルームエアコン",
                "brand_name": "白くまくん",
                "base_model_number": normalize_model_number(item.get("model_number", "")),
                "full_model_numbers": set([item["model_number"]]),
                "series_name": item.get("series_name", "白くまくん"),
                "series_nickname": "白くまくん",
                "model_year": "2026年モデル",
                "technical_specifications": item
            }

    # --- G. 結合フラット JSON の作成 & コサイン類似度スコアリング ---
    merged_list = []
    for base_key, entry in merged_map.items():
        usp_values = list(set([x for x in entry.get("unique_selling_point_sources", []) if x]))
        usp_scores = get_similarity_scores_for_list(usp_values)
        
        price_values = entry.get("price_sources", [])
        price_scores = get_similarity_scores_for_list(price_values)
        
        merged_list.append({
            "manufacturer": entry["manufacturer"],
            "product_category": entry["product_category"],
            "brand_name": entry["brand_name"],
            "base_model_number": entry["base_model_number"],
            "full_model_numbers": list(entry["full_model_numbers"]),
            "series_name": entry.get("series_name"),
            "series_nickname": entry.get("series_nickname"),
            "model_year": entry.get("model_year", "2026年モデル"),
            "applicable_room_size": entry.get("applicable_room_size"),
            
            "unique_selling_point": {
                "values": usp_values,
                "cosine_similarity_scores": usp_scores
            },
            "price_details": {
                "values": price_values,
                "cosine_similarity_scores": price_scores
            },
            
            "indoor_unit": entry.get("indoor_unit"),
            "outdoor_unit": entry.get("outdoor_unit"),
            "dimensions_mm": entry.get("dimensions_mm"),
            "power_supply_detail": entry.get("power_supply_detail"),
            "piping_detail": entry.get("piping_detail"),
            "color_variations": entry.get("color_variations", []),
            "recommendation_tags": entry.get("recommendation_tags", []),
            "detail_specs": entry.get("detail_specs"),
            "technical_specifications": entry.get("technical_specifications"),
            "recommended_features": entry.get("recommended_features"),
            "detail_functions": entry.get("detail_functions")
        })

    output_json_path = os.path.join(target_dir, "merged_aircon_models.json")
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved multi-manufacturer merged JSON -> {output_json_path} (Total: {len(merged_list)} models)")

    # --- H. CSV ファイルの出力 (全37列 / BOM付き UTF-8: utf-8-sig) ---
    headers = [
        "メーカー名", "製品カテゴリー", "ブランド名", "ベース型番", "全表記型番", "シリーズ名", "愛称", "年式", "畳数目安", "冷房能力(kW)",
        "ユニークセリングポイント (USP)", "USPコサイン類似度スコア", "税込価格 (円)", "税抜価格 (円)", "価格コサイン類似度スコア",
        "室内機型番", "室内機質量 (kg)", "室内機寸法_幅 (mm)", "室内機寸法_高さ (mm)", "室内機寸法_奥行 (mm)",
        "室外機型番", "室外機質量 (kg)", "室外機寸法_幅 (mm)", "室外機寸法_高さ (mm)", "室外機寸法_奥行 (mm)",
        "電源規格", "配管径_液 (mm)", "配管径_ガス (mm)", "暖房能力 (kW)", "暖房消費電力 (W)", "冷房能力 (kW)", "冷房消費電力 (W)",
        "年間消費電力量 (kWh)", "APF (通年エネルギー消費効率)", "冷媒種類", "冷媒封入量 (kg)", "GWP", "おもなおすすめ機能"
    ]
    
    rows = [headers]
    
    for item in merged_list:
        full_models = "; ".join(item.get("full_model_numbers", []))
        room_size = item["applicable_room_size"]["tatami"] if item.get("applicable_room_size") else ""
        cap_kw = item["applicable_room_size"]["capacity_kw"] if item.get("applicable_room_size") else ""
        
        usp_vals = " | ".join(item["unique_selling_point"]["values"]) if item.get("unique_selling_point") else ""
        usp_scrs = ", ".join(map(str, item["unique_selling_point"]["cosine_similarity_scores"])) if item.get("unique_selling_point") else ""
        
        price_inc, price_exc, price_scrs = "", "", ""
        if item.get("price_details") and item["price_details"].get("values"):
            fp = item["price_details"]["values"][0]
            price_inc = "オープン価格" if fp.get("is_open_price") else fp.get("tax_included_yen", "")
            price_exc = "オープン価格" if fp.get("is_open_price") else fp.get("tax_excluded_yen", "")
            price_scrs = ", ".join(map(str, item["price_details"].get("cosine_similarity_scores", [])))

        indoor_m = item["indoor_unit"]["model_number"] if item.get("indoor_unit") else (item["technical_specifications"]["indoor_unit_model"] if item.get("technical_specifications") else "")
        indoor_w = item["indoor_unit"]["weight_kg"] if item.get("indoor_unit") and item["indoor_unit"].get("weight_kg") else (item["technical_specifications"]["weight_kg"]["indoor"] if item.get("technical_specifications") and item["technical_specifications"].get("weight_kg") else "")
        
        in_w = item["dimensions_mm"]["indoor"]["width"] if item.get("dimensions_mm") and item["dimensions_mm"].get("indoor") else ""
        in_h = item["dimensions_mm"]["indoor"]["height"] if item.get("dimensions_mm") and item["dimensions_mm"].get("indoor") else ""
        in_d = item["dimensions_mm"]["indoor"]["depth"] if item.get("dimensions_mm") and item["dimensions_mm"].get("indoor") else ""

        outdoor_m = item["outdoor_unit"]["model_number"] if item.get("outdoor_unit") else (item["technical_specifications"]["outdoor_unit_model"] if item.get("technical_specifications") else "")
        outdoor_w = item["outdoor_unit"]["weight_kg"] if item.get("outdoor_unit") and item["outdoor_unit"].get("weight_kg") else (item["technical_specifications"]["weight_kg"]["outdoor"] if item.get("technical_specifications") and item["technical_specifications"].get("weight_kg") else "")
        
        out_w = item["dimensions_mm"]["outdoor"]["width"] if item.get("dimensions_mm") and item["dimensions_mm"].get("outdoor") else ""
        out_h = item["dimensions_mm"]["outdoor"]["height"] if item.get("dimensions_mm") and item["dimensions_mm"].get("outdoor") else ""
        out_d = item["dimensions_mm"]["outdoor"]["depth"] if item.get("dimensions_mm") and item["dimensions_mm"].get("outdoor") else ""

        pwr = f"{item['power_supply_detail']['phase']}{item['power_supply_detail']['voltage_v']}V {item['power_supply_detail']['current_a']}A" if item.get("power_supply_detail") else (item["technical_specifications"]["power_supply"] if item.get("technical_specifications") else "")
        
        pipe_l = item["piping_detail"]["liquid_mm"] if item.get("piping_detail") else (item["technical_specifications"]["piping_diameter_mm"]["liquid"] if item.get("technical_specifications") and item["technical_specifications"].get("piping_diameter_mm") else "")
        pipe_g = item["piping_detail"]["gas_mm"] if item.get("piping_detail") else (item["technical_specifications"]["piping_diameter_mm"]["gas"] if item.get("technical_specifications") and item["technical_specifications"].get("piping_diameter_mm") else "")

        heat_kw = item["detail_specs"]["heating"]["capacity_kw"] if item.get("detail_specs") and item["detail_specs"].get("heating") else (item["technical_specifications"]["heating"]["rated_capacity_kw"] if item.get("technical_specifications") and item["technical_specifications"].get("heating") else "")
        heat_w = get_heating_power(item)

        cool_kw = item["detail_specs"]["cooling"]["capacity_kw"] if item.get("detail_specs") and item["detail_specs"].get("cooling") else (item["technical_specifications"]["cooling"]["rated_capacity_kw"] if item.get("technical_specifications") and item["technical_specifications"].get("cooling") else "")
        cool_w = get_cooling_power(item)

        ann_kwh = item["detail_specs"]["energy_saving"]["annual_power_consumption_kwh"] if item.get("detail_specs") and item["detail_specs"].get("energy_saving") else (item["technical_specifications"]["annual_power_consumption_kwh"]["annual_total"] if item.get("technical_specifications") and item["technical_specifications"].get("annual_power_consumption_kwh") else "")
        apf_v = item["detail_specs"]["energy_saving"]["apf"] if item.get("detail_specs") and item["detail_specs"].get("energy_saving") else (item["technical_specifications"]["apf"] if item.get("technical_specifications") else "")

        ref_t = item["technical_specifications"]["refrigerant"]["type"] if item.get("technical_specifications") and item["technical_specifications"].get("refrigerant") else "R32"
        ref_kg = item["technical_specifications"]["refrigerant"]["charge_amount_kg"] if item.get("technical_specifications") and item["technical_specifications"].get("refrigerant") else ""
        gwp_v = item["technical_specifications"]["refrigerant"]["gwp"] if item.get("technical_specifications") and item["technical_specifications"].get("gwp") else 675

        feat_list = []
        if item.get("recommended_features"):
            for c, arr in item["recommended_features"].items():
                if isinstance(arr, list):
                    feat_list.extend(arr)
        if item.get("detail_functions"):
            for c, arr in item["detail_functions"].items():
                if isinstance(arr, list):
                    feat_list.extend(arr)
        feat_str = " / ".join(list(set(feat_list)))

        rows.append([
            item["manufacturer"], item["product_category"], item.get("brand_name", ""),
            item["base_model_number"], full_models, item.get("series_name", ""), item.get("series_nickname", ""),
            item.get("model_year", ""), room_size, cap_kw, usp_vals, usp_scrs, price_inc, price_exc, price_scrs,
            indoor_m, indoor_w, in_w, in_h, in_d, outdoor_m, outdoor_w, out_w, out_h, out_d,
            pwr, pipe_l, pipe_g, heat_kw, heat_w, cool_kw, cool_w, ann_kwh, apf_v, ref_t, ref_kg, gwp_v, feat_str
        ])

    output_csv_path = os.path.join(target_dir, "merged_aircon_models.csv")
    with open(output_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
        
    print(f"Successfully saved multi-manufacturer CSV -> {output_csv_path} (Total: {len(rows)-1} rows)")

if __name__ == "__main__":
    main()
