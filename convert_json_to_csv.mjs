import fs from 'fs';
import path from 'path';

function escapeCsvField(val) {
    if (val === null || val === undefined) return '""';
    if (typeof val === 'object') {
        val = JSON.stringify(val);
    }
    const str = String(val).replace(/"/g, '""');
    return `"${str}"`;
}

function main() {
    const jsonPath = path.join(process.cwd(), 'merged_aircon_models.json');
    console.log('Loading merged_aircon_models.json...');
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

    const headers = [
        "ベース型番",
        "全表記型番",
        "シリーズ名",
        "愛称",
        "年式",
        "畳数目安",
        "冷房能力(kW)",
        "ユニークセリングポイント (USP)",
        "USPコサイン類似度スコア",
        "税込価格 (円)",
        "税抜価格 (円)",
        "価格コサイン類似度スコア",
        "室内機型番",
        "室内機質量 (kg)",
        "室内機寸法_幅 (mm)",
        "室内機寸法_高さ (mm)",
        "室内機寸法_奥行 (mm)",
        "室外機型番",
        "室外機質量 (kg)",
        "室外機寸法_幅 (mm)",
        "室外機寸法_高さ (mm)",
        "室外機寸法_奥行 (mm)",
        "電源規格",
        "配管径_液 (mm)",
        "配管径_ガス (mm)",
        "暖房能力 (kW)",
        "暖房消費電力 (W)",
        "冷房能力 (kW)",
        "冷房消費電力 (W)",
        "年間消費電力量 (kWh)",
        "APF (通年エネルギー消費効率)",
        "冷媒種類",
        "冷媒封入量 (kg)",
        "GWP",
        "おもなおすすめ機能"
    ];

    const rows = [headers.map(escapeCsvField).join(',')];

    for (const item of data) {
        const fullModels = (item.full_model_numbers || []).join('; ');
        const roomSize = item.applicable_room_size ? item.applicable_room_size.tatami : '';
        const capKw = item.applicable_room_size ? item.applicable_room_size.capacity_kw : '';
        
        const uspValues = item.unique_selling_point && item.unique_selling_point.values ? item.unique_selling_point.values.join(' | ') : '';
        const uspScores = item.unique_selling_point && item.unique_selling_point.cosine_similarity_scores ? item.unique_selling_point.cosine_similarity_scores.join(', ') : '';

        let priceTaxInc = '';
        let priceTaxExc = '';
        let priceScores = '';
        if (item.price_details && item.price_details.values && item.price_details.values.length > 0) {
            const firstPrice = item.price_details.values[0];
            priceTaxInc = firstPrice.is_open_price ? 'オープン価格' : (firstPrice.tax_included_yen || '');
            priceTaxExc = firstPrice.is_open_price ? 'オープン価格' : (firstPrice.tax_excluded_yen || '');
            priceScores = (item.price_details.cosine_similarity_scores || []).join(', ');
        }

        const indoorModel = item.indoor_unit ? item.indoor_unit.model_number : (item.technical_specifications ? item.technical_specifications.indoor_unit_model : '');
        const indoorWeight = item.indoor_unit ? item.indoor_unit.weight_kg : (item.technical_specifications && item.technical_specifications.weight_kg ? item.technical_specifications.weight_kg.indoor : '');
        
        const indoorW = item.dimensions_mm && item.dimensions_mm.indoor ? item.dimensions_mm.indoor.width : '';
        const indoorH = item.dimensions_mm && item.dimensions_mm.indoor ? item.dimensions_mm.indoor.height : '';
        const indoorD = item.dimensions_mm && item.dimensions_mm.indoor ? item.dimensions_mm.indoor.depth : '';

        const outdoorModel = item.outdoor_unit ? item.outdoor_unit.model_number : (item.technical_specifications ? item.technical_specifications.outdoor_unit_model : '');
        const outdoorWeight = item.outdoor_unit ? item.outdoor_unit.weight_kg : (item.technical_specifications && item.technical_specifications.weight_kg ? item.technical_specifications.weight_kg.outdoor : '');
        
        const outdoorW = item.dimensions_mm && item.dimensions_mm.outdoor ? item.dimensions_mm.outdoor.width : '';
        const outdoorH = item.dimensions_mm && item.dimensions_mm.outdoor ? item.dimensions_mm.outdoor.height : '';
        const outdoorD = item.dimensions_mm && item.dimensions_mm.outdoor ? item.dimensions_mm.outdoor.depth : '';

        const pwrSupply = item.power_supply_detail ? `${item.power_supply_detail.phase}${item.power_supply_detail.voltage_v}V ${item.power_supply_detail.current_a}A` : (item.technical_specifications ? item.technical_specifications.power_supply : '');
        
        const pipeLiq = item.piping_detail ? item.piping_detail.liquid_mm : (item.technical_specifications && item.technical_specifications.piping_diameter_mm ? item.technical_specifications.piping_diameter_mm.liquid : '');
        const pipeGas = item.piping_detail ? item.piping_detail.gas_mm : (item.technical_specifications && item.technical_specifications.piping_diameter_mm ? item.technical_specifications.piping_diameter_mm.gas : '');

        const heatKw = item.detail_specs && item.detail_specs.heating ? item.detail_specs.heating.capacity_kw : (item.technical_specifications && item.technical_specifications.heating ? item.technical_specifications.heating.rated_capacity_kw : '');
        const heatW = item.detail_specs && item.detail_specs.heating ? item.detail_specs.heating.power_w : (item.technical_specifications && item.technical_specifications.heating && item.technical_specifications.heating.electrical_properties ? item.technical_specifications.heating.electrical_properties.max_power_w : '');

        const coolKw = item.detail_specs && item.detail_specs.cooling ? item.detail_specs.cooling.capacity_kw : (item.technical_specifications && item.technical_specifications.cooling ? item.technical_specifications.cooling.rated_capacity_kw : '');
        const coolW = item.detail_specs && item.detail_specs.cooling ? item.detail_specs.cooling.power_w : (item.technical_specifications && item.technical_specifications.cooling && item.technical_specifications.cooling.electrical_properties ? item.technical_specifications.cooling.electrical_properties.max_power_w : '');

        const annualKwh = item.detail_specs && item.detail_specs.energy_saving ? item.detail_specs.energy_saving.annual_power_consumption_kwh : (item.technical_specifications && item.technical_specifications.annual_power_consumption_kwh ? item.technical_specifications.annual_power_consumption_kwh.annual_total : '');
        const apfVal = item.detail_specs && item.detail_specs.energy_saving ? item.detail_specs.energy_saving.apf : (item.technical_specifications ? item.technical_specifications.apf : '');

        const refType = item.technical_specifications && item.technical_specifications.refrigerant ? item.technical_specifications.refrigerant.type : 'R32';
        const refKg = item.technical_specifications && item.technical_specifications.refrigerant ? item.technical_specifications.refrigerant.charge_amount_kg : '';
        const gwpVal = item.technical_specifications && item.technical_specifications.refrigerant ? item.technical_specifications.refrigerant.gwp : 675;

        // おすすめ機能リスト
        let featuresList = [];
        if (item.recommended_features) {
            for (const cat in item.recommended_features) {
                if (Array.isArray(item.recommended_features[cat])) {
                    featuresList = featuresList.concat(item.recommended_features[cat]);
                }
            }
        }
        const featuresStr = Array.from(new Set(featuresList)).join(' / ');

        const row = [
            item.base_model_number,
            fullModels,
            item.series_name,
            item.series_nickname || '',
            item.model_year || '2026年モデル',
            roomSize,
            capKw,
            uspValues,
            uspScores,
            priceTaxInc,
            priceTaxExc,
            priceScores,
            indoorModel,
            indoorWeight,
            indoorW,
            indoorH,
            indoorD,
            outdoorModel,
            outdoorWeight,
            outdoorW,
            outdoorH,
            outdoorD,
            pwrSupply,
            pipeLiq,
            pipeGas,
            heatKw,
            heatW,
            coolKw,
            coolW,
            annualKwh,
            apfVal,
            refType,
            refKg,
            gwpVal,
            featuresStr
        ];

        rows.push(row.map(escapeCsvField).join(','));
    }

    // Excel 文字化け防止のため BOM (\uFEFF) を先頭に付与して保存
    const csvContent = '\uFEFF' + rows.join('\r\n');
    const outputPath = path.join(process.cwd(), 'merged_aircon_models.csv');
    fs.writeFileSync(outputPath, csvContent, 'utf8');
    console.log(`Successfully exported ${rows.length - 1} rows to ${outputPath}`);
}

main();
