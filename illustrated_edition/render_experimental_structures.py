"""Render deposited experimental coordinates without generative image tools.

The images are C-alpha traces, not electron-density maps or complete cell models.
Archive source files are kept with hashes in the plate provenance record.
"""
from pathlib import Path
import hashlib,json,shlex
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from scipy.interpolate import make_interp_spline
from PIL import Image

ROOT=Path(__file__).resolve().parent
ART=ROOT/'art';DATA=ROOT/'research'
NAVY='#162B3C';TEAL='#176B73';CORAL='#B65E45';GOLD='#B18A32';GRAY='#96A1A9'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':NAVY})

def atoms(path):
    lines=path.read_text().splitlines()
    i=next(i for i,s in enumerate(lines) if s.startswith('_atom_site.group_PDB'))
    j=i
    while lines[j].startswith('_atom_site.'):j+=1
    keys=[s.strip().split('.',1)[1] for s in lines[i:j]]
    rows=[]
    while j<len(lines) and not lines[j].startswith('#'):
        values=shlex.split(lines[j])
        if len(values)!=len(keys):raise ValueError('Unexpected mmCIF atom row')
        row=dict(zip(keys,values))
        if row['pdbx_PDB_model_num']=='1' and row['group_PDB']=='ATOM' and row['label_atom_id']=='CA' and row['label_alt_id'] in ['.','A']:
            rows.append(row)
        j+=1
    chains={}
    for row in rows:
        chains.setdefault(row['auth_asym_id'],[]).append([float(row['Cartn_'+a]) for a in ['x','y','z']])
    return {k:np.array(v) for k,v in chains.items()}

def rgb(hexcode):return tuple(int(hexcode[i:i+2],16)/255 for i in [1,3,5])

def render(chains,colors,path,rotation=None,radii=None):
    """Orthographic C-alpha traces with depth sorting, not molecular surfaces."""
    radii=radii or {}
    coords=np.concatenate(list(chains.values()));center=coords.mean(0)
    if rotation is None:
        _,_,vh=np.linalg.svd(coords-center);rotation=np.stack([vh[1],vh[0],vh[2]],axis=1)
    rotated={k:(v-center)@rotation for k,v in chains.items()}
    lines=[];depths=[];basecolors=[];widths=[]
    for key,xyz in rotated.items():
        breaks=np.flatnonzero(np.linalg.norm(np.diff(xyz,axis=0),axis=1)>5.3)+1
        for segment in np.split(xyz,breaks):
            if len(segment)<2:continue
            t=np.arange(len(segment))
            curve=make_interp_spline(t,segment,k=min(3,len(segment)-1))(np.linspace(0,len(segment)-1,len(segment)*8))
            for aa,bb in zip(curve[:-1],curve[1:]):
                lines.append([aa[:2],bb[:2]]);depths.append((aa[2]+bb[2])/2)
                basecolors.append(rgb(colors[key]));widths.append(3.2*radii.get(key,.58))
    z=np.array(depths);order=np.argsort(z);col=np.array(basecolors)
    # Depth affects display shade only, never the source coordinates.
    shade=.68+.32*(z-z.min())/(z.max()-z.min()+1e-9)
    col=np.clip(col*shade[:,None],0,1)
    fig,ax=plt.subplots(figsize=(5.8,6.3),facecolor='white')
    lc=LineCollection(np.array(lines)[order],colors=col[order],linewidths=np.array(widths)[order],capstyle='round',joinstyle='round')
    ax.add_collection(lc);ax.autoscale();ax.set_aspect('equal');ax.margins(.07);ax.axis('off')
    fig.subplots_adjust(0,0,1,1);fig.savefig(path,dpi=300,facecolor='white');plt.close(fig)


def finish_plate(chapter,renderfile,title,subtitle,legend,footnote):
    fig=plt.figure(figsize=(7.6,6.4),facecolor='white')
    ax=fig.add_axes([.03,.12,.70,.77]);ax.imshow(Image.open(renderfile));ax.axis('off')
    fig.text(.04,.965,title,weight='bold',fontsize=15,va='top')
    fig.text(.04,.91,subtitle,fontsize=11.5,va='top',color='#46535D')
    y=.73
    for color,label in legend:
        fig.add_artist(Line2D([.75,.79],[y,y],transform=fig.transFigure,color=color,lw=5,solid_capstyle='round'))
        fig.text(.81,y,label,va='center',fontsize=11)
        y-=.125
    fig.text(.04,.05,footnote,fontsize=10.5,color='#46535D',va='bottom')
    fig.savefig(ART/f'ch{chapter:02d}_plate.png',dpi=300,facecolor='white')
    fig.savefig(ART/f'ch{chapter:02d}_plate.pdf',facecolor='white')
    plt.close(fig)

def main():
    c=atoms(DATA/'1AO7.cif')
    selected={k:c[k] for k in ['A','B','C','D','E']}
    up=np.concatenate([c['D'],c['E']]).mean(0)-c['A'].mean(0);up/=np.linalg.norm(up)
    allc=np.concatenate(list(selected.values()));_,_,vh=np.linalg.svd(allc-allc.mean(0))
    right=vh[1]-up*np.dot(vh[1],up);right/=np.linalg.norm(right);toward=np.cross(right,up)
    colors={'A':GRAY,'B':'#B1A18B','C':CORAL,'D':TEAL,'E':NAVY}
    render(selected,colors,ART/'1AO7_trace.png',np.stack([right,up,toward],axis=1),{'C':1.15})
    finish_plate(5,ART/'1AO7_trace.png','A peptide HLA T cell receptor complex','Experimental X ray model  •  PDB 1AO7  •  2.60 Å',[
        (TEAL,'TCR α\nchain D'),(NAVY,'TCR β\nchain E'),(CORAL,'Viral peptide\nchain C'),(GRAY,'HLA A2\nchain A'),('#B1A18B','β2 microglobulin\nchain B')],
        'Cα traces of modeled protein fragments. Colours identify chains.\nThis viral peptide complex is an immune recognition example, not a breast cancer target.')
    c2=atoms(DATA/'8SK7.cif')
    if not all(k in c2 for k in ['A','G','X']):raise ValueError(f'Unexpected 8SK7 chains {list(c2)}')
    pick={k:c2[k] for k in ['A','G','X']};colors2={'A':GRAY,'G':TEAL,'X':CORAL}
    render(pick,colors2,ART/'8SK7_trace.png',radii={'X':.8})
    finish_plate(7,ART/'8SK7_trace.png','Experimental evidence after protein design','Cryo EM derived model  •  PDB 8SK7  •  2.93 Å',[
        (GRAY,'HA1\nchain A'),(TEAL,'HA2\nchain G'),(CORAL,'Designed binder\nchain X')],
        'One haemagglutinin protomer and one HA_20 binder are shown as Cα traces.\nOther protomers, binders, glycans and atoms are omitted. This is an influenza study.')
    records=json.loads((ROOT/'scientific_plate_sources.json').read_text())
    records=[r for r in records if r['chapter'] not in [5,7]]
    for n,pdb,credit,method in [(5,'1AO7','Garboczi DN, Ghosh P, Utz U, Fan QR, Biddison WE and Wiley DC','X ray diffraction'),(7,'8SK7','Borst AJ and Bennett NR; Watson JL et al','Electron microscopy')]:
        p=DATA/(pdb+'.cif')
        records.append({'chapter':n,'file':f'ch{n:02d}_plate.png','original_file':p.name,'source_page':'https://www.rcsb.org/structure/'+pdb,'original_url':'https://files.rcsb.org/download/'+pdb+'.cif','artist':credit,'license':'PDB coordinate data CC0 1.0','license_url':'https://creativecommons.org/publicdomain/zero/1.0/','original_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':method,'representation':'Original orthographic rendering of modeled C-alpha coordinates; no predicted coordinates generated','changes':'Selected chains and atom representation; colours and view assigned for explanation','retrieved':'2026-10-24'})
    (ROOT/'scientific_plate_sources.json').write_text(json.dumps(sorted(records,key=lambda x:x['chapter']),indent=2))
    print(json.dumps({'rendered':[5,7],'coordinate_atom_counts':{k:len(v) for k,v in selected.items()},'8SK7_selected':{k:len(v) for k,v in pick.items()}}))

if __name__=='__main__':main()
