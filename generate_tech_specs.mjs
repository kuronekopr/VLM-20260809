import fs from 'fs';
import path from 'path';

// 壁掛形 標準仕様表 (JIS C 9612:2013) P.61 記載データの構造化定義
const techSpecsRaw = [
    // --- RX SERIES (うるさらX) ---
    {
        page: 15, model: "S22ATRS", indoor: "F22ATRS", outdoor: "R22ARS", power: "単100V",
        heating: { kw: 2.5, kw_range: [0.6, 6.2], low_temp_kw: 4.5, current: 4.6, current_range: [18.0, 18.0], power_w: 440, power_range_w: [75, 1820], pf: 96, db_in: 59, db_out: 60 },
        cooling: { kw: 2.2, kw_range: [0.5, 3.3], current: 4.1, current_range: [14.0, 14.0], power_w: 390, power_range_w: [75, 850], pf: 95, db_in: 57, db_out: 58 },
        starting_current: 5.2, comp_output: 600, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 43 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 433, cooling: 170, annual: 603 }, apf: 6.9, ref: { type: "R32", kg: 0.96, gwp: 675 }
    },
    {
        page: 15, model: "S25ATRS", indoor: "F25ATRS", outdoor: "R25ARS", power: "単100V",
        heating: { kw: 2.8, kw_range: [0.6, 6.3], low_temp_kw: 4.7, current: 5.2, current_range: [18.0, 18.0], power_w: 500, power_range_w: [75, 1820], pf: 96, db_in: 61, db_out: 60 },
        cooling: { kw: 2.5, kw_range: [0.5, 3.5], current: 4.9, current_range: [14.0, 14.0], power_w: 470, power_range_w: [75, 870], pf: 95, db_in: 59, db_out: 58 },
        starting_current: 5.2, comp_output: 750, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 43 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 495, cooling: 200, annual: 695 }, apf: 6.8, ref: { type: "R32", kg: 0.96, gwp: 675 }
    },
    {
        page: 15, model: "S28ATRS", indoor: "F28ATRS", outdoor: "R28ARS", power: "単100V",
        heating: { kw: 3.6, kw_range: [0.6, 7.2], low_temp_kw: 5.7, current: 6.8, current_range: [20.0, 20.0], power_w: 660, power_range_w: [75, 2000], pf: 97, db_in: 62, db_out: 60 },
        cooling: { kw: 2.8, kw_range: [0.5, 4.0], current: 5.8, current_range: [18.8, 18.8], power_w: 550, power_range_w: [70, 1030], pf: 95, db_in: 60, db_out: 58 },
        starting_current: 6.8, comp_output: 750, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 46 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 560, cooling: 230, annual: 790 }, apf: 6.7, ref: { type: "R32", kg: 1.02, gwp: 675 }
    },
    {
        page: 15, model: "S36ATRS", indoor: "F36ATRS", outdoor: "R36ARS", power: "単100V",
        heating: { kw: 4.2, kw_range: [0.6, 7.3], low_temp_kw: 5.7, current: 8.4, current_range: [20.0, 20.0], power_w: 810, power_range_w: [65, 2000], pf: 97, db_in: 62, db_out: 57 },
        cooling: { kw: 3.6, kw_range: [0.5, 4.1], current: 8.3, current_range: [18.8, 18.8], power_w: 800, power_range_w: [65, 1020], pf: 96, db_in: 61, db_out: 58 },
        starting_current: 8.4, comp_output: 950, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 48 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 724, cooling: 308, annual: 1032 }, apf: 6.6, ref: { type: "R32", kg: 1.02, gwp: 675 }
    },
    {
        page: 15, model: "S40ATRS", indoor: "F40ATRS", outdoor: "R40ARS", power: "単100V",
        heating: { kw: 5.0, kw_range: [0.4, 7.2], low_temp_kw: 5.7, current: 10.3, current_range: [20.0, 20.0], power_w: 1000, power_range_w: [70, 2000], pf: 97, db_in: 66, db_out: 60 },
        cooling: { kw: 4.0, kw_range: [0.4, 5.3], current: 9.6, current_range: [18.8, 18.8], power_w: 920, power_range_w: [65, 1600], pf: 96, db_in: 66, db_out: 58 },
        starting_current: 10.3, comp_output: 1100, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 48 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 813, cooling: 333, annual: 1146 }, apf: 6.6, ref: { type: "R32", kg: 1.02, gwp: 675 }
    },
    {
        page: 15, model: "S40ATRP", indoor: "F40ATRP", outdoor: "R40ARP", power: "単200V",
        heating: { kw: 5.0, kw_range: [0.4, 12.1], low_temp_kw: 9.0, current: 4.5, current_range: [19.6, 19.6], power_w: 890, power_range_w: [65, 3580], pf: 98, db_in: 69, db_out: 61 },
        cooling: { kw: 4.0, kw_range: [0.3, 5.3], current: 3.9, current_range: [13.5, 13.5], power_w: 770, power_range_w: [65, 1300], pf: 98, db_in: 67, db_out: 63 },
        starting_current: 4.5, comp_output: 1100, plug: { amp: 20, shape: "エルバー" }, cores: 3, weight: { in: 16.5, out: 56 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 739, cooling: 297, annual: 1036 }, apf: 7.3, ref: { type: "R32", kg: 1.37, gwp: 675 }
    },
    {
        page: 15, model: "S40ATRV", indoor: "F40ATRV", outdoor: "R40ARV", power: "単200V(直結/室外電源)",
        heating: { kw: 5.0, kw_range: [0.4, 12.1], low_temp_kw: 9.0, current: 4.5, current_range: [19.6, 19.6], power_w: 890, power_range_w: [65, 3580], pf: 98, db_in: 69, db_out: 61 },
        cooling: { kw: 4.0, kw_range: [0.3, 5.3], current: 3.9, current_range: [13.5, 13.5], power_w: 770, power_range_w: [65, 1300], pf: 98, db_in: 67, db_out: 63 },
        starting_current: 4.5, comp_output: 1100, plug: null, cores: 3, weight: { in: 16.5, out: 56 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 739, cooling: 297, annual: 1036 }, apf: 7.3, ref: { type: "R32", kg: 1.37, gwp: 675 }
    },

    // --- AX SERIES ---
    {
        page: 17, model: "S22ATAS", indoor: "F22ATAS", outdoor: "R22AAS", power: "単100V",
        heating: { kw: 2.5, kw_range: [0.6, 6.2], low_temp_kw: 4.5, current: 4.6, current_range: [18.0, 18.0], power_w: 440, power_range_w: [75, 1820], pf: 96, db_in: 59, db_out: 60 },
        cooling: { kw: 2.2, kw_range: [0.5, 3.3], current: 4.1, current_range: [14.0, 14.0], power_w: 390, power_range_w: [75, 850], pf: 95, db_in: 57, db_out: 58 },
        starting_current: 4.6, comp_output: 600, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 35 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 433, cooling: 170, annual: 603 }, apf: 6.9, ref: { type: "R32", kg: 0.96, gwp: 675 }
    },
    {
        page: 17, model: "S25ATAS", indoor: "F25ATAS", outdoor: "R25AAS", power: "単100V",
        heating: { kw: 2.8, kw_range: [0.6, 6.3], low_temp_kw: 4.7, current: 5.2, current_range: [18.0, 18.0], power_w: 500, power_range_w: [75, 1820], pf: 96, db_in: 60, db_out: 60 },
        cooling: { kw: 2.5, kw_range: [0.5, 3.5], current: 4.9, current_range: [14.0, 14.0], power_w: 470, power_range_w: [75, 870], pf: 95, db_in: 59, db_out: 58 },
        starting_current: 5.2, comp_output: 750, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 35 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 495, cooling: 200, annual: 695 }, apf: 6.8, ref: { type: "R32", kg: 0.96, gwp: 675 }
    },
    {
        page: 17, model: "S28ATAS", indoor: "F28ATAS", outdoor: "R28AAS", power: "単100V",
        heating: { kw: 3.6, kw_range: [0.6, 7.2], low_temp_kw: 5.7, current: 6.8, current_range: [20.0, 20.0], power_w: 660, power_range_w: [75, 2000], pf: 97, db_in: 62, db_out: 57 },
        cooling: { kw: 2.8, kw_range: [0.5, 4.0], current: 5.8, current_range: [18.8, 18.8], power_w: 550, power_range_w: [70, 1030], pf: 95, db_in: 60, db_out: 58 },
        starting_current: 6.8, comp_output: 750, plug: { amp: 20, shape: "IL" }, cores: 3, weight: { in: 16, out: 38 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 560, cooling: 230, annual: 790 }, apf: 6.7, ref: { type: "R32", kg: 1.02, gwp: 675 }
    },

    // --- SX SERIES (risora) ---
    {
        page: 21, model: "S22ATSS", indoor: "F22ATSSW(K)", outdoor: "R22ASS", power: "単100V",
        heating: { kw: 2.5, kw_range: [0.7, 4.0], low_temp_kw: 2.9, current: 5.0, current_range: [13.8, 13.8], power_w: 435, power_range_w: [130, 1220], pf: 87, db_in: 61, db_out: 60 },
        cooling: { kw: 2.2, kw_range: [0.6, 2.8], current: 6.3, current_range: [11.35, 11.35], power_w: 555, power_range_w: [135, 800], pf: 88, db_in: 61, db_out: 61 },
        starting_current: 6.3, comp_output: 600, plug: { amp: 15, shape: "II" }, cores: 3, weight: { in: 9, out: 21 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 483, cooling: 222, annual: 705 }, apf: 5.9, ref: { type: "R32", kg: 0.46, gwp: 675 }
    },
    {
        page: 21, model: "S25ATSS", indoor: "F25ATSSW(K)", outdoor: "R25ASS", power: "単100V",
        heating: { kw: 2.8, kw_range: [0.7, 4.3], low_temp_kw: 3.3, current: 6.7, current_range: [14.5, 14.5], power_w: 590, power_range_w: [130, 1280], pf: 88, db_in: 61, db_out: 61 },
        cooling: { kw: 2.5, kw_range: [0.6, 3.1], current: 7.2, current_range: [11.35, 11.35], power_w: 650, power_range_w: [130, 910], pf: 90, db_in: 61, db_out: 61 },
        starting_current: 7.2, comp_output: 750, plug: { amp: 15, shape: "II" }, cores: 3, weight: { in: 9, out: 25 }, piping: { liquid: 6.4, gas: 9.5 },
        kwh: { heating: 565, cooling: 237, annual: 802 }, apf: 5.9, ref: { type: "R32", kg: 0.65, gwp: 675 }
    }
];

const technicalSpecifications = techSpecsRaw.map(item => {
    return {
        catalog_page: item.page,
        model_number: item.model,
        indoor_unit_model: item.indoor,
        outdoor_unit_model: item.outdoor,
        power_supply: item.power,
        heating: {
            rated_capacity_kw: item.heating.kw,
            capacity_range_kw: item.heating.kw_range,
            low_temp_max_capacity_kw: item.heating.low_temp_kw,
            electrical_properties: {
                max_current_a: item.heating.current,
                max_current_range_a: item.heating.current_range,
                max_power_w: item.heating.power_w,
                max_power_range_w: item.heating.power_range_w,
                power_factor_pct: item.heating.pf
            },
            sound_power_level_db: {
                indoor: item.heating.db_in,
                outdoor: item.heating.db_out
            }
        },
        cooling: {
            rated_capacity_kw: item.cooling.kw,
            capacity_range_kw: item.cooling.kw_range,
            electrical_properties: {
                max_current_a: item.cooling.current,
                max_current_range_a: item.cooling.current_range,
                max_power_w: item.cooling.power_w,
                max_power_range_w: item.cooling.power_range_w,
                power_factor_pct: item.cooling.pf
            },
            sound_power_level_db: {
                indoor: item.cooling.db_in,
                outdoor: item.cooling.db_out
            }
        },
        starting_current_a: item.starting_current,
        compressor_output_w: item.comp_output,
        power_plug: item.plug ? {
            capacity_a: item.plug.amp,
            shape_code: item.plug.shape
        } : null,
        connection_cores: item.cores,
        weight_kg: {
            indoor: item.weight.in,
            outdoor: item.weight.out
        },
        piping_diameter_mm: {
            liquid: item.piping.liquid,
            gas: item.piping.gas
        },
        annual_power_consumption_kwh: {
            heating_total: item.kwh.heating,
            cooling_total: item.kwh.cooling,
            annual_total: item.kwh.annual
        },
        apf: item.apf,
        refrigerant: {
            type: item.ref.type,
            charge_amount_kg: item.ref.kg,
            gwp: item.ref.gwp
        }
    };
});

const outputPath = path.join(process.cwd(), 'technical_spec_aircon_daikin_.json');
fs.writeFileSync(outputPath, JSON.stringify(technicalSpecifications, null, 2), 'utf8');
console.log(`Successfully generated technical_spec_aircon_daikin_.json with ${technicalSpecifications.length} Daikin tech spec models.`);
