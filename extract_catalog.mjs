import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

function getAdcToken() {
    try {
        return execSync('gcloud auth application-default print-access-token', { encoding: 'utf8' }).trim();
    } catch (e) {
        console.error('gcloud ADC access token acquisition failed:', e);
        process.exit(1);
    }
}

const accessToken = getAdcToken();
const projectId = 'antigravity-20260726';
const location = 'us-central1';
const modelName = 'gemini-2.5-flash';

const endpoint = `https://${location}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${location}/publishers/google/models/${modelName}:generateContent`;

// Schema definition
const responseSchema = {
    type: "ARRAY",
    description: "エアコンカタログの型番ごと詳細データ配列",
    items: {
        type: "OBJECT",
        properties: {
            model_number: { type: "STRING", description: "型番 (例: S22ATRS, S40ATRS(P)(V))" },
            series_name: { type: "STRING", description: "シリーズ名 (例: RX SERIES, AX SERIES, SX SERIES, GX SERIES, CX SERIES, E SERIES)" },
            series_nickname: { type: "STRING", description: "シリーズ愛称 (例: うるさらX, risora)" },
            model_year: { type: "STRING", description: "モデル年式 (例: 2026年モデル)" },
            applicable_room_size: {
                type: "OBJECT",
                properties: {
                    tatami: { type: "STRING", description: "お部屋の広さ・畳数 (例: 6畳程度)" },
                    capacity_kw: { type: "NUMBER", description: "冷房能力 (kW) 例: 2.2" }
                },
                required: ["tatami", "capacity_kw"]
            },
            price: {
                type: "OBJECT",
                properties: {
                    is_open_price: { type: "BOOLEAN", description: "オープン価格の場合はtrue" },
                    tax_included_yen: { type: "INTEGER", description: "税込価格（円）。オープン価格の場合はnull" },
                    tax_excluded_yen: { type: "INTEGER", description: "税抜価格（円）。オープン価格の場合はnull" },
                    raw_text: { type: "STRING", description: "カタログ上の表示テキスト" }
                },
                required: ["is_open_price", "raw_text"]
            },
            unique_selling_point: {
                type: "STRING",
                description: "「2026年モデル」表記の直下にあるシリーズのキャッチコピー・特長テキスト"
            },
            recommended_features: {
                type: "OBJECT",
                description: "「おもなおすすめポイント」表の機能カテゴリ別の機能リスト",
                properties: {
                    基本運転_室外機機能: { type: "ARRAY", items: { type: "STRING" } },
                    しつど制御: { type: "ARRAY", items: { type: "STRING" } },
                    自動運転_節電運転: { type: "ARRAY", items: { type: "STRING" } },
                    気流制御: { type: "ARRAY", items: { type: "STRING" } },
                    清潔: { type: "ARRAY", items: { type: "STRING" } },
                    快適温度制御: { type: "ARRAY", items: { type: "STRING" } },
                    生活便利: { type: "ARRAY", items: { type: "STRING" } },
                    その他: { type: "ARRAY", items: { type: "STRING" } }
                },
                required: [
                    "基本運転_室外機機能",
                    "しつど制御",
                    "自動運転_節電運転",
                    "気流制御",
                    "清潔",
                    "快適温度制御",
                    "生活便利",
                    "その他"
                ]
            }
        },
        required: [
            "model_number",
            "series_name",
            "applicable_room_size",
            "price",
            "unique_selling_point",
            "recommended_features"
        ]
    }
};

async function main() {
    const imagePaths = [
        path.join(process.cwd(), 'Data', 'aircon_daikin_00001_2026_room_aircon_catalog_p0003.png'),
        path.join(process.cwd(), 'Data', 'aircon_daikin_00001_2026_room_aircon_catalog_p0004.png')
    ];

    console.log('Loading catalog images...');
    const parts = [];

    for (const imgPath of imagePaths) {
        const imageBuffer = fs.readFileSync(imgPath);
        parts.push({
            inlineData: {
                mimeType: 'image/png',
                data: imageBuffer.toString('base64')
            }
        });
    }

    const promptText = `
添付されたエアコンのカタログ画像（P.3およびP.4）から、掲載されているすべての型番について型番単位の構造化データを抽出してください。

【重要な抽出ルール】
1. 型番 (model_number): 上部の型番一覧に記載されているすべての型番（例: S22ATRS, S25ATRS, S40ATRS(P)(V), S22ATES, S28ATES(V) など）を漏れなく抽出してください。
2. シリーズ (series_name / series_nickname): 各型番が属するシリーズ名 (RX SERIES, AX SERIES, SX SERIES, GX SERIES, CX SERIES, E SERIES) と愛称 (うるさらX, risora など) を抽出してください。
3. ユニークセリングポイント (unique_selling_point): 各シリーズヘッダーにある「2026年モデル」（または「NEW 2026年モデル」）表記の直下にある説明文章テキスト（キャッチコピー）を抽出し、そのシリーズ内の全型番に付与してください。
   - 例: RX SERIES の場合は「無給水加湿と気流で快適 節電自動運転搭載のフラッグシップモデル」
   - 例: AX SERIES の場合は「さらら除湿、快適気流、節電自動運転など便利機能が充実のハイグレードモデル」
   - 例: SX SERIES の場合は「薄さと色で理想の空間を彩るスタイリッシュエアコン」
   - 例: GX SERIES の場合は「快適気流・さらら除湿・クリーンなど、高い機能性が魅力」
   - 例: CX SERIES の場合は「コンパクトサイズ室内機を採用 (2.2kW～5.6kW) 室内洗浄などクリーン機能が充実」
   - 例: E SERIES の場合は「コンパクトサイズ室内機採用のスタンダードモデル」
4. おもなおすすめポイント (recommended_features):
   - ページ下部の「おもなおすすめポイント」表を参照し、該当シリーズの列において背景色がついている・チェックされている・文字が記載されている機能をすべて抽出し、左側の「基本運転／室外機機能」「しつど制御」「自動運転／節電運転」「気流制御」「清潔」「快適温度制御」「生活便利」「その他」の各カテゴリ配列に格納してください。
5. 販売価格 (price):
   - カタログに税込価格・税抜価格が数値で記載されている場合は tax_included_yen と tax_excluded_yen を整数の数値（例: 517000, 470000）で抽出し、is_open_price: false としてください。
   - 「※オープン価格」と記載されている場合は is_open_price: true とし、価格数値は null としてください。
`;

    parts.push({ text: promptText });

    const requestBody = {
        contents: [{ role: 'user', parts: parts }],
        generationConfig: {
            responseMimeType: 'application/json',
            responseSchema: responseSchema,
            temperature: 0.1
        }
    };

    console.log('Sending request to Vertex AI Gemini VLM endpoint...');

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`API Error ${response.status}: ${errText}`);
        }

        const data = await response.json();
        const jsonText = data.candidates[0].content.parts[0].text;

        console.log('Successfully received VLM output.');

        const modelsData = JSON.parse(jsonText);
        console.log(`Extracted total ${modelsData.length} models.`);

        const outputPath = path.join(process.cwd(), 'catalog_models.json');
        fs.writeFileSync(outputPath, JSON.stringify(modelsData, null, 2), 'utf8');
        console.log(`Saved output to ${outputPath}`);

    } catch (err) {
        console.error('Error during VLM extraction:', err);
    }
}

main();
