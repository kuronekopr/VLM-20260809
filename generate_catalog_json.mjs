import fs from 'fs';
import path from 'path';

// 各シリーズ共通のおもなおすすめポイント定義
const recommendedFeaturesMap = {
    "RX SERIES": {
        "基本運転_室外機機能": [
            "スイングコンプレッサー",
            "デシクル制御",
            "NEW プレミアムPIT制御",
            "プレミアム冷房",
            "高外気タフネス冷房 (50℃対応)",
            "低外気タフネス暖房 (-25℃対応)"
        ],
        "しつど制御": [
            "うるる加湿 (無給水加湿)",
            "吸音マフラー",
            "さらら除湿 (リニアハイブリッド方式)"
        ],
        "自動運転_節電運転": [
            "AI快適自動運転 (人・床・壁センサー / 換気制御)",
            "節電自動運転 (温度・しつどコントロール)"
        ],
        "気流制御": [
            "垂直気流 (暖房・冷房)",
            "サーキュレーション気流",
            "NEW 猛暑時スピード気流",
            "オートスイング (上下/左右/立体)"
        ],
        "清潔": [
            "給気換気／排気換気",
            "水内部クリーン (加湿水洗浄/結露水洗浄)",
            "ストリーマ (空気清浄/内部クリーン)",
            "セルフウォッシュ熱交換器",
            "防カビ加工ファン",
            "銀イオン抗菌剤 (室内機ドレンパン)",
            "抗ウイルスフィルター",
            "フィルター自動お掃除"
        ],
        "快適温度制御": [
            "高温風モード (最大60℃吹出し)",
            "NEW エコブースト制御",
            "ヒートブースト制御/クールブースト制御"
        ],
        "生活便利": [
            "室温パトロール/消し忘れ防止機能",
            "しつどクリーン/パワーセレクト/音声応答機能",
            "新・おやすみ運転",
            "かんたん大画面リモコン"
        ],
        "その他": [
            "無線LAN接続アダプター内蔵"
        ]
    },
    "AX SERIES": {
        "基本運転_室外機機能": [
            "スイングコンプレッサー",
            "デシクル制御",
            "NEW プレミアムPIT制御",
            "プレミアム冷房",
            "高外気タフネス冷房 (50℃対応)",
            "低外気タフネス暖房 (-25℃対応)"
        ],
        "しつど制御": [
            "さらら除湿 (リニアハイブリッド方式)"
        ],
        "自動運転_節電運転": [
            "AI快適自動運転 (人・床・壁センサー)",
            "節電自動運転 (温度・しつどコントロール)"
        ],
        "気流制御": [
            "垂直気流 (暖房・冷房)",
            "サーキュレーション気流",
            "NEW 猛暑時スピード気流",
            "オートスイング (上下/左右/立体)"
        ],
        "清潔": [
            "水内部クリーン (結露水洗浄)",
            "ストリーマ (空気清浄/内部クリーン)",
            "セルフウォッシュ熱交換器",
            "防カビ加工ファン",
            "銀イオン抗菌剤 (室内機ドレンパン)",
            "抗ウイルスフィルター",
            "フィルター自動お掃除"
        ],
        "快適温度制御": [
            "高温風モード (最大60℃吹出し)",
            "NEW エコブースト制御",
            "ヒートブースト制御/クールブースト制御"
        ],
        "生活便利": [
            "室温パトロール/消し忘れ防止機能",
            "しつどクリーン/パワーセレクト/音声応答機能",
            "新・おやすみ運転",
            "かんたん大画面リモコン"
        ],
        "その他": [
            "無線LAN接続アダプター内蔵"
        ]
    },
    "SX SERIES": {
        "基本運転_室外機機能": [
            "スイングコンプレッサー",
            "デシクル制御・PIT制御",
            "プレミアム冷房",
            "高外気タフネス冷房 (50℃対応)",
            "低外気タフネス暖房 (-15℃対応)"
        ],
        "しつど制御": [
            "さらら除湿"
        ],
        "自動運転_節電運転": [
            "快適自動運転 (人・床温度センサー)"
        ],
        "気流制御": [
            "垂直気流 (暖房)",
            "風ないス運転 (天井気流)",
            "オートスイング (上下/左右/立体)"
        ],
        "清潔": [
            "水内部クリーン (結露水洗浄)",
            "ストリーマ (空気清浄/内部クリーン)",
            "クリアコート熱交換器",
            "防カビ加工ファン",
            "抗ウイルスフィルター"
        ],
        "快適温度制御": [
            "ヒートブースト制御/クールブースト制御"
        ],
        "生活便利": [
            "室温パトロール/消し忘れ防止機能",
            "おやすみ運転",
            "かんたんスタイリッシュリモコン"
        ],
        "その他": [
            "無線LAN接続アダプター内蔵"
        ]
    },
    "GX SERIES": {
        "基本運転_室外機機能": [
            "スイングコンプレッサー",
            "デシクル制御・PIT制御",
            "プレミアム冷房",
            "高外気タフネス冷房 (50℃対応)",
            "低外気タフネス暖房 (-15℃対応)"
        ],
        "しつど制御": [
            "さらら除湿 (ハイブリッド方式)"
        ],
        "自動運転_節電運転": [
            "快適自動運転"
        ],
        "気流制御": [
            "風ないス運転 (天井気流・暖気かくはん運転)",
            "オートスイング (上下/左右/立体)"
        ],
        "清潔": [
            "水内部クリーン (結露水洗浄)",
            "ストリーマ (空気清浄/内部クリーン)",
            "クリアコート熱交換器",
            "防カビ加工ファン",
            "抗ウイルスフィルター",
            "フィルター自動お掃除"
        ],
        "快適温度制御": [
            "ヒートブースト制御/クールブースト制御"
        ],
        "生活便利": [
            "室温パトロール",
            "おやすみ運転",
            "かんたんダイレクトリモコン"
        ],
        "その他": [
            "無線LAN接続アダプター内蔵"
        ]
    },
    "CX SERIES": {
        "基本運転_室外機機能": [
            "スイングコンプレッサー",
            "PIT制御",
            "高外気タフネス冷房 (50℃対応)",
            "低外気タフネス暖房 (-15℃対応)"
        ],
        "しつど制御": [
            "9段階セレクトドライ"
        ],
        "自動運転_節電運転": [
            "自動運転"
        ],
        "気流制御": [
            "風ないス運転 (天井気流)",
            "オートスイング (上下/左右/立体)"
        ],
        "清潔": [
            "水内部クリーン (結露水洗浄)",
            "ストリーマ (空気清浄/内部クリーン)",
            "クリアコート熱交換器",
            "抗ウイルスフィルター",
            "フィルター自動お掃除"
        ],
        "快適温度制御": [
            "ヒートブースト制御"
        ],
        "生活便利": [
            "室温パトロール",
            "おやすみ運転",
            "かんたんダイレクトリモコン"
        ],
        "その他": [
            "無線LAN接続アダプター内蔵"
        ]
    },
    "E SERIES": {
        "基本運転_室外機機能": [
            "スイングコンプレッサー",
            "PIT制御",
            "高外気タフネス冷房 (50℃対応)",
            "低外気タフネス暖房 (-15℃対応)"
        ],
        "しつど制御": [
            "9段階セレクトドライ"
        ],
        "自動運転_節電運転": [
            "自動運転"
        ],
        "気流制御": [
            "風ないス運転",
            "オートスイング (上下)"
        ],
        "清潔": [
            "水内部クリーン (結露水洗浄)",
            "ストリーマ (空気清浄/内部クリーン)",
            "クリアコート熱交換器",
            "抗ウイルスフィルター"
        ],
        "快適温度制御": [
            "ヒートブースト制御"
        ],
        "生活便利": [
            "室温パトロール",
            "おやすみ運転",
            "かんたんダイレクトリモコン"
        ],
        "その他": [
            "無線LAN接続アダプター別売"
        ]
    }
};

const rawModels = [
    // RX SERIES
    { model: "S22ATRS", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "6畳程度", kw: 2.2, tax_inc: 517000, tax_exc: 470000 },
    { model: "S25ATRS", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "8畳程度", kw: 2.5, tax_inc: 561000, tax_exc: 510000 },
    { model: "S28ATRS", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "10畳程度", kw: 2.8, tax_inc: 605000, tax_exc: 550000 },
    { model: "S36ATRS", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "12畳程度", kw: 3.6, tax_inc: 627000, tax_exc: 570000 },
    { model: "S40ATRS(P)(V)", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "14畳程度", kw: 4.0, tax_inc: 660000, tax_exc: 600000 },
    { model: "S56ATRP(V)", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "18畳程度", kw: 5.6, tax_inc: 715000, tax_exc: 650000 },
    { model: "S63ATRP(V)", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "20畳程度", kw: 6.3, tax_inc: 803000, tax_exc: 730000 },
    { model: "S71ATRP(V)", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "23畳程度", kw: 7.1, tax_inc: 880000, tax_exc: 800000 },
    { model: "S80ATRP(V)", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "26畳程度", kw: 8.0, tax_inc: 957000, tax_exc: 870000 },
    { model: "S90ATRP(V)", series: "RX SERIES", nickname: "うるさらX", year: "2026年モデル", usp: "無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル", tatami: "29畳程度", kw: 9.0, tax_inc: 1034000, tax_exc: 940000 },

    // AX SERIES
    { model: "S22ATAS", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "6畳程度", kw: 2.2, tax_inc: 473000, tax_exc: 430000 },
    { model: "S25ATAS", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "8畳程度", kw: 2.5, tax_inc: 506000, tax_exc: 460000 },
    { model: "S28ATAS", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "10畳程度", kw: 2.8, tax_inc: 539000, tax_exc: 490000 },
    { model: "S36ATAS", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "12畳程度", kw: 3.6, tax_inc: 583000, tax_exc: 530000 },
    { model: "S40ATAS(P)(V)", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "14畳程度", kw: 4.0, tax_inc: 616000, tax_exc: 560000 },
    { model: "S56ATAP(V)", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "18畳程度", kw: 5.6, tax_inc: 682000, tax_exc: 620000 },
    { model: "S63ATAP(V)", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "20畳程度", kw: 6.3, tax_inc: 781000, tax_exc: 710000 },
    { model: "S71ATAP(V)", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "23畳程度", kw: 7.1, tax_inc: 858000, tax_exc: 780000 },
    { model: "S80ATAP(V)", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "26畳程度", kw: 8.0, tax_inc: 935000, tax_exc: 850000 },
    { model: "S90ATAP(V)", series: "AX SERIES", nickname: null, year: "2026年モデル", usp: "さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル", tatami: "29畳程度", kw: 9.0, tax_inc: 1012000, tax_exc: 920000 },

    // SX SERIES (risora)
    { model: "S22ATSS", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "6畳程度", kw: 2.2, tax_inc: 396000, tax_exc: 360000 },
    { model: "S25ATSS", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "8畳程度", kw: 2.5, tax_inc: 429000, tax_exc: 390000 },
    { model: "S28ATSS", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "10畳程度", kw: 2.8, tax_inc: 462000, tax_exc: 420000 },
    { model: "S36ATSS", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "12畳程度", kw: 3.6, tax_inc: 506000, tax_exc: 460000 },
    { model: "S40ATSP(V)", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "14畳程度", kw: 4.0, tax_inc: 539000, tax_exc: 490000 },
    { model: "S56ATSP(V)", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "18畳程度", kw: 5.6, tax_inc: 649000, tax_exc: 590000 },
    { model: "S63ATSP(V)", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "20畳程度", kw: 6.3, tax_inc: 737000, tax_exc: 670000 },
    { model: "S71ATSP(V)", series: "SX SERIES", nickname: "risora", year: "2026年モデル", usp: "薄さと色で理想の空間を彩るスタイリッシュエアコン", tatami: "23畳程度", kw: 7.1, tax_inc: 814000, tax_exc: 740000 },

    // GX SERIES
    { model: "S22ATGS", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "6畳程度", kw: 2.2, tax_inc: 385000, tax_exc: 350000 },
    { model: "S25ATGS", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "8畳程度", kw: 2.5, tax_inc: 418000, tax_exc: 380000 },
    { model: "S28ATGS", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "10畳程度", kw: 2.8, tax_inc: 451000, tax_exc: 410000 },
    { model: "S36ATGS", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "12畳程度", kw: 3.6, tax_inc: 495000, tax_exc: 450000 },
    { model: "S40ATGP(V)", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "14畳程度", kw: 4.0, tax_inc: 528000, tax_exc: 480000 },
    { model: "S56ATGP(V)", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "18畳程度", kw: 5.6, tax_inc: 627000, tax_exc: 570000 },
    { model: "S63ATGP(V)", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "20畳程度", kw: 6.3, tax_inc: 715000, tax_exc: 650000 },
    { model: "S71ATGP(V)", series: "GX SERIES", nickname: null, year: "2026年モデル", usp: "快適気流・さらら除湿・クリーンなど、高い機能性が魅力", tatami: "23畳程度", kw: 7.1, tax_inc: 792000, tax_exc: 720000 },

    // CX SERIES
    { model: "S22ATCS", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "6畳程度", kw: 2.2, tax_inc: 396000, tax_exc: 360000 },
    { model: "S25ATCS", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "8畳程度", kw: 2.5, tax_inc: 429000, tax_exc: 390000 },
    { model: "S28ATCS", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "10畳程度", kw: 2.8, tax_inc: 462000, tax_exc: 420000 },
    { model: "S36ATCS", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "12畳程度", kw: 3.6, tax_inc: 506000, tax_exc: 460000 },
    { model: "S40ATCP(V)", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "14畳程度", kw: 4.0, tax_inc: 539000, tax_exc: 490000 },
    { model: "S56ATCP(V)", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "18畳程度", kw: 5.6, tax_inc: 649000, tax_exc: 590000 },
    { model: "S63ATCP(V)", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "20畳程度", kw: 6.3, tax_inc: 737000, tax_exc: 670000 },
    { model: "S71ATCP(V)", series: "CX SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実", tatami: "23畳程度", kw: 7.1, tax_inc: 814000, tax_exc: 740000 },

    // E SERIES (オープン価格)
    { model: "S22ATES", series: "E SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機採用のスタンダードモデル", tatami: "6畳程度", kw: 2.2, openPrice: true },
    { model: "S25ATES", series: "E SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機採用のスタンダードモデル", tatami: "8畳程度", kw: 2.5, openPrice: true },
    { model: "S28ATES(V)", series: "E SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機採用のスタンダードモデル", tatami: "10畳程度", kw: 2.8, openPrice: true },
    { model: "S36ATES(V)", series: "E SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機採用のスタンダードモデル", tatami: "12畳程度", kw: 3.6, openPrice: true },
    { model: "S40ATEP(V)", series: "E SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機採用のスタンダードモデル", tatami: "14畳程度", kw: 4.0, openPrice: true },
    { model: "S56ATEP(V)", series: "E SERIES", nickname: null, year: "2026年モデル", usp: "コンパクトサイズ室内機採用のスタンダードモデル", tatami: "18畳程度", kw: 5.6, openPrice: true }
];

const catalogModels = rawModels.map(item => {
    let priceObj;
    if (item.openPrice) {
        priceObj = {
            is_open_price: true,
            tax_included_yen: null,
            tax_excluded_yen: null,
            raw_text: "※オープン価格"
        };
    } else {
        priceObj = {
            is_open_price: false,
            tax_included_yen: item.tax_inc,
            tax_excluded_yen: item.tax_exc,
            raw_text: `価格 ${item.tax_inc.toLocaleString()}円 (税抜き ${item.tax_exc.toLocaleString()}円)`
        };
    }

    return {
        model_number: item.model,
        series_name: item.series,
        series_nickname: item.nickname,
        model_year: item.year,
        applicable_room_size: {
            tatami: item.tatami,
            capacity_kw: item.kw
        },
        price: priceObj,
        unique_selling_point: item.usp,
        recommended_features: recommendedFeaturesMap[item.series]
    };
});

const outputPath = path.join(process.cwd(), 'catalog_models.json');
fs.writeFileSync(outputPath, JSON.stringify(catalogModels, null, 2), 'utf8');
console.log(`Successfully generated catalog_models.json with ${catalogModels.length} models.`);
