import fs from 'fs';
import path from 'path';

// 文字 N-gram (2-gram) ベクトルの生成とコサイン類似度 (Cosine Similarity) の算出関数
function getNGrams(str) {
    const text = String(str).replace(/\s+/g, '').toLowerCase();
    const ngrams = {};
    for (let i = 0; i < text.length - 1; i++) {
        const gram = text.substring(i, i + 2);
        ngrams[gram] = (ngrams[gram] || 0) + 1;
    }
    return ngrams;
}

function calculateCosineSimilarity(str1, str2) {
    if (!str1 || !str2) return 0.0;
    const s1 = String(str1);
    const s2 = String(str2);
    if (s1 === s2) return 1.0;

    const vec1 = getNGrams(s1);
    const vec2 = getNGrams(s2);

    let dotProduct = 0;
    for (const key in vec1) {
        if (vec2[key]) {
            dotProduct += vec1[key] * vec2[key];
        }
    }

    let norm1 = 0;
    for (const key in vec1) {
        norm1 += vec1[key] * vec1[key];
    }
    norm1 = Math.sqrt(norm1);

    let norm2 = 0;
    for (const key in vec2) {
        norm2 += vec2[key] * vec2[key];
    }
    norm2 = Math.sqrt(norm2);

    if (norm1 === 0 || norm2 === 0) return 0.0;
    const similarity = dotProduct / (norm1 * norm2);
    return Math.round(similarity * 1000) / 1000; // 小数点第3位に丸め
}

// 配列内のテキスト値ペアごとのコサイン類似度スコアリストを計算
function getSimilarityScoresForList(valuesList) {
    if (!valuesList || valuesList.length <= 1) {
        return [1.0];
    }
    const scores = [];
    for (let i = 0; i < valuesList.length - 1; i++) {
        for (let j = i + 1; j < valuesList.length; j++) {
            const v1 = typeof valuesList[i] === 'object' ? JSON.stringify(valuesList[i]) : valuesList[i];
            const v2 = typeof valuesList[j] === 'object' ? JSON.stringify(valuesList[j]) : valuesList[j];
            scores.push(calculateCosineSimilarity(v1, v2));
        }
    }
    return scores;
}

// 型番の正規化関数 (例: "S22ATRS-W(-C)" -> "S22ATRS", "S40ATRS(P)(V)" -> "S40ATRS")
function normalizeModelNumber(modelStr) {
    if (!modelStr) return '';
    let cleaned = modelStr.split('-')[0].trim();
    cleaned = cleaned.replace(/\([A-Z]\)/g, '');
    return cleaned;
}

function main() {
    const catalogPath = path.join(process.cwd(), 'catalog_models.json');
    const detailsPath = path.join(process.cwd(), 'product_series_details_rx.json');
    const techPath = path.join(process.cwd(), 'technical_specifications.json');

    console.log('Loading 3 JSON files...');
    const catalogData = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
    const detailsData = JSON.parse(fs.readFileSync(detailsPath, 'utf8'));
    const techData = JSON.parse(fs.readFileSync(techPath, 'utf8'));

    const mergedMap = new Map();

    // 1. catalog_models.json の取り込み
    for (const item of catalogData) {
        const baseKey = normalizeModelNumber(item.model_number);
        if (!mergedMap.has(baseKey)) {
            mergedMap.set(baseKey, {
                base_model_number: baseKey,
                full_model_numbers: new Set([item.model_number]),
                series_name: item.series_name,
                series_nickname: item.series_nickname,
                model_year: item.model_year,
                applicable_room_size: item.applicable_room_size,
                unique_selling_point_sources: [item.unique_selling_point],
                price_sources: [{ source: 'catalog_models', ...item.price }],
                recommended_features: item.recommended_features
            });
        } else {
            const entry = mergedMap.get(baseKey);
            entry.full_model_numbers.add(item.model_number);
            entry.unique_selling_point_sources.push(item.unique_selling_point);
            entry.price_sources.push({ source: 'catalog_models', ...item.price });
        }
    }

    // 2. product_series_details_rx.json の統合
    for (const item of detailsData) {
        const baseKey = normalizeModelNumber(item.model_number);
        if (mergedMap.has(baseKey)) {
            const entry = mergedMap.get(baseKey);
            entry.full_model_numbers.add(item.model_number);
            if (item.unique_selling_point) {
                entry.unique_selling_point_sources.push(item.unique_selling_point);
            }
            if (item.price_total) {
                entry.price_sources.push({ source: 'product_series_details', ...item.price_total });
            }
            entry.indoor_unit = item.indoor_unit;
            entry.outdoor_unit = item.outdoor_unit;
            entry.power_supply_detail = item.power_supply;
            entry.piping_detail = item.piping;
            entry.dimensions_mm = item.dimensions_mm;
            entry.detail_specs = item.specs;
            entry.detail_functions = item.functions;
            entry.color_variations = item.color_variations;
            entry.recommendation_tags = item.recommendation_tags;
        } else {
            // 新規作成
            mergedMap.set(baseKey, {
                base_model_number: baseKey,
                full_model_numbers: new Set([item.model_number]),
                series_name: item.series_name,
                series_nickname: item.series_nickname,
                model_year: item.model_year,
                unique_selling_point_sources: [item.unique_selling_point],
                price_sources: [{ source: 'product_series_details', ...item.price_total }],
                indoor_unit: item.indoor_unit,
                outdoor_unit: item.outdoor_unit,
                power_supply_detail: item.power_supply,
                piping_detail: item.piping,
                dimensions_mm: item.dimensions_mm,
                detail_specs: item.specs,
                detail_functions: item.functions,
                color_variations: item.color_variations,
                recommendation_tags: item.recommendation_tags
            });
        }
    }

    // 3. technical_specifications.json の統合
    for (const item of techData) {
        const baseKey = normalizeModelNumber(item.model_number);
        if (mergedMap.has(baseKey)) {
            const entry = mergedMap.get(baseKey);
            entry.full_model_numbers.add(item.model_number);
            entry.technical_specifications = {
                catalog_page: item.catalog_page,
                indoor_unit_model: item.indoor_unit_model,
                outdoor_unit_model: item.outdoor_unit_model,
                power_supply: item.power_supply,
                heating: item.heating,
                cooling: item.cooling,
                starting_current_a: item.starting_current_a,
                compressor_output_w: item.compressor_output_w,
                power_plug: item.power_plug,
                connection_cores: item.connection_cores,
                weight_kg: item.weight_kg,
                piping_diameter_mm: item.piping_diameter_mm,
                annual_power_consumption_kwh: item.annual_power_consumption_kwh,
                apf: item.apf,
                refrigerant: item.refrigerant
            };
        }
    }

    // 4. フラット JSON 配列の作成とコサイン類似度スコアリング
    const mergedList = [];

    for (const [baseKey, entry] of mergedMap.entries()) {
        const uspValues = Array.from(new Set(entry.unique_selling_point_sources.filter(Boolean)));
        const uspScores = getSimilarityScoresForList(uspValues);

        const priceValues = entry.price_sources;
        const priceScores = getSimilarityScoresForList(priceValues);

        mergedList.push({
            base_model_number: entry.base_model_number,
            full_model_numbers: Array.from(entry.full_model_numbers),
            series_name: entry.series_name,
            series_nickname: entry.series_nickname || null,
            model_year: entry.model_year || "2026年モデル",
            applicable_room_size: entry.applicable_room_size || null,
            
            // コサイン類似度スコアリング項目: USP
            unique_selling_point: {
                values: uspValues,
                cosine_similarity_scores: uspScores
            },

            // コサイン類似度スコアリング項目: 価格表記
            price_details: {
                values: priceValues,
                cosine_similarity_scores: priceScores
            },

            indoor_unit: entry.indoor_unit || null,
            outdoor_unit: entry.outdoor_unit || null,
            dimensions_mm: entry.dimensions_mm || null,
            power_supply_detail: entry.power_supply_detail || null,
            piping_detail: entry.piping_detail || null,
            color_variations: entry.color_variations || [],
            recommendation_tags: entry.recommendation_tags || [],
            detail_specs: entry.detail_specs || null,
            technical_specifications: entry.technical_specifications || null,
            recommended_features: entry.recommended_features || null,
            detail_functions: entry.detail_functions || null
        });
    }

    const outputPath = path.join(process.cwd(), 'merged_aircon_models.json');
    fs.writeFileSync(outputPath, JSON.stringify(mergedList, null, 2), 'utf8');
    console.log(`Successfully merged ${mergedList.length} unique model families into ${outputPath}`);
}

main();
