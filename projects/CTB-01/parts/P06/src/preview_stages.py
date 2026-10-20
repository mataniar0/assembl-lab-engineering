"""Display exact route configurations, cropped only for visual access; proofs remain full solids."""
from generate import draw3,plt,save_json
from model import *

def generate_stages():
 d,d5,d4,d3,u,b=inputs();crop=p02.plate_solid(box(-300,-300,300,300),225,78)
 for name in CONCEPTS:
  full=assembly(name,d,d5,d4,d3,u,b);rings={k:s for k,s in full.items() if k.startswith('P06')}
  base={k:s for k,s in full.items() if not k.startswith('P06')};ringid='P06'+name
  if name=='B':
   configs=[{**base,'P06B1':full['P06B1'].translate([0,40,6.4])},
            {**base,'P06B1':full['P06B1'],'P06B2':full['P06B2'],'P06B3':full['P06B3'].translate([0,0,6.4])},full]
   titles=['B1 start: tangent+40 / Z+6.4; closed27 present','B1/B2 seated; B3 raised6.4 before drop','All3 segments +6 stop plugs seated']
  else:
   configs=[{ringid:full[ringid]},
            {ringid:full[ringid],**{k:s for k,s in base.items() if k.startswith('L')}} ,full]
   if name=='C':configs[1].update({k:s.translate([0,0,40]) for k,s in rings.items() if '_K' in k})
   titles=['Ring held before Y_FIRST cheek closure','Six cheeks and12 spacers seated'+('; keys40mm high' if name=='C' else ''),'Final conditional real assembly; upstream out of crop']
  fig=plt.figure(figsize=(17,6),layout='constrained')
  for i,(config,title) in enumerate(zip(configs,titles),1):
   ax=fig.add_subplot(1,3,i,projection='3d',proj_type='ortho')
   for k,s in config.items():
    shown=s^crop
    if shown.volume()>1e-8:draw3(ax,shown,'#3eaaa2' if k.startswith('P06') else '#c2a983',.9 if k.startswith('P06') else .2)
   ax.set(xlim=(-150,150),ylim=(-150,150),zlim=(225,303),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((300,300,150));ax.view_init(28,35);ax.set_title(title,fontsize=9)
  fig.suptitle(f'{name}: actual route configurations / DESIGN_ONLY / Z225..303 visual crop\nExact full-solid sweeps in proofs.json; no fixture, skin, strength or approved P01 change implied',fontsize=11)
  fig.savefig(PART/'assembly'/f'{name}-route-configurations.png',dpi=110,bbox_inches='tight',pad_inches=.25);plt.close(fig)
if __name__=='__main__':generate_stages()
