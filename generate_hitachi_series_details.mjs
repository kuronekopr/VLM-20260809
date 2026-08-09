import fs from 'fs';
import path from 'path';

// 日立 Xシリーズ共通詳細機能フラグ
const hitachiXFunctions = {
    "空気清浄": ["Premiumプラズマ空清", "凍結洗浄 クリーナー", "プラス換気ユニット (別売)"],
    "室外お掃除": ["室外熱交換器 凍結洗浄"],
    "熱交換器_清潔": ["ヒートプラス (熱交換器高温加熱)", "不在時に自動洗浄", "タイマー洗浄", "手動洗浄", "イオンを内部に充満", "銅排水トレー自動洗浄"],
    "ファン清潔": ["ファンお掃除ロボ (ファンの汚れを自動お掃除)", "ステンレス・ファン", "ビッグ＆ウェーブファン"],
    "エアコン内部清潔": ["ステンレス・クリーン システム", "銅排水トレー", "親水性コーティング熱交換器", "カビバスター (エアコン内部クリーン)", "内部湿気乾燥運転"],
    "センサー_自動": ["くらしセンサー (人感・日射センサー)", "LA自慢制御", "eco運転", "オートセーブ／オートオフ"],
    "快適_気流": ["風よけエリアセレクト", "ロング＆ワイド気流", "上下スイング", "左右スイング"],
    "除湿_冷房": ["カラっと除湿 <再熱方式> (自動/手動/ランドリー/けつろ/パワフル/カビ見張り)", "健康冷房 [涼快]", "冷房", "[みはっておやすみ]", "[快眠] モード", "外気温50℃でも冷房運転可能"],
    "暖房": ["つつみこみ暖房", "スピード暖房", "温風プラス", "あらかじめ温風", "みはって霜取りS"],
    "スマホ連携": ["白くまくんアプリ (無線LAN機能内蔵)"],
    "点検_タイマー": ["シーズン前自動点検", "毎日予約"]
};

// 日立 Xシリーズ 各型番の詳細仕様定義
const hitachiXModelsData = [
    {
        model: "RAS-X2226S",
        outdoor_model: "RAC-XR2226S",
        voltage: 100,
        current: 20,
        outdoor_dim: { width: 799, margin_w: 97, depth: 299, margin_d: 68, height: 629 },
        heating: { tatami: "6〜7畳", area: "9〜11㎡", kw: 2.5, kw_range: [0.3, 6.0], w: 430, w_range: [110, 1490] },
        cooling: { tatami: "6〜9畳", area: "10〜15㎡", kw: 2.2, kw_range: [0.4, 3.5], w: 400, w_range: [115, 900] },
        energy: { kwh: 570, target_year: 2027, rate_pct: 110, apf: 7.3, low_temp_kw: 4.5 }
    },
    {
        model: "RAS-X2526S",
        outdoor_model: "RAC-XR2526S",
        voltage: 100,
        current: 20,
        outdoor_dim: { width: 799, margin_w: 97, depth: 299, margin_d: 68, height: 629 },
        heating: { tatami: "6〜8畳", area: "10〜13㎡", kw: 2.8, kw_range: [0.3, 6.0], w: 490, w_range: [110, 1490] },
        cooling: { tatami: "7〜10畳", area: "11〜17㎡", kw: 2.5, kw_range: [0.4, 3.6], w: 490, w_range: [115, 920] },
        energy: { kwh: 648, target_year: 2027, rate_pct: 110, apf: 7.3, low_temp_kw: 4.5 }
    },
    {
        model: "RAS-X2826S",
        outdoor_model: "RAC-XR2826S",
        voltage: 100,
        current: 20,
        outdoor_dim: { width: 799, margin_w: 97, depth: 299, margin_d: 68, height: 629 },
        heating: { tatami: "8〜10畳", area: "13〜16㎡", kw: 3.6, kw_range: [0.3, 6.8], w: 680, w_range: [110, 1995] },
        cooling: { tatami: "8〜12畳", area: "13〜19㎡", kw: 2.8, kw_range: [0.4, 4.1], w: 560, w_range: [115, 1210] },
        energy: { kwh: 746, target_year: 2027, rate_pct: 107, apf: 7.1, low_temp_kw: 5.5 }
    },
    {
        model: "RAS-X3626S",
        outdoor_model: "RAC-XR3626S",
        voltage: 100,
        current: 20,
        outdoor_dim: { width: 799, margin_w: 97, depth: 299, margin_d: 68, height: 629 },
        heating: { tatami: "9〜12畳", area: "15〜19㎡", kw: 4.2, kw_range: [0.3, 6.9], w: 890, w_range: [110, 1995] },
        cooling: { tatami: "10〜15畳", area: "16〜25㎡", kw: 3.6, kw_range: [0.4, 4.2], w: 825, w_range: [115, 1250] },
        energy: { kwh: 1032, target_year: 2027, rate_pct: 100, apf: 6.6, low_temp_kw: 5.5 }
    },
    {
        model: "RAS-XR4026D",
        outdoor_model: "RAC-XR4026D",
        voltage: 200,
        current: 20,
        outdoor_dim: { width: 859, margin_w: 97, depth: 319, margin_d: 68, height: 709 },
        heating: { tatami: "11〜14畳", area: "18〜23㎡", kw: 5.0, kw_range: [0.4, 11.9], w: 920, w_range: [135, 3900] },
        cooling: { tatami: "11〜17畳", area: "18〜28㎡", kw: 4.0, kw_range: [0.5, 5.5], w: 880, w_range: [155, 1800] },
        energy: { kwh: 1066, target_year: 2027, rate_pct: 107, apf: 7.1, low_temp_kw: 8.9 }
    },
    {
        model: "RAS-XR5626D",
        outdoor_model: "RAC-XR5626D",
        voltage: 200,
        current: 20,
        outdoor_dim: { width: 859, margin_w: 97, depth: 319, margin_d: 68, height: 709 },
        heating: { tatami: "15〜18畳", area: "24〜30㎡", kw: 6.7, kw_range: [0.4, 11.9], w: 1480, w_range: [135, 3900] },
        cooling: { tatami: "15〜23畳", area: "25〜39㎡", kw: 5.6, kw_range: [0.5, 6.0], w: 1600, w_range: [155, 2000] },
        energy: { kwh: 1655, target_year: 2027, rate_pct: 101, apf: 6.4, low_temp_kw: 8.9 }
    },
    {
        model: "RAS-XR6326D",
        outdoor_model: "RAC-XR6326D",
        voltage: 200,
        current: 20,
        outdoor_dim: { width: 859, margin_w: 97, depth: 319, margin_d: 68, height: 709 },
        heating: { tatami: "16〜20畳", area: "26〜32㎡", kw: 7.1, kw_range: [0.4, 12.2], w: 1700, w_range: [135, 3900] },
        cooling: { tatami: "17〜26畳", area: "29〜43㎡", kw: 6.3, kw_range: [0.6, 6.7], w: 1760, w_range: [175, 3050] },
        energy: { kwh: 1922, target_year: 2027, rate_pct: 101, apf: 6.2, low_temp_kw: 8.9 }
    },
    {
        model: "RAS-XR7126D",
        outdoor_model: "RAC-XR7126D",
        voltage: 200,
        current: 20,
        outdoor_dim: { width: 859, margin_w: 97, depth: 319, margin_d: 68, height: 709 },
        heating: { tatami: "19〜23畳", area: "31〜39㎡", kw: 8.5, kw_range: [0.4, 11.9], w: 2140, w_range: [145, 3900] },
        cooling: { tatami: "20〜30畳", area: "32〜49㎡", kw: 7.1, kw_range: [0.6, 7.2], w: 2340, w_range: [175, 3100] },
        energy: { kwh: 2276, target_year: 2027, rate_pct: 100, apf: 5.9, low_temp_kw: 8.9 }
    },
    {
        model: "RAS-XR8026D",
        outdoor_model: "RAC-XR8026D",
        voltage: 200,
        current: 20,
        outdoor_dim: { width: 859, margin_w: 97, depth: 319, margin_d: 68, height: 709 },
        heating: { tatami: "21〜26畳", area: "35〜43㎡", kw: 9.5, kw_range: [0.4, 11.9], w: 2580, w_range: [145, 3900] },
        cooling: { tatami: "22〜33畳", area: "36〜55㎡", kw: 8.0, kw_range: [0.6, 8.1], w: 2900, w_range: [175, 3150] },
        energy: { kwh: 2655, target_year: 2027, rate_pct: 100, apf: 5.7, low_temp_kw: 8.9 }
    },
    {
        model: "RAS-XR9026D",
        outdoor_model: "RAC-XR9026D",
        voltage: 200,
        current: 20,
        outdoor_dim: { width: 859, margin_w: 97, depth: 319, margin_d: 68, height: 709 },
        heating: { tatami: "23〜29畳", area: "39〜48㎡", kw: 10.6, kw_range: [0.4, 12.0], w: 3200, w_range: [145, 3900] },
        cooling: { tatami: "25〜38畳", area: "41〜62㎡", kw: 9.0, kw_range: [0.6, 9.13], w: 3000, w_range: [175, 3200] },
        energy: { kwh: 3338, target_year: 2027, rate_pct: 92, apf: 5.1, low_temp_kw: 9.1 }
    }
];

const productSeriesDetailsHitachiX = hitachiXModelsData.map(item => {
    return {
        manufacturer: "日立",
        product_category: "壁掛形ルームエアコン",
        brand_name: "白くまくん",
        model_number: item.model,
        series_name: "Xシリーズ",
        series_nickname: "白くまくん",
        model_year: "2026年モデル",
        unique_selling_point: "[LA自慢]・[凍結洗浄 ヒートプラス]・[ファンお掃除ロボ]・[Premiumプラズマ空清]・[凍結洗浄 クリーナー] 搭載プレミアムモデル",
        color_variations: ["スターホワイト(W)"],
        recommendation_tags: [
            "東北電力推薦 暖房エアコン",
            "ZEHにもおすすめ",
            "フロンラベル A",
            "日本製"
        ],
        price_total: {
            is_open_price: true,
            energy_saving_achievement_pct: item.energy.rate_pct,
            raw_text: `オープン価格 (省エネ達成率 ${item.energy.rate_pct}%)`
        },
        indoor_unit: {
            model_number: item.model,
            weight_kg: null,
            is_open_price: true
        },
        outdoor_unit: {
            model_number: item.outdoor_model,
            weight_kg: null,
            is_open_price: true
        },
        power_supply: {
            phase: "単相",
            voltage_v: item.voltage,
            current_a: item.current,
            is_outdoor_power_supply: false
        },
        piping: {
            liquid_mm: 6.4,
            gas_mm: 9.5,
            max_length_m: 20,
            chargeless_length_m: 20,
            max_height_difference_m: 10
        },
        dimensions_mm: {
            indoor: {
                width: 798,
                height: 295,
                depth: 385
            },
            outdoor: {
                width: item.outdoor_dim.width,
                width_margin: item.outdoor_dim.margin_w,
                depth: item.outdoor_dim.depth,
                depth_margin: item.outdoor_dim.margin_d,
                height: item.outdoor_dim.height
            }
        },
        specs: {
            heating: {
                tatami_range: item.heating.tatami,
                area_m2: item.heating.area,
                capacity_kw: item.heating.kw,
                capacity_range_kw: item.heating.kw_range,
                power_w: item.heating.w,
                power_range_w: item.heating.w_range
            },
            cooling: {
                tatami_range: item.cooling.tatami,
                area_m2: item.cooling.area,
                capacity_kw: item.cooling.kw,
                capacity_range_kw: item.cooling.kw_range,
                power_w: item.cooling.w,
                power_range_w: item.cooling.w_range
            },
            energy_saving: {
                annual_power_consumption_kwh: item.energy.kwh,
                target_year: item.energy.target_year,
                achievement_rate_pct: item.energy.rate_pct,
                apf: item.energy.apf,
                low_temp_heating_capacity_kw: item.energy.low_temp_kw
            }
        },
        functions: hitachiXFunctions
    };
});

const outputPath = path.join(process.cwd(), 'product_series_details_hitachi_x.json');
fs.writeFileSync(outputPath, JSON.stringify(productSeriesDetailsHitachiX, null, 2), 'utf8');
console.log(`Successfully generated product_series_details_hitachi_x.json with ${productSeriesDetailsHitachiX.length} models.`);
