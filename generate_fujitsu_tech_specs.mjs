import fs from 'fs';
import path from 'path';

// 富士通 FMV ノートパソコン ＆ 一体型デスクトップ PC 標準仕様一覧データ (FMV Lineup P.01〜P.04)
const fujitsuTechSpecs = [
    // P.01 モバイルノートPC群
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note U (UA-K1)",
        model_number: "FMVUASK1BA",
        copilot_plus_pc: true,
        made_in_japan: true,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Basic + Office Home & Business 2024",
        display: {
            size: "14.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "ノングレア液晶 (高輝度・高色純度・広視野角)",
            touch: false
        },
        cpu: "インテル® Core™ Ultra 7 プロセッサー 258V (Pコア最大4.8GHz / 低消費電力Eコア最大3.7GHz)",
        npu: "インテル® AI Boost (最大47TOPS)",
        gpu: "インテル® Arc™ グラフィックス 140V",
        memory: "32GB (LPDDR5X-8533, 増設・交換不可)",
        storage: "約512GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
        lan: "1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "Thunderbolt™ 4 USB4 (Gen3)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen1)×2 (うち1つは電源オフUSB充電機能付)",
            "HDMI出力端子×1",
            "microSDメモリーカードスロット"
        ],
        camera: "フルHD Webカメラ (プライバシーカメラシャッター付, 有効画素数約207万画素)",
        audio: "Dolby Atmos®",
        battery_life_hours: { video_playback: 15.5, idle: 36.0 },
        dimensions_mm: { width: 308.8, depth: 209, height_min: 15.8, height_max: 17.3 },
        weight_g: 848
    },
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note U (U59-L1)",
        model_number: "FMVU59L1BA",
        copilot_plus_pc: true,
        made_in_japan: true,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "14.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "タッチパネル式 ノングレア液晶 (高輝度・高色純度・広視野角)",
            touch: true
        },
        cpu: "インテル® Core™ Ultra 5 プロセッサー 226V (Pコア最大4.5GHz / 低消費電力Eコア最大3.5GHz)",
        npu: "インテル® AI Boost (最大40TOPS)",
        gpu: "インテル® Arc™ グラフィックス 130V",
        memory: "16GB (LPDDR5X-8533, 増設・交換不可)",
        storage: "約512GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
        lan: "1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "Thunderbolt™ 4 USB4 (Gen3)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen1)×2 (うち1つは電源オフUSB充電機能付)",
            "HDMI出力端子×1",
            "microSDメモリーカードスロット"
        ],
        camera: "フルHD Webカメラ (プライバシーカメラシャッター付, 有効画素数約207万画素)",
        audio: "Dolby Atmos®",
        battery_life_hours: { video_playback: 14.5, idle: 34.0 },
        dimensions_mm: { width: 308.8, depth: 209, height_min: 15.8, height_max: 17.3 },
        weight_g: 908
    },
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note (UX-K3)",
        model_number: "FMVUX5K3BA",
        copilot_plus_pc: false,
        made_in_japan: false,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "14.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "ノングレア液晶 (高輝度・高色純度・広視野角)",
            touch: false
        },
        cpu: "インテル® Core™ Ultra 7 プロセッサー 255U (Pコア最大5.2GHz / 低消費電力コア最大2.4GHz)",
        npu: "インテル® AI Boost (最大12TOPS)",
        gpu: "インテル® グラフィックス",
        memory: "16GB (LPDDR5X-8400, 増設・交換不可)",
        storage: "約512GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
        lan: "1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "USB 3.2 (Gen2×2)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen1)×2 (うち1つは電源オフUSB充電機能付)",
            "HDMI出力端子×1",
            "microSDメモリーカードスロット"
        ],
        camera: "フルHD Webカメラ (プライバシーカメラシャッター付, 有効画素数約207万画素)",
        audio: "Dolby Atmos®",
        battery_life_hours: { video_playback: 7.0, idle: 18.0 },
        dimensions_mm: { width: 308.8, depth: 209, height_min: 16.3, height_max: 17.8 },
        weight_g: 634
    },
    // P.02 モバイル・スタンダードノートPC群
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note U (U77-K3)",
        model_numbers: ["FMVU77K3BA", "FMVU77K3WA", "FMVU77K3HA"],
        copilot_plus_pc: false,
        made_in_japan: true,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "14.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "ノングレア液晶 (高輝度・高色純度・広視野角)",
            touch: false
        },
        cpu: "インテル® Core™ Ultra 7 プロセッサー 155H (16コア/22スレッド, Pコア最大4.8GHz)",
        npu: "インテル® AI Boost (最大11TOPS)",
        gpu: "インテル® Arc™ グラフィックス",
        memory: "16GB (LPDDR5X-7467, 増設・交換不可)",
        storage: "約512GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
        lan: "1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "Thunderbolt™ 4 USB4 (Gen3)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen1)×2 (うち1つは電源オフUSB充電機能付)",
            "HDMI出力端子×1"
        ],
        camera: "フルHD Webカメラ (プライバシーカメラシャッター付)",
        battery_life_hours: { video_playback: 13.5, idle: 35.0 },
        dimensions_mm: { width: 308.8, depth: 209, height_min: 16.3, height_max: 17.8 },
        weight_g: 869
    },
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note M (M55-K3)",
        model_numbers: ["FMVM55K3BA", "FMVM55K3SA"],
        copilot_plus_pc: false,
        made_in_japan: false,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "14.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "スーパーファイン液晶 (高輝度・広視野角)",
            touch: false
        },
        cpu: "AMD Ryzen™ 5 7535U プロセッサ (6コア/12スレッド, 最大4.55GHz)",
        gpu: "AMD Radeon™ 660M",
        memory: "16GB (LPDDR5X-5500, 増設・交換不可)",
        storage: "約256GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 6E (2.4Gbps対応), Bluetooth®",
        interfaces: [
            "USB4 (Gen3)×1, USB 3.2 (Gen2)×1 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen2)×1",
            "HDMI出力端子×1"
        ],
        camera: "フルHD Webカメラ",
        battery_life_hours: { video_playback: 9.9, idle: 18.5 },
        dimensions_mm: { width: 313.4, depth: 223, height_min: 19.8, height_max: 20.4 },
        weight_g: 1300
    },
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note C (CZ-K1)",
        model_numbers: ["FMVCZK1EA", "FMVCZK1MA", "FMVCZK1SA"],
        copilot_plus_pc: false,
        made_in_japan: true,
        os: "Windows 11 Home",
        bundled_office: "Microsoft Office Home & Business 2024",
        display: {
            size: "13.3型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "フルフラットファインパネル (高輝度・高色純度・広視野角)",
            touch: false
        },
        cpu: "インテル® Core™ Ultra 5 プロセッサー 134U (12コア/14スレッド, Pコア最大4.4GHz)",
        npu: "インテル® AI Boost (最大11TOPS)",
        gpu: "インテル® グラフィックス",
        memory: "16GB (LPDDR5X-6400, 増設・交換不可)",
        storage: "約256GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
        interfaces: [
            "USB 3.2 (Gen2×2)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)"
        ],
        camera: "フルHD Webカメラ",
        battery_life_hours: { video_playback: 13.9, idle: 24.2 },
        dimensions_mm: { width: 297, depth: 210, height_min: 13.9, height_max: 13.9 },
        weight_g: 1187
    },
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note P (P75-L1)",
        model_number: "FMVP75L1HA",
        copilot_plus_pc: false,
        made_in_japan: true,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "16.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "ノングレア液晶 (高輝度・広視野角)",
            touch: false
        },
        cpu: "AMD Ryzen™ 7 250 プロセッサ (8コア/16スレッド, 最大5.1GHz)",
        npu: "AMD Ryzen™ AI (最大16TOPS)",
        gpu: "AMD Radeon™ 780M",
        memory: "16GB (LPDDR5X-7500, 増設・交換不可)",
        storage: "約512GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (2.88Gbps対応), Bluetooth®",
        interfaces: [
            "USB4 (Gen3×2)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen1)×2 (うち1つは電源オフUSB充電機能付)",
            "HDMI出力端子×1"
        ],
        camera: "5MP Webカメラ (プライバシーカメラシャッター付, 有効画素数約500万画素)",
        battery_life_hours: { video_playback: 12.3, idle: 19.3 },
        dimensions_mm: { width: 355, depth: 243, height_min: 19.7, height_max: 19.7 },
        weight_g: 1680
    },
    // P.03 大画面オールインワン
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note A (A79-L1)",
        model_number: "FMVA79L1BA",
        copilot_plus_pc: true,
        made_in_japan: true,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "16.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "フルフラットファインパネル (高輝度・高色純度・広視野角)",
            touch: false
        },
        cpu: "AMD Ryzen™ AI 7 445 プロセッサ (6コア/12スレッド, 最大4.6GHz)",
        npu: "AMD Ryzen™ AI (最大50TOPS)",
        gpu: "AMD Radeon™ 840M",
        memory: "16GB (LPDDR5X-7500, 増設・交換不可)",
        storage: "約512GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
        lan: "1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "USB4 (Gen3×2)×2 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen1)×2 (うち1つは電源オフUSB充電機能付)",
            "HDMI出力端子×1",
            "SDメモリーカード対応"
        ],
        camera: "5MP Webカメラ (プライバシーカメラシャッター付)",
        battery_life_hours: { video_playback: 15.2, idle: 24.1 },
        dimensions_mm: { width: 355, depth: 249, height_min: 19.9, height_max: 19.9 },
        weight_g: 1890
    },
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "ノートパソコン",
        series_name: "Note A (A77-K3 / A75-K3 / A53-K3)",
        model_numbers: ["FMVA77K3BA", "FMVA77K3GA", "FMVA77K3SA", "FMVA75K3BA", "FMVA75K3GA", "FMVA75K3SA", "FMVA53K3BA", "FMVA53K3SA"],
        copilot_plus_pc: false,
        made_in_japan: false,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "16.0型ワイド (狭額縁)",
            resolution: "1920×1200ドット (WUXGA)",
            finish: "スーパーファイン液晶 (高輝度・広視野角)",
            touch: false
        },
        cpu_options: [
            "AMD Ryzen™ 7 7735U プロセッサ (8コア/16スレッド, 最大4.75GHz)",
            "インテル® Core™ i7-1355U プロセッサー (10コア/12スレッド, 最大5.0GHz)",
            "インテル® Core™ i5-1335U プロセッサー (10コア/12スレッド, 最大4.6GHz)"
        ],
        optical_drive: "BDXL™対応Blu-ray Discドライブ / スーパーマルチドライブ",
        memory: "16GB (DDR5-4800 / DDR5-5200)",
        storage: "約512GB SSD / 約256GB SSD (PCIe Gen4)",
        wireless: "Wi-Fi 7 (5.76Gbps対応), Bluetooth®",
        lan: "1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "USB4 (Gen3)×1, USB 3.2 (Gen2)×1 (USB Power Delivery対応, DisplayPort Alt Mode対応)",
            "USB 3.2 (Gen1)×2 / USB 3.2 (Gen2)×1",
            "HDMI出力端子×1",
            "SDメモリーカード対応"
        ],
        battery_life_hours: { video_playback: "約4.8時間〜6.7時間", idle: "約9.4時間〜11.6時間" },
        dimensions_mm: { width: 360, depth: 243.5, height_min: 26.8, height_max: 26.8 },
        weight_g: 1900
    },
    // P.04 一体型デスクトップ
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "一体型デスクトップ",
        series_name: "Desktop F (F77-L1)",
        model_number: "FMVF77L1BA",
        copilot_plus_pc: true,
        made_in_japan: false,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "27.0型ワイド (狭額縁)",
            resolution: "2560×1440ドット (QHD)",
            finish: "スーパーファイン低反射液晶 (高解像度・高輝度・広視野角)",
            touch: false
        },
        cpu: "AMD Ryzen™ AI 7 350 プロセッサ (8コア/16スレッド, 最大5.0GHz)",
        npu: "AMD Ryzen™ AI (最大50TOPS)",
        gpu: "AMD Radeon™ 860M",
        memory: "32GB (DDR5-5600, 最大64GB)",
        storage: "約1TB SSD (PCIe Gen4)",
        optical_drive: "BDXL™対応Blu-ray Discドライブ",
        wireless: "Wi-Fi 6E (2.4Gbps対応), Bluetooth®",
        lan: "2.5GBASE-T/1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "USB 3.2 (Gen2)×1 (Type-C)",
            "USB 3.2 (Gen2)×2, USB 3.2 (Gen1)×1 (Type-A)",
            "HDMI入力端子×1, HDMI出力端子×1",
            "SDメモリーカードスロット"
        ],
        audio: "Dolby Atmos® Sound by Pioneer ツイーター搭載",
        camera: "HD Webカメラ (プライバシーカメラシャッター付)",
        dimensions_mm: { width: 616, depth: 189, height_min: 437, height_max: 438 },
        weight_g: 8000
    },
    {
        manufacturer: "富士通",
        brand_name: "FMV",
        product_category: "一体型デスクトップ",
        series_name: "Desktop F (F75-L1 / F55-L1)",
        model_numbers: ["FMVF75L1BA", "FMVF55L1WA"],
        copilot_plus_pc: false,
        made_in_japan: false,
        os: "Windows 11 Home",
        bundled_office: "Microsoft 365 Personal (24か月版) / Office Home & Business 2024",
        display: {
            size: "23.8型ワイド (狭額縁)",
            resolution: "1920×1080ドット (Full HD)",
            finish: "スーパーファイン低反射液晶 (高輝度・広視野角)",
            touch: false
        },
        cpu_options: [
            "AMD Ryzen™ 7 250 プロセッサ (8コア/16スレッド, 最大4.4GHz, NPU 16TOPS)",
            "AMD Ryzen™ 5 220 プロセッサ (6コア/12スレッド, 最大3.9GHz)"
        ],
        gpu_options: ["AMD Radeon™ 780M", "AMD Radeon™ 740M"],
        memory: "16GB (DDR5-5600, 最大64GB)",
        storage: "約512GB SSD (PCIe Gen4)",
        optical_drive: "スーパーマルチドライブ",
        wireless: "Wi-Fi 6E (2.4Gbps対応), Bluetooth®",
        lan: "2.5GBASE-T/1000BASE-T/100BASE-TX/10BASE-T準拠",
        interfaces: [
            "USB 3.2 (Gen2)×1 (Type-C)",
            "USB 3.2 (Gen2)×2, USB 3.2 (Gen1)×1 (Type-A)",
            "HDMI入力端子×1, HDMI出力端子×1",
            "SDメモリーカードスロット"
        ],
        audio: "Dolby Atmos® Sound by Pioneer ツイーター搭載",
        camera: "HD Webカメラ (プライバシーカメラシャッター付)",
        dimensions_mm: { width: 544, depth: 189, height_min: 395, height_max: 398 },
        weight_g: 6200
    }
];

const outputPath = path.join(process.cwd(), 'technical_spec_pc_fujitsu.json');
fs.writeFileSync(outputPath, JSON.stringify(fujitsuTechSpecs, null, 2), 'utf8');
console.log(`Successfully generated technical_spec_pc_fujitsu.json with ${fujitsuTechSpecs.length} Fujitsu FMV spec series.`);
