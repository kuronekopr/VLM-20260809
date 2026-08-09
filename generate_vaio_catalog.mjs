import fs from 'fs';
import path from 'path';

// VAIO ノートパソコン カタログ概要データ (Index P.02)
const vaioRawModels = [
    {
        model: "VAIO SX14-R",
        series: "SX14-R",
        desc: "ハイエンド軽量大画面モバイル",
        size: "14.0型ワイド",
        colors: ["ディープエメラルド", "ファインブラック"],
        page: 3,
        copilot: true,
        cpu: "インテル® Core™ Ultra 5 シリーズ 3 プロセッサー"
    },
    {
        model: "VAIO SX14",
        series: "SX14",
        desc: "ハイエンド大画面モバイル",
        size: "14.0型ワイド",
        colors: ["ファインホワイト", "アーバンブロンズ", "ファインブラック", "ブライトシルバー"],
        page: 5,
        copilot: false,
        cpu: "インテル® Core™ プロセッサー"
    },
    {
        model: "VAIO SX12",
        series: "SX12",
        desc: "ハイエンドコンパクトモバイル",
        size: "12.5型ワイド",
        colors: ["アーバンブロンズ", "ファインブラック", "ブライトシルバー", "ローズゴールド"],
        page: 7,
        copilot: false,
        cpu: "インテル® Core™ プロセッサー"
    },
    {
        model: "VAIO S13",
        series: "S13",
        desc: "アドバンスドモバイル",
        size: "13.3型ワイド",
        colors: ["ブロンズ", "ブラック"],
        page: 9,
        copilot: false,
        cpu: "インテル® Core™ プロセッサー"
    },
    {
        model: "VAIO F16",
        series: "F16",
        desc: "スタンダード大画面ノート",
        size: "16.0型ワイド",
        colors: ["サテンゴールド", "ネイビーブルー", "ウォームホワイト"],
        page: 11,
        copilot: false,
        cpu: "インテル® Core™ プロセッサー"
    },
    {
        model: "VAIO F14",
        series: "F14",
        desc: "スタンダード大画面モバイル",
        size: "14.0型ワイド",
        colors: ["ネイビーブルー", "サテンゴールド", "ウォームホワイト"],
        page: 13,
        copilot: false,
        cpu: "インテル® Core™ プロセッサー"
    }
];

const catalogVaio = vaioRawModels.map(item => {
    return {
        manufacturer: "VAIO",
        product_category: "ノートパソコン",
        brand_name: "VAIO",
        model_number: item.model,
        series_name: item.series,
        category_description: item.desc,
        display_size: item.size,
        color_variations: item.colors,
        color_count: item.colors.length,
        catalog_page: item.page,
        copilot_plus_pc: item.copilot,
        processor_family: item.cpu,
        unique_selling_point: `${item.desc} (${item.size}) ${item.copilot ? "Copilot+PC対応" : ""}`.trim()
    };
});

const outputPath = path.join(process.cwd(), 'catalog_models_pc_vaio.json');
fs.writeFileSync(outputPath, JSON.stringify(catalogVaio, null, 2), 'utf8');
console.log(`Successfully generated catalog_models_pc_vaio.json with ${catalogVaio.length} VAIO laptop models.`);
