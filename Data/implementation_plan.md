# [総合実装計画] VAIO ノートパソコン「標準仕様表」データ抽出 ＆ 構造化

添付された VAIO カタログの仕様一覧ページ（仕様一覧① P.25-26 および 仕様一覧③ P.29-30）より、エアコンの仕様表 (`technical_specifications.json`) と同様に、各シリーズモデル（`VAIO SX14-R`, `VAIO S13`, `VAIO F16`, `VAIO F14`）の技術標準仕様データを抽出して `technical_specifications_vaio.json` を生成する計画です。

---

## ユーザーレビューが必要な事項

> [!IMPORTANT]
> **VAIO 標準仕様表 データ構造仕様 (`technical_specifications_vaio.json`)**
> - **対象メーカー / カテゴリー**: `manufacturer: "VAIO"`, `product_category: "ノートパソコン"`
> - **抽出対象シリーズモデル**:
>   1. `VAIO SX14-R` (Core Ultra 7 / Core Ultra 5 125H / Core Ultra 5 325U Copilot+PCモデル)
>   2. `VAIO S13` (Core 7 150U / Core 5 120U)
>   3. `VAIO F16` (16.0型 Core 7 150U / Core 5 120U)
>   4. `VAIO F14` (14.0型 Full HD Core 7 150U / Core 5 120U)
> - **仕様フィールドマッピング**:
>   - `os`: OSバージョン (`"Windows 11 Home 64ビット"` / `"Windows 11 Pro 64ビット"`)
>   - `cpu`: CPU詳細 (プロセッサー名, コア/スレッド数, 最大周波数, TDP, NPU TOPS)
>   - `display`: ディスプレイ仕様 (サイズ, 解像度, アスペクト比, 表面処理)
>   - `memory`: メモリ容量 (例: `"16GB"`, `"32GB"`)
>   - `storage`: ストレージ種別・容量 (例: `"第四世代 ハイスピードSSD 512GB"`, `"スタンダードSSD 1TB"`)
>   - `camera`: カメラ画素数 (例: `"921万画素"`, `"92万画素"`)
>   - `wireless`: Wi-Fi 規格 (`Wi-Fi 7` / `Wi-Fi 6E`) ＆ Bluetooth バージョン (`5.4` / `5.3`)
>   - `interfaces`: ポート構成 (USB Type-C Thunderbolt 4, HDMI, 有線LAN等)
>   - `battery_life_hours`: バッテリー駆動時間 (動画再生時 / アイドル時)
>   - `dimensions_mm`: 外形寸法 (幅 × 高さ × 奥行)
>   - `weight_kg`: 本体質量 (kg)
>   - `biometrics`: 生体認証 (`["指紋認証", "顔認証"]`)

---

## 変更・新規対象ファイル一覧

1. **[NEW] `generate_vaio_tech_specs.mjs`**: 仕様一覧画像（P.25-26, P.29-30）から `technical_specifications_vaio.json` を生成するスクリプト。
2. **[NEW] `technical_specifications_vaio.json`**: VAIO ノートPC各モデルの標準仕様 JSON データ。
3. **[NEW] `prompts/vaio_tech_spec_prompt.md`**: ビジネスユーザーが Gemini チャット UI で VAIO 仕様一覧画像を添付してコピペ実行できるプロンプト。
4. **[UPDATE] `process_aircon_data.py`**: 本仕様データも `c:\json_data` に自動コピー保存。

---

## 検証計画

1. **仕様データの正確性検証**:
   - OS, CPU, メモリ, ディスプレイサイズ・解像度, バッテリー駆動時間, 外形寸法, 本体質量などの数値がカタログ仕様表の値と完全に一致すること。
2. **ファイル出力と保存の検証**:
   - `technical_specifications_vaio.json` および `c:\json_data\technical_specifications_vaio.json` が正常に出力されること。
