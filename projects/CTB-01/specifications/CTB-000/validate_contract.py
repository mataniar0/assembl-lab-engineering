#!/usr/bin/env python3
"""CTB-000 data-contract checks ONLY. Not a CAD fit, material or strength test."""
import csv, json, math
from pathlib import Path
P=Path(__file__).resolve().parent
D=json.loads((P/'CTB-000_parameters.json').read_text(encoding='utf-8'))
I=json.loads((P/'CTB-000_interfaces.json').read_text(encoding='utf-8'))['interfaces']
f=D['frozen']; d=D['derived']; p=D['provisional']; F=D['coordinate_frame']
checks={
 'overall_height_sum':d['tabletop_bottom_z_mm']+f['top_total_thickness_mm']==f['table_height_mm'],
 'stack_intervals':d['bottom_skin_z_mm']==[450,456] and d['core_z_mm']==[456,494] and d['top_skin_z_mm']==[494,500],
 'core_height_38':d['core_height_mm']==f['top_total_thickness_mm']-2*f['core_and_skin_plywood_nominal_mm'],
 'parallel_leg_thickness':d['leg_outer_thickness_mm']==2*f['cheek_thickness_mm']+f['leg_inner_gap_mm'],
 'cheek_offsets_and_gap':F['cheek_t_intervals_mm']==[[-13.5,-7.5],[7.5,13.5]],
 'three_legs_120':f['leg_angles_deg']==[0,120,240],
 'six_identical_cheeks':d['cheek_total_qty']==f['leg_count']*f['cheeks_per_leg'],
 'twelve_spacers':d['spacer_total_qty']==f['leg_count']*f['spacers_per_leg'],
 'skin_diameter_342':d['skin_diameter_if_rim_around_both_skins_mm']==f['table_outer_diameter_mm']-2*f['rim_kerf_plywood_nominal_mm'],
 'rim_perimeter_computed':math.isclose(d['rim_centerline_perimeter_mm'],math.pi*d['rim_centerline_diameter_mm'],abs_tol=.001),
 'rim_requires_segmentation':d['rim_centerline_perimeter_mm']>f['stock_sheet_height_mm'],
 'sheet_dimensions_portrait':f['stock_sheet_height_mm']==800 and f['stock_sheet_width_mm']==440,
 'sheet_array_height_first':f['stock_sheet_mm']==[f['stock_sheet_height_mm'],f['stock_sheet_width_mm']],
 'rim_segment_count_for_800':d['minimum_unjoined_segment_count_for_max_800mm']==math.ceil(d['rim_centerline_perimeter_mm']/f['stock_sheet_height_mm']),
 'anchor_z_contained':all(456<=a<b<=494 for a,b in p['anchor_disc_z_ranges_mm']),
 'tongue_upper_clearance':p['upper_cheek_tongue_z_range_mm'][1]<=494,
 'Y_outside_tabletop':p['Y_connector_center_z_mm']<d['tabletop_bottom_z_mm'],
 'interface_ids_unique':len({i['id'] for i in I})==len(I),
 'interface_ids_complete':{i['id'] for i in I}=={'IF-%02d'%k for k in range(1,15)},
 'no_production_claim':D['document_status']!='PRODUCTION_APPROVED',
 'legacy_V_not_current':D['authoritative_source_policy']['decisions_in_this_baseline_override_legacy_V_leg_models'],
}
with (P/'CTB-000_parts.csv').open(encoding='utf-8-sig') as file:
    rows=list(csv.DictReader(file))
checks['part_ids_unique']=len({x['part_family_id'] for x in rows})==len(rows)
checks['part_counts_six_cheeks']=next(x['qty'] for x in rows if x['part_family_id']=='P01')=='6'
checks['part_counts_twelve_spacers']=sum(int(x['qty']) for x in rows if x['part_family_id'] in ('P02','P02B'))==12
checks['provisional_Y_overhang_flag']=p['Y_arm_end_radius_mm']>p['Y_cheek_interface_radial_limits_mm'][1]
for k,v in checks.items():print(('PASS' if v else 'FAIL')+' '+k)
print('Summary:',sum(checks.values()),'/',len(checks),'data checks passed')
raise SystemExit(0 if all(checks.values()) else 1)
