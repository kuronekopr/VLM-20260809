import fs from 'fs';
import path from 'path';

// 日立エアコン 標準仕様一覧表 (JIS C 9612:2013) データ (全37型番)
const hitachiTechSpecsData = [
    // Xシリーズ (P.20)
    { model: "RAS-XR2226S", outdoor: "RAC-XR2226S", page: 20, volt: "単相100V", heat_kw: 2.5, heat_w: 430, low_kw: 4.5, low_w: 1360, cool_kw: 2.2, cool_w: 400, comp_w: 600, start_a: 5.1, weight_in: 15.5, weight_out: 31.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 408, kwh_c: 162, kwh_t: 570, apf: 7.3, cat: "I", ref_kg: 1.08 },
    { model: "RAS-XR2526S", outdoor: "RAC-XR2526S", page: 20, volt: "単相100V", heat_kw: 2.8, heat_w: 490, low_kw: 4.5, low_w: 1360, cool_kw: 2.5, cool_w: 490, comp_w: 650, start_a: 5.7, weight_in: 15.5, weight_out: 31.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 464, kwh_c: 184, kwh_t: 648, apf: 7.3, cat: "I", ref_kg: 1.08 },
    { model: "RAS-XR2826S", outdoor: "RAC-XR2826S", page: 20, volt: "単相100V", heat_kw: 3.6, heat_w: 680, low_kw: 5.5, low_w: 1915, cool_kw: 2.8, cool_w: 560, comp_w: 750, start_a: 7.6, weight_in: 15.5, weight_out: 31.0, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 535, kwh_c: 211, kwh_t: 746, apf: 7.1, cat: "I", ref_kg: 1.08 },
    { model: "RAS-XR3626S", outdoor: "RAC-XR3626S", page: 20, volt: "単相100V", heat_kw: 4.2, heat_w: 890, low_kw: 5.5, low_w: 1915, cool_kw: 3.6, cool_w: 825, comp_w: 950, start_a: 9.6, weight_in: 15.5, weight_out: 31.0, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 744, kwh_c: 288, kwh_t: 1032, apf: 6.6, cat: "I", ref_kg: 1.08 },
    { model: "RAS-XR4026D", outdoor: "RAC-XR4026D", page: 20, volt: "単相200V", heat_kw: 5.0, heat_w: 920, low_kw: 8.9, low_w: 3560, cool_kw: 4.0, cool_w: 880, comp_w: 1100, start_a: 5.4, weight_in: 16.5, weight_out: 39.0, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 761, kwh_c: 305, kwh_t: 1066, apf: 7.1, cat: "I", ref_kg: 1.46 },
    { model: "RAS-XR5626D", outdoor: "RAC-XR5626D", page: 20, volt: "単相200V", heat_kw: 6.7, heat_w: 1480, low_kw: 8.9, low_w: 3560, cool_kw: 5.6, cool_w: 1600, comp_w: 1500, start_a: 9.4, weight_in: 16.5, weight_out: 39.0, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1169, kwh_c: 486, kwh_t: 1655, apf: 6.4, cat: "I", ref_kg: 1.46 },
    { model: "RAS-XR6326D", outdoor: "RAC-XR6326D", page: 20, volt: "単相200V", heat_kw: 7.1, heat_w: 1700, low_kw: 8.9, low_w: 3560, cool_kw: 6.3, cool_w: 1760, comp_w: 1700, start_a: 10.1, weight_in: 17.0, weight_out: 39.0, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 1368, kwh_c: 554, kwh_t: 1922, apf: 6.2, cat: "II", ref_kg: 1.55 },
    { model: "RAS-XR7126D", outdoor: "RAC-XR7126D", page: 20, volt: "単相200V", heat_kw: 8.5, heat_w: 2140, low_kw: 8.9, low_w: 3560, cool_kw: 7.1, cool_w: 2340, comp_w: 1900, start_a: 12.3, weight_in: 17.0, weight_out: 39.0, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 1614, kwh_c: 662, kwh_t: 2276, apf: 5.9, cat: "II", ref_kg: 1.55 },
    { model: "RAS-XR8026D", outdoor: "RAC-XR8026D", page: 20, volt: "単相200V", heat_kw: 9.5, heat_w: 2580, low_kw: 8.9, low_w: 3560, cool_kw: 8.0, cool_w: 2900, comp_w: 2150, start_a: 14.6, weight_in: 17.0, weight_out: 40.0, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 1849, kwh_c: 806, kwh_t: 2655, apf: 5.7, cat: "II", ref_kg: 1.62 },
    { model: "RAS-XR9026D", outdoor: "RAC-XR9026D", page: 20, volt: "単相200V", heat_kw: 10.6, heat_w: 3200, low_kw: 9.1, low_w: 3600, cool_kw: 9.0, cool_w: 3000, comp_w: 2400, start_a: 16.2, weight_in: 17.0, weight_out: 41.0, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 2334, kwh_c: 1004, kwh_t: 3338, apf: 5.1, cat: "II", ref_kg: 1.77 },

    // Wシリーズ (P.22)
    { model: "RAS-WR2226S", outdoor: "RAC-WR2226S", page: 22, volt: "単相100V", heat_kw: 2.5, heat_w: 540, low_kw: 3.0, low_w: 1160, cool_kw: 2.2, cool_w: 560, comp_w: 600, start_a: 6.6, weight_in: 10.5, weight_out: 24.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 495, kwh_c: 222, kwh_t: 717, apf: 5.8, cat: "I", ref_kg: 0.52 },
    { model: "RAS-WR2526S", outdoor: "RAC-WR2526S", page: 22, volt: "単相100V", heat_kw: 2.8, heat_w: 600, low_kw: 3.3, low_w: 1150, cool_kw: 2.5, cool_w: 650, comp_w: 650, start_a: 7.1, weight_in: 10.5, weight_out: 24.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 567, kwh_c: 248, kwh_t: 815, apf: 5.8, cat: "I", ref_kg: 0.57 },
    { model: "RAS-WR2826S", outdoor: "RAC-WR2826S", page: 22, volt: "単相100V", heat_kw: 3.6, heat_w: 880, low_kw: 3.8, low_w: 1480, cool_kw: 2.8, cool_w: 800, comp_w: 750, start_a: 9.6, weight_in: 10.5, weight_out: 24.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 644, kwh_c: 269, kwh_t: 913, apf: 5.8, cat: "I", ref_kg: 0.57 },
    { model: "RAS-WR3626S", outdoor: "RAC-WR3626S", page: 22, volt: "単相100V", heat_kw: 4.2, heat_w: 1160, low_kw: 3.8, low_w: 1480, cool_kw: 3.6, cool_w: 1390, comp_w: 950, start_a: 14.8, weight_in: 10.5, weight_out: 24.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 974, kwh_c: 416, kwh_t: 1390, apf: 4.9, cat: "I", ref_kg: 0.57 },
    { model: "RAS-WR4026D", outdoor: "RAC-WR4026D", page: 22, volt: "単相200V", heat_kw: 5.0, heat_w: 1510, low_kw: 5.5, low_w: 2550, cool_kw: 4.0, cool_w: 1530, comp_w: 1100, start_a: 8.9, weight_in: 10.5, weight_out: 33.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1081, kwh_c: 463, kwh_t: 1544, apf: 4.9, cat: "III", ref_kg: 0.74 },
    { model: "RAS-WR5626D", outdoor: "RAC-WR5626D", page: 22, volt: "単相200V", heat_kw: 6.7, heat_w: 2060, low_kw: 6.8, low_w: 3440, cool_kw: 5.6, cool_w: 2200, comp_w: 1500, start_a: 12.0, weight_in: 11.0, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1482, kwh_c: 636, kwh_t: 2118, apf: 5.0, cat: "III", ref_kg: 1.29 },

    // Gシリーズ (P.24)
    { model: "RAS-GR2226S", outdoor: "RAC-GR2226S", page: 24, volt: "単相100V", heat_kw: 2.2, heat_w: 470, low_kw: 2.8, low_w: 1100, cool_kw: 2.2, cool_w: 580, comp_w: 600, start_a: 6.8, weight_in: 9.0, weight_out: 19.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 488, kwh_c: 229, kwh_t: 717, apf: 5.8, cat: "I", ref_kg: 0.50 },
    { model: "RAS-GR2526S", outdoor: "RAC-GR2526S", page: 24, volt: "単相100V", heat_kw: 2.8, heat_w: 650, low_kw: 3.0, low_w: 1120, cool_kw: 2.5, cool_w: 710, comp_w: 650, start_a: 8.4, weight_in: 9.0, weight_out: 19.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 567, kwh_c: 248, kwh_t: 815, apf: 5.8, cat: "I", ref_kg: 0.68 },
    { model: "RAS-GR2826S", outdoor: "RAC-GR2826S", page: 24, volt: "単相100V", heat_kw: 3.6, heat_w: 880, low_kw: 3.4, low_w: 1480, cool_kw: 2.8, cool_w: 790, comp_w: 750, start_a: 10.4, weight_in: 9.0, weight_out: 23.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 648, kwh_c: 265, kwh_t: 913, apf: 5.8, cat: "I", ref_kg: 0.68 },
    { model: "RAS-GR3626S", outdoor: "RAC-GR3626S", page: 24, volt: "単相100V", heat_kw: 4.2, heat_w: 1190, low_kw: 3.4, low_w: 1480, cool_kw: 3.6, cool_w: 1330, comp_w: 950, start_a: 14.1, weight_in: 9.0, weight_out: 24.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 981, kwh_c: 409, kwh_t: 1390, apf: 4.9, cat: "I", ref_kg: 0.62 },
    { model: "RAS-GR4026D", outdoor: "RAC-GR4026D", page: 24, volt: "単相200V", heat_kw: 5.0, heat_w: 1450, low_kw: 5.3, low_w: 2550, cool_kw: 4.0, cool_w: 1430, comp_w: 1100, start_a: 8.4, weight_in: 9.0, weight_out: 33.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1106, kwh_c: 438, kwh_t: 1544, apf: 4.9, cat: "III", ref_kg: 0.74 },
    { model: "RAS-GR5626D", outdoor: "RAC-GR5626D", page: 24, volt: "単相200V", heat_kw: 6.7, heat_w: 2020, low_kw: 6.7, low_w: 3280, cool_kw: 5.6, cool_w: 2170, comp_w: 1500, start_a: 11.8, weight_in: 10.0, weight_out: 35.0, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1482, kwh_c: 636, kwh_t: 2118, apf: 5.0, cat: "III", ref_kg: 0.91 },
    { model: "RAS-GR6326D", outdoor: "RAC-GR6326D", page: 24, volt: "単相200V", heat_kw: 7.1, heat_w: 2150, low_kw: 6.8, low_w: 3250, cool_kw: 6.3, cool_w: 2150, comp_w: 1700, start_a: 11.4, weight_in: 10.5, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 1680, kwh_c: 703, kwh_t: 2383, apf: 5.0, cat: "III", ref_kg: 1.36 },
    { model: "RAS-GR7126D", outdoor: "RAC-GR7126D", page: 24, volt: "単相200V", heat_kw: 8.5, heat_w: 2980, low_kw: 6.9, low_w: 3300, cool_kw: 7.1, cool_w: 2830, comp_w: 1900, start_a: 15.7, weight_in: 10.5, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 2163, kwh_c: 821, kwh_t: 2984, apf: 4.5, cat: "III", ref_kg: 1.36 },

    // Dシリーズ (P.26)
    { model: "RAS-DR2226S", outdoor: "RAC-DR2226S", page: 26, volt: "単相100V", heat_kw: 2.2, heat_w: 470, low_kw: 2.8, low_w: 1100, cool_kw: 2.2, cool_w: 635, comp_w: 600, start_a: 7.5, weight_in: 7.5, weight_out: 19.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 502, kwh_c: 215, kwh_t: 717, apf: 5.8, cat: "I", ref_kg: 0.50 },
    { model: "RAS-DR2526S", outdoor: "RAC-DR2526S", page: 26, volt: "単相100V", heat_kw: 2.8, heat_w: 650, low_kw: 3.0, low_w: 1120, cool_kw: 2.5, cool_w: 710, comp_w: 650, start_a: 8.4, weight_in: 8.0, weight_out: 23.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 567, kwh_c: 248, kwh_t: 815, apf: 5.8, cat: "I", ref_kg: 0.68 },
    { model: "RAS-DR2826S", outdoor: "RAC-DR2826S", page: 26, volt: "単相100V", heat_kw: 3.6, heat_w: 930, low_kw: 3.4, low_w: 1340, cool_kw: 2.8, cool_w: 850, comp_w: 750, start_a: 10.9, weight_in: 8.0, weight_out: 23.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 647, kwh_c: 282, kwh_t: 929, apf: 5.7, cat: "I", ref_kg: 0.68 },
    { model: "RAS-DR3626S", outdoor: "RAC-DR3626S", page: 26, volt: "単相100V", heat_kw: 4.2, heat_w: 1220, low_kw: 3.4, low_w: 1340, cool_kw: 3.6, cool_w: 1330, comp_w: 950, start_a: 14.3, weight_in: 8.0, weight_out: 24.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 988, kwh_c: 402, kwh_t: 1390, apf: 4.9, cat: "I", ref_kg: 0.62 },
    { model: "RAS-DR4026D", outdoor: "RAC-DR4026D", page: 26, volt: "単相200V", heat_kw: 5.0, heat_w: 1480, low_kw: 5.3, low_w: 2350, cool_kw: 4.0, cool_w: 1430, comp_w: 1100, start_a: 8.6, weight_in: 8.0, weight_out: 33.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1090, kwh_c: 454, kwh_t: 1544, apf: 4.9, cat: "III", ref_kg: 0.74 },
    { model: "RAS-DR5626D", outdoor: "RAC-DR5626D", page: 26, volt: "単相200V", heat_kw: 6.7, heat_w: 2020, low_kw: 6.7, low_w: 3280, cool_kw: 5.6, cool_w: 2170, comp_w: 1500, start_a: 12.5, weight_in: 8.5, weight_out: 35.0, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1458, kwh_c: 660, kwh_t: 2118, apf: 5.0, cat: "III", ref_kg: 0.89 },
    { model: "RAS-DR6326D", outdoor: "RAC-DR6326D", page: 26, volt: "単相200V", heat_kw: 7.1, heat_w: 2150, low_kw: 6.8, low_w: 3150, cool_kw: 6.3, cool_w: 2150, comp_w: 1700, start_a: 10.9, weight_in: 9.0, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 1693, kwh_c: 690, kwh_t: 2383, apf: 5.0, cat: "III", ref_kg: 1.36 },
    { model: "RAS-DR7126D", outdoor: "RAC-DR7126D", page: 26, volt: "単相200V", heat_kw: 8.5, heat_w: 2980, low_kw: 6.9, low_w: 3200, cool_kw: 7.1, cool_w: 2830, comp_w: 1900, start_a: 15.1, weight_in: 9.0, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 2131, kwh_c: 853, kwh_t: 2984, apf: 4.5, cat: "III", ref_kg: 1.36 },

    // Eシリーズ (P.28)
    { model: "RAS-ER2226S", outdoor: "RAC-ER2226S", page: 28, volt: "単相100V", heat_kw: 2.2, heat_w: 430, low_kw: 3.1, low_w: 1090, cool_kw: 2.2, cool_w: 480, comp_w: 600, start_a: 5.6, weight_in: 9.0, weight_out: 21.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 442, kwh_c: 188, kwh_t: 630, apf: 6.6, cat: "I", ref_kg: 0.68 },
    { model: "RAS-ER2526S", outdoor: "RAC-ER2526S", page: 28, volt: "単相100V", heat_kw: 2.8, heat_w: 560, low_kw: 3.3, low_w: 1160, cool_kw: 2.5, cool_w: 550, comp_w: 650, start_a: 6.4, weight_in: 9.0, weight_out: 26.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 506, kwh_c: 211, kwh_t: 717, apf: 6.6, cat: "I", ref_kg: 0.72 },
    { model: "RAS-ER2826S", outdoor: "RAC-ER2826S", page: 28, volt: "単相100V", heat_kw: 3.6, heat_w: 790, low_kw: 3.8, low_w: 1250, cool_kw: 2.8, cool_w: 630, comp_w: 750, start_a: 8.8, weight_in: 9.0, weight_out: 30.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 575, kwh_c: 227, kwh_t: 802, apf: 6.6, cat: "I", ref_kg: 0.85 },
    { model: "RAS-ER3626S", outdoor: "RAC-ER3626S", page: 28, volt: "単相100V", heat_kw: 4.2, heat_w: 890, low_kw: 4.2, low_w: 1300, cool_kw: 3.6, cool_w: 825, comp_w: 950, start_a: 9.6, weight_in: 11.0, weight_out: 32.0, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 724, kwh_c: 308, kwh_t: 1032, apf: 6.6, cat: "I", ref_kg: 0.98 },
    { model: "RAS-ER4026D", outdoor: "RAC-ER4026D", page: 28, volt: "単相200V", heat_kw: 5.0, heat_w: 1040, low_kw: 6.9, low_w: 2600, cool_kw: 4.0, cool_w: 890, comp_w: 1100, start_a: 6.0, weight_in: 12.0, weight_out: 40.5, plug: "15A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 822, kwh_c: 324, kwh_t: 1146, apf: 6.6, cat: "III", ref_kg: 1.55 },
    { model: "RAS-ER5626D", outdoor: "RAC-ER5626D", page: 28, volt: "単相200V", heat_kw: 6.7, heat_w: 1510, low_kw: 7.0, low_w: 2650, cool_kw: 5.6, cool_w: 1650, comp_w: 1500, start_a: 9.5, weight_in: 12.0, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 9.52, kwh_h: 1195, kwh_c: 486, kwh_t: 1681, apf: 6.3, cat: "III", ref_kg: 1.55 },
    { model: "RAS-ER6326D", outdoor: "RAC-ER6326D", page: 28, volt: "単相200V", heat_kw: 7.1, heat_w: 1700, low_kw: 7.1, low_w: 2700, cool_kw: 6.3, cool_w: 1780, comp_w: 1700, start_a: 9.0, weight_in: 12.0, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 1383, kwh_c: 570, kwh_t: 1953, apf: 6.1, cat: "III", ref_kg: 1.58 },
    { model: "RAS-ER7126D", outdoor: "RAC-ER7126D", page: 28, volt: "単相200V", heat_kw: 8.5, heat_w: 2150, low_kw: 7.2, low_w: 2800, cool_kw: 7.1, cool_w: 2350, comp_w: 1900, start_a: 11.6, weight_in: 12.0, weight_out: 40.5, plug: "20A", pipe_l: 6.35, pipe_g: 12.7, kwh_h: 1604, kwh_c: 672, kwh_t: 2276, apf: 5.9, cat: "III", ref_kg: 1.58 }
];

const getSeriesNameFromModel = (model) => {
    if (model.includes('-XR')) return 'Xシリーズ';
    if (model.includes('-WR')) return 'Wシリーズ';
    if (model.includes('-GR')) return 'Gシリーズ';
    if (model.includes('-DR')) return 'Dシリーズ';
    if (model.includes('-ER')) return 'Eシリーズ';
    return '白くまくん';
};

const technicalSpecificationsHitachi = hitachiTechSpecsData.map(item => {
    return {
        manufacturer: "日立",
        product_category: "壁掛形ルームエアコン",
        brand_name: "白くまくん",
        model_number: item.model,
        series_name: getSeriesNameFromModel(item.model),
        catalog_page: item.page,
        indoor_unit_model: item.model,
        outdoor_unit_model: item.outdoor,
        power_supply: item.volt,
        heating: {
            rated_capacity_kw: item.heat_kw,
            rated_power_w: item.heat_w,
            low_temp_2c: {
                capacity_kw: item.low_kw,
                power_w: item.low_w
            }
        },
        cooling: {
            rated_capacity_kw: item.cool_kw,
            rated_power_w: item.cool_w
        },
        compressor_output_w: item.comp_w,
        starting_current_a: item.start_a,
        weight_kg: {
            indoor: item.weight_in,
            outdoor: item.weight_out
        },
        power_plug: item.plug,
        piping_diameter_mm: {
            liquid: item.pipe_l,
            gas: item.pipe_g
        },
        annual_power_consumption_kwh: {
            heating: item.kwh_h,
            cooling: item.kwh_c,
            annual_total: item.kwh_t
        },
        apf: item.apf,
        energy_saving_class: item.cat,
        refrigerant: {
            type: "R32",
            charge_amount_kg: item.ref_kg,
            gwp: 675
        }
    };
});

const outputPath = path.join(process.cwd(), 'technical_specifications_hitachi.json');
fs.writeFileSync(outputPath, JSON.stringify(technicalSpecificationsHitachi, null, 2), 'utf8');
console.log(`Successfully generated technical_specifications_hitachi.json with ${technicalSpecificationsHitachi.length} models.`);
