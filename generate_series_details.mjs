import fs from 'fs';
import path from 'path';

// RXシリーズ共通機能フラグ
const rxFunctions = {
    "基本運転": [
        "NEW プレミアムPIT制御",
        "プレミアム冷房",
        "高外気タフネス冷房 (50℃対応)",
        "低外気タフネス暖房 (-25℃対応)",
        "鍛え浸防制熱交換器",
        "ドレンパンヒーター"
    ],
    "しつど制御": [
        "うるる加湿 (無給水加湿)",
        "吸音マフラー",
        "さらら除湿 (リニアハイブリッド方式)",
        "9段階セレクトドライ"
    ],
    "自動運転": [
        "AI快適自動運転 (人・床・壁センサー/換気制御)",
        "節電自動運転 (温度・しつどコントロール)"
    ],
    "気流制御": [
        "垂直気流 (暖房・冷房)",
        "サーキュレーション気流",
        "NEW 猛暑時スピード気流",
        "風ないス運転",
        "ロング気流 (12m/4.0kW以上)",
        "オートスイング (上下/左右/立体)",
        "センサー風向"
    ],
    "清潔": [
        "給気換気／排気換気",
        "美肌保湿運転",
        "水内部クリーン (加湿水洗浄)",
        "水内部クリーン (結露水洗浄)",
        "セルフウォッシュ熱交換器",
        "クリアコート熱交換器",
        "ストリーマ (空気清浄/内部クリーン)",
        "防カビ加工ファン",
        "銀イオン抗菌剤 (室内機ドレンパン)",
        "抗ウイルスフィルター",
        "フィルター自動お掃除",
        "水de脱臭"
    ],
    "快適温度制御": [
        "高温風モード (最大60℃吹出し)",
        "NEW エコブースト制御",
        "ヒートブースト制御",
        "クールブースト制御",
        "10℃からの暖房設定",
        "インテリジェントデフロスト",
        "人・床温度センサー"
    ],
    "生活便利": [
        "しつどクリーン",
        "消し忘れ防止機能",
        "パワーセレクト",
        "音声応答機能",
        "リモコン設定メモリー機能",
        "パワフル運転",
        "ランドリー乾燥",
        "室温パトロール",
        "NEW 高温防止モード",
        "新・おやすみ運転"
    ],
    "タイマー_機能": [
        "時刻設定入切タイマー (学習入タイマー)",
        "ワンタッチ切タイマー",
        "ワンタッチ入タイマー",
        "スマホ接続対応 (無線LAN接続アダプター内蔵)"
    ]
};

// RXシリーズ各型番の詳細仕様データ定義
const rxModelsData = [
    {
        model: "S22ATRS-W(-C)",
        tatami: "6畳程度",
        price_total: { tax_inc: 517000, tax_exc: 470000 },
        indoor: { model: "F22ATRS-W(-C)", weight: 16, tax_inc: 209000, tax_exc: 190000 },
        outdoor: { model: "R22ARS", weight: 43, tax_inc: 308000, tax_exc: 280000 },
        power: { phase: "単相", voltage: 100, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 795, margin_w: 78, depth: 300, margin_d: 42, height: 728 },
        heating: { tatami: "6〜7畳", area: "9〜11㎡", kw: 2.5, kw_range: [0.6, 6.2], w: 440, w_range: [75, 1820] },
        cooling: { tatami: "6〜9畳", area: "10〜15㎡", kw: 2.2, kw_range: [0.5, 3.3], w: 390, w_range: [75, 850] },
        energy: { kwh: 603, target_year: 2027, rate_pct: 104, apf: 6.9, low_temp_kw: 4.5 }
    },
    {
        model: "S25ATRS-W(-C)",
        tatami: "8畳程度",
        price_total: { tax_inc: 561000, tax_exc: 510000 },
        indoor: { model: "F25ATRS-W(-C)", weight: 16, tax_inc: 222200, tax_exc: 202000 },
        outdoor: { model: "R25ARS", weight: 43, tax_inc: 338800, tax_exc: 308000 },
        power: { phase: "単相", voltage: 100, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 795, margin_w: 78, depth: 300, margin_d: 42, height: 728 },
        heating: { tatami: "6〜8畳", area: "10〜13㎡", kw: 2.8, kw_range: [0.6, 6.3], w: 500, w_range: [75, 1820] },
        cooling: { tatami: "7〜10畳", area: "11〜17㎡", kw: 2.5, kw_range: [0.5, 3.5], w: 470, w_range: [75, 870] },
        energy: { kwh: 695, target_year: 2027, rate_pct: 103, apf: 6.8, low_temp_kw: 4.7 }
    },
    {
        model: "S28ATRS-W(-C)",
        tatami: "10畳程度",
        price_total: { tax_inc: 605000, tax_exc: 550000 },
        indoor: { model: "F28ATRS-W(-C)", weight: 16, tax_inc: 242000, tax_exc: 220000 },
        outdoor: { model: "R28ARS", weight: 46, tax_inc: 363000, tax_exc: 330000 },
        power: { phase: "単相", voltage: 100, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 795, margin_w: 78, depth: 300, margin_d: 42, height: 728 },
        heating: { tatami: "8〜10畳", area: "13〜16㎡", kw: 3.6, kw_range: [0.6, 7.2], w: 660, w_range: [75, 2000] },
        cooling: { tatami: "8〜12畳", area: "13〜19㎡", kw: 2.8, kw_range: [0.5, 4.0], w: 550, w_range: [70, 1030] },
        energy: { kwh: 790, target_year: 2027, rate_pct: 101, apf: 6.7, low_temp_kw: 5.7 }
    },
    {
        model: "S36ATRS-W(-C)",
        tatami: "12畳程度",
        price_total: { tax_inc: 627000, tax_exc: 570000 },
        indoor: { model: "F36ATRS-W(-C)", weight: 16, tax_inc: 248600, tax_exc: 226000 },
        outdoor: { model: "R36ARS", weight: 48, tax_inc: 378400, tax_exc: 344000 },
        power: { phase: "単相", voltage: 100, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 795, margin_w: 78, depth: 300, margin_d: 42, height: 728 },
        heating: { tatami: "9〜12畳", area: "15〜19㎡", kw: 4.2, kw_range: [0.6, 7.3], w: 810, w_range: [65, 2000] },
        cooling: { tatami: "10〜15畳", area: "16〜25㎡", kw: 3.6, kw_range: [0.5, 4.1], w: 800, w_range: [65, 1020] },
        energy: { kwh: 1032, target_year: 2027, rate_pct: 100, apf: 6.6, low_temp_kw: 5.7 }
    },
    {
        model: "S40ATRS-W(-C)",
        tatami: "14畳程度",
        price_total: { tax_inc: 660000, tax_exc: 600000 },
        indoor: { model: "F40ATRS-W(-C)", weight: 16.5, tax_inc: 261800, tax_exc: 238000 },
        outdoor: { model: "R40ARS", weight: 48, tax_inc: 398200, tax_exc: 362000 },
        power: { phase: "単相", voltage: 100, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 795, margin_w: 78, depth: 300, margin_d: 42, height: 728 },
        heating: { tatami: "11〜14畳", area: "18〜23㎡", kw: 5.0, kw_range: [0.4, 7.2], w: 1000, w_range: [70, 2000] },
        cooling: { tatami: "11〜17畳", area: "18〜28㎡", kw: 4.0, kw_range: [0.4, 5.3], w: 920, w_range: [65, 1600] },
        energy: { kwh: 1146, target_year: 2027, rate_pct: 100, apf: 6.6, low_temp_kw: 5.7 }
    },
    {
        model: "S40ATRP-W(-C)",
        tatami: "14畳程度",
        price_total: { tax_inc: 660000, tax_exc: 600000 },
        indoor: { model: "F40ATRP-W(-C)", weight: 16.5, tax_inc: 261800, tax_exc: 238000 },
        outdoor: { model: "R40ARP", weight: 56, tax_inc: 398200, tax_exc: 362000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862 },
        heating: { tatami: "11〜14畳", area: "18〜23㎡", kw: 5.0, kw_range: [0.4, 12.1], w: 890, w_range: [65, 3580] },
        cooling: { tatami: "11〜17畳", area: "18〜28㎡", kw: 4.0, kw_range: [0.3, 5.3], w: 770, w_range: [65, 1300] },
        energy: { kwh: 1036, target_year: 2027, rate_pct: 110, apf: 7.3, low_temp_kw: 9.0 }
    },
    {
        model: "S40ATRV-W(-C)",
        tatami: "14畳程度",
        price_total: { tax_inc: 660000, tax_exc: 600000 },
        indoor: { model: "F40ATRV-W(-C)", weight: 16.5, tax_inc: 261800, tax_exc: 238000 },
        outdoor: { model: "R40ARV", weight: 56, tax_inc: 398200, tax_exc: 362000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: true },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862 },
        heating: { tatami: "11〜14畳", area: "18〜23㎡", kw: 5.0, kw_range: [0.4, 12.1], w: 890, w_range: [65, 3580] },
        cooling: { tatami: "11〜17畳", area: "18〜28㎡", kw: 4.0, kw_range: [0.3, 5.3], w: 770, w_range: [65, 1300] },
        energy: { kwh: 1036, target_year: 2027, rate_pct: 110, apf: 7.3, low_temp_kw: 9.0 }
    },
    {
        model: "S56ATRP-W(-C)",
        tatami: "18畳程度",
        price_total: { tax_inc: 715000, tax_exc: 650000 },
        indoor: { model: "F56ATRP-W(-C)", weight: 16.5, tax_inc: 286000, tax_exc: 260000 },
        outdoor: { model: "R56ARP", weight: 56, tax_inc: 429000, tax_exc: 390000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862 },
        heating: { tatami: "15〜18畳", area: "24〜30㎡", kw: 6.7, kw_range: [0.4, 12.1], w: 1380, w_range: [75, 3580] },
        cooling: { tatami: "15〜23畳", area: "25〜39㎡", kw: 5.6, kw_range: [0.3, 6.0], w: 1390, w_range: [70, 1580] },
        energy: { kwh: 1605, target_year: 2027, rate_pct: 104, apf: 6.6, low_temp_kw: 9.0 }
    },
    {
        model: "S56ATRV-W(-C)",
        tatami: "18畳程度",
        price_total: { tax_inc: 715000, tax_exc: 650000 },
        indoor: { model: "F56ATRV-W(-C)", weight: 16.5, tax_inc: 286000, tax_exc: 260000 },
        outdoor: { model: "R56ARV", weight: 56, tax_inc: 429000, tax_exc: 390000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: true },
        piping: { liquid: 6.4, gas: 9.5, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862 },
        heating: { tatami: "15〜18畳", area: "24〜30㎡", kw: 6.7, kw_range: [0.4, 12.1], w: 1380, w_range: [75, 3580] },
        cooling: { tatami: "15〜23畳", area: "25〜39㎡", kw: 5.6, kw_range: [0.3, 6.0], w: 1390, w_range: [70, 1580] },
        energy: { kwh: 1605, target_year: 2027, rate_pct: 104, apf: 6.6, low_temp_kw: 9.0 }
    },
    {
        model: "S63ATRP-W(-C)",
        tatami: "20畳程度",
        price_total: { tax_inc: 803000, tax_exc: 730000 },
        indoor: { model: "F63ATRP-W(-C)", weight: 16.5, tax_inc: 325600, tax_exc: 296000 },
        outdoor: { model: "R63ARP", weight: 52, tax_inc: 477400, tax_exc: 434000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 12.7, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 799 },
        heating: { tatami: "16〜20畳", area: "26〜32㎡", kw: 7.1, kw_range: [0.4, 12.2], w: 1550, w_range: [75, 3730] },
        cooling: { tatami: "17〜26畳", area: "29〜43㎡", kw: 6.3, kw_range: [0.3, 6.5], w: 1750, w_range: [80, 1820] },
        energy: { kwh: 1922, target_year: 2027, rate_pct: 101, apf: 6.2, low_temp_kw: 9.1 }
    },
    {
        model: "S63ATRV-W(-C)",
        tatami: "20畳程度",
        price_total: { tax_inc: 803000, tax_exc: 730000 },
        indoor: { model: "F63ATRV-W(-C)", weight: 16.5, tax_inc: 325600, tax_exc: 296000 },
        outdoor: { model: "R63ARV", weight: 52, tax_inc: 477400, tax_exc: 434000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: true },
        piping: { liquid: 6.4, gas: 12.7, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 799 },
        heating: { tatami: "16〜20畳", area: "26〜32㎡", kw: 7.1, kw_range: [0.4, 12.2], w: 1550, w_range: [75, 3730] },
        cooling: { tatami: "17〜26畳", area: "29〜43㎡", kw: 6.3, kw_range: [0.3, 6.5], w: 1750, w_range: [80, 1820] },
        energy: { kwh: 1922, target_year: 2027, rate_pct: 101, apf: 6.2, low_temp_kw: 9.1 }
    },
    {
        model: "S71ATRP-W(-C)",
        tatami: "23畳程度",
        price_total: { tax_inc: 880000, tax_exc: 800000 },
        indoor: { model: "F71ATRP-W(-C)", weight: 16.5, tax_inc: 352000, tax_exc: 320000 },
        outdoor: { model: "R71ARP", weight: 55, tax_inc: 528000, tax_exc: 480000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 12.7, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862 },
        heating: { tatami: "19〜23畳", area: "31〜39㎡", kw: 8.5, kw_range: [0.4, 12.2], w: 2020, w_range: [80, 3730] },
        cooling: { tatami: "20〜30畳", area: "32〜49㎡", kw: 7.1, kw_range: [0.3, 7.3], w: 2210, w_range: [90, 2240] },
        energy: { kwh: 2276, target_year: 2027, rate_pct: 100, apf: 5.9, low_temp_kw: 9.1 }
    },
    {
        model: "S71ATRV-W(-C)",
        tatami: "23畳程度",
        price_total: { tax_inc: 880000, tax_exc: 800000 },
        indoor: { model: "F71ATRV-W(-C)", weight: 16.5, tax_inc: 352000, tax_exc: 320000 },
        outdoor: { model: "R71ARV", weight: 55, tax_inc: 528000, tax_exc: 480000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: true },
        piping: { liquid: 6.4, gas: 12.7, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862 },
        heating: { tatami: "19〜23畳", area: "31〜39㎡", kw: 8.5, kw_range: [0.4, 12.2], w: 2020, w_range: [80, 3730] },
        cooling: { tatami: "20〜30畳", area: "32〜49㎡", kw: 7.1, kw_range: [0.3, 7.3], w: 2210, w_range: [90, 2240] },
        energy: { kwh: 2276, target_year: 2027, rate_pct: 100, apf: 5.9, low_temp_kw: 9.1 }
    },
    {
        model: "S80ATRP-W(-C)",
        tatami: "26畳程度",
        price_total: { tax_inc: 957000, tax_exc: 870000 },
        indoor: { model: "F80ATRP-W(-C)", weight: 16.5, tax_inc: 382800, tax_exc: 348000 },
        outdoor: { model: "R80ARP", weight: 59, tax_inc: 574200, tax_exc: 522000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 12.7, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862, note: "8.0kW-9.0kWは★72mm" },
        heating: { tatami: "21〜26畳", area: "35〜43㎡", kw: 9.5, kw_range: [0.4, 12.2], w: 2450, w_range: [85, 3730] },
        cooling: { tatami: "22〜33畳", area: "36〜55㎡", kw: 8.0, kw_range: [0.3, 8.2], w: 2910, w_range: [90, 3060] },
        energy: { kwh: 2655, target_year: 2027, rate_pct: 100, apf: 5.7, low_temp_kw: 9.1 }
    },
    {
        model: "S90ATRP-W(-C)",
        tatami: "29畳程度",
        price_total: { tax_inc: 1034000, tax_exc: 940000 },
        indoor: { model: "F90ATRP-W(-C)", weight: 16.5, tax_inc: 413600, tax_exc: 376000 },
        outdoor: { model: "R90ARP", weight: 59, tax_inc: 620400, tax_exc: 564000 },
        power: { phase: "単相", voltage: 200, current: 20, is_outdoor_power: false },
        piping: { liquid: 6.4, gas: 12.7, max_len: 15, chargeless: 15, max_diff: 12 },
        outdoor_dim: { width: 850, margin_w: 89, depth: 320, margin_d: 66, height: 862, note: "8.0kW-9.0kWは★72mm" },
        heating: { tatami: "23〜29畳", area: "39〜48㎡", kw: 10.6, kw_range: [0.4, 12.4], w: 2960, w_range: [90, 3960] },
        cooling: { tatami: "25〜38畳", area: "41〜62㎡", kw: 9.0, kw_range: [0.6, 9.1], w: 2990, w_range: [120, 3070] },
        energy: { kwh: 3274, target_year: 2027, rate_pct: 94, apf: 5.2, low_temp_kw: 9.5 }
    }
];

const productSeriesDetails = rxModelsData.map(item => {
    return {
        model_number: item.model,
        series_name: "RX SERIES",
        series_nickname: "うるさらX",
        model_year: "2026年モデル",
        unique_selling_point: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル",
        color_variations: ["ホワイト(-W) (N9.5)", "ベージュ(-C) (1Y 7.5/2)"],
        recommendation_tags: [
            "北海道電力推薦 あったかエアコン",
            "東北電力推薦 暖房エアコン",
            "ZEHにもおすすめ",
            "うるるとさらら",
            "STREAMER"
        ],
        price_total: {
            is_open_price: false,
            tax_included_yen: item.price_total.tax_inc,
            tax_excluded_yen: item.price_total.tax_exc
        },
        indoor_unit: {
            model_number: item.indoor.model,
            weight_kg: item.indoor.weight,
            tax_included_yen: item.indoor.tax_inc,
            tax_excluded_yen: item.indoor.tax_exc
        },
        outdoor_unit: {
            model_number: item.outdoor.model,
            weight_kg: item.outdoor.weight,
            tax_included_yen: item.outdoor.tax_inc,
            tax_excluded_yen: item.outdoor.tax_exc
        },
        power_supply: {
            phase: item.power.phase,
            voltage_v: item.power.voltage,
            current_a: item.power.current,
            is_outdoor_power_supply: item.power.is_outdoor_power
        },
        piping: {
            liquid_mm: item.piping.liquid,
            gas_mm: item.piping.gas,
            max_length_m: item.piping.max_len,
            chargeless_length_m: item.piping.chargeless,
            max_height_difference_m: item.piping.max_diff
        },
        dimensions_mm: {
            indoor: {
                width: 798,
                height: 295,
                depth: 370,
                compact_type: "半間コンパクト"
            },
            outdoor: {
                width: item.outdoor_dim.width,
                width_margin: item.outdoor_dim.margin_w,
                depth: item.outdoor_dim.depth,
                depth_margin: item.outdoor_dim.margin_d,
                height: item.outdoor_dim.height,
                note: item.outdoor_dim.note || null
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
        functions: rxFunctions
    };
});

const outputPath = path.join(process.cwd(), 'product_series_details_rx.json');
fs.writeFileSync(outputPath, JSON.stringify(productSeriesDetails, null, 2), 'utf8');
console.log(`Successfully generated product_series_details_rx.json with ${productSeriesDetails.length} models.`);
