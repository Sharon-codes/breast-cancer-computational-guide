"""Draw original scientific schematics for Chapter 4, without generated clinical imagery."""
from pathlib import Path
import io, os, tempfile
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.backends.backend_pdf import PdfPages

OUT = Path(__file__).resolve().parent / 'art'
OUT.mkdir(parents=True, exist_ok=True)
NAVY = '#162B3C'
TEAL = '#176B73'
TERRA = '#B65E45'
GRAY = '#687078'
LIGHT = '#D9DFE3'
PALE = '#F3F5F6'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12.5,'text.color':NAVY,
 'axes.labelcolor':NAVY,'axes.edgecolor':GRAY,'xtick.color':GRAY,'ytick.color':GRAY,
 'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white',
 'pdf.fonttype':42,'ps.fonttype':42,'axes.titlesize':14})
FIGS=[]

def canvas(title, height=6.6):
    fig=plt.figure(figsize=(8.0,height),dpi=300)
    ax=fig.add_axes([.055,.065,.89,.85]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    fig.text(.055,.965,title,ha='left',va='top',fontsize=16,fontweight='bold',color=NAVY)
    return fig,ax

def txt(ax,x,y,s,size=12.5,color=NAVY,weight='normal',ha='center',va='center',**kw):
    return ax.text(x,y,s,fontsize=size,color=color,fontweight=weight,ha=ha,va=va,**kw)

def arrow(ax,a,b,color=GRAY,lw=1.5,style='-',rad=0):
    p=FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=11,linewidth=lw,
       color=color,linestyle=style,connectionstyle=f'arc3,rad={rad}',shrinkA=3,shrinkB=3)
    ax.add_patch(p);return p

def box(ax,x,y,w,h,label,edge=NAVY,face='white',size=12.2,rounding=.013,lw=1.4):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0.005,rounding_size={rounding}',
      linewidth=lw,edgecolor=edge,facecolor=face))
    txt(ax,x,y,label,size=size)

def card(ax,x,y,w=.12,h=.105,label='',edge=TEAL,pattern=0):
    ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor='white',edgecolor=edge,lw=1.5))
    # Symbolic pixel grid only. No tissue or invented medical findings.
    for i in range(1,4):
        ax.plot([x-w/2+i*w/4]*2,[y-h/2,y+h/2],color=LIGHT,lw=.65)
        ax.plot([x-w/2,x+w/2],[y-h/2+i*h/4]*2,color=LIGHT,lw=.65)
    if pattern:
        ax.add_patch(Rectangle((x-w*.24,y-h*.23),w*.24,h*.23,facecolor='#CAD1D6',edgecolor='none'))
    if label:txt(ax,x,y-h/2-.021,label,size=11.2,va='top')

def atomic_bytes(path, data):
    with tempfile.NamedTemporaryFile(dir=OUT,prefix='ch04_pending_',suffix=path.suffix,delete=False) as f:
        pending=Path(f.name)
        f.write(data);f.flush();os.fsync(f.fileno())
    os.replace(pending,path)

def save(fig,name):
    png=io.BytesIO();fig.savefig(png,format='png',dpi=300,bbox_inches=None)
    with Image.open(io.BytesIO(png.getvalue())) as check:check.load()
    atomic_bytes(OUT/f'{name}.png',png.getvalue())
    with Image.open(OUT/f'{name}.png') as check:check.load()
    pdf=io.BytesIO();fig.savefig(pdf,format='pdf',bbox_inches=None)
    atomic_bytes(OUT/f'{name}.pdf',pdf.getvalue())
    FIGS.append(fig)

# 1 Hierarchy and a paired split comparison.
fig,ax=canvas('Linked images must stay with their source person',7.3)
txt(ax,.01,.985,'A  Related records',size=13.5,weight='bold',ha='left')
box(ax,.51,.905,.22,.07,'Person P017')
box(ax,.17,.795,.25,.065,'Earlier exam E0',edge=GRAY)
box(ax,.61,.795,.28,.065,'Current exam E1',edge=TEAL)
arrow(ax,(.46,.87),(.22,.83));arrow(ax,(.55,.87),(.60,.83),TEAL)
xs=[.31,.49,.67,.85]
for i,(x,l) in enumerate(zip(xs,['Left 1','Left 2','Right 1','Right 2'])):
    arrow(ax,(.61,.758),(x,.705),TEAL,lw=1.1)
    card(ax,x,.655,w=.13,h=.095,label=l,pattern=1)
card(ax,.08,.648,w=.11,h=.082,edge=GRAY)
txt(ax,.08,.573,'Linked\nprior views',size=11.2)
arrow(ax,(.17,.758),(.09,.698),GRAY,lw=1.1)
card(ax,.30,.476,w=.056,h=.046,edge=TEAL)
card(ax,.41,.476,w=.056,h=.046,edge=TEAL)
arrow(ax,(.31,.57),(.30,.505),TEAL,lw=1.1)
arrow(ax,(.33,.57),(.40,.505),TEAL,lw=1.1)
txt(ax,.355,.427,'Derived tiles',size=11.4)
ax.plot([.0,1.0],[.385,.385],color=LIGHT,lw=1.2)
txt(ax,.01,.35,'B  Split files',size=13.2,weight='bold',ha='left',color=TERRA)
txt(ax,.54,.35,'C  Split people',size=13.2,weight='bold',ha='left',color=TEAL)
for x,l in [(.12,'Training'),(.37,'Testing'),(.64,'Training'),(.89,'Testing')]:
    txt(ax,x,.294,l,size=12,weight='bold')
for x,l in [(.12,'P017\nview 1'),(.37,'P017\nview 2')]:
    box(ax,x,.207,.18,.105,l,edge=TERRA,size=11.8)
arrow(ax,(.20,.205),(.286,.205),TERRA,lw=2)
txt(ax,.245,.105,'Same person\nacross the boundary',size=11.5,color=TERRA)
box(ax,.64,.207,.19,.105,'P017\nall records',edge=TEAL,size=11.8)
box(ax,.89,.207,.19,.105,'P042\nall records',edge=TEAL,size=11.8)
ax.plot([.765,.765],[.13,.28],color=TEAL,lw=1.5,ls='--')
txt(ax,.765,.105,'One partition\nper person',size=11.5,color=TEAL)
fig.text(.055,.025,'Schematic image cards and fictional identifiers',fontsize=11,color=GRAY)
save(fig,'ch04_01')

# 2 Configuration and data travel through distinct lanes.
fig,ax=canvas('A fixed model enters a human reading workflow',7.0)
txt(ax,.01,.96,'DEVELOPMENT',size=12,weight='bold',ha='left',color=TEAL)
for x,label in [(.15,'Grouped\ntraining data'),(.50,'Learn\nparameters'),(.85,'Validate model\nand threshold')]:
    box(ax,x,.85,.25,.12,label,edge=TEAL,size=12.1)
arrow(ax,(.28,.85),(.365,.85),TEAL);arrow(ax,(.63,.85),(.715,.85),TEAL)
ax.plot([0,1],[.72,.72],color=LIGHT,lw=1.3)
txt(ax,.01,.672,'INDEPENDENT EVALUATION',size=12,weight='bold',ha='left')
# Four schematic view cards before an input check.
for dx,dy in [(-.033,.026),(.033,.026),(-.033,-.026),(.033,-.026)]:
    card(ax,.15+dx,.555+dy,w=.05,h=.042,edge=TEAL)
txt(ax,.15,.455,'Real exam\ninput checks',size=12.1)
# Feature-map stack makes the computation visually distinct from text boxes.
for off in [.018,.009,0]:
    ax.add_patch(Rectangle((.394+off,.49+off),.212,.12,facecolor=PALE,edgecolor=TEAL,lw=1.2))
txt(ax,.50,.55,'Fixed input\npreparation\nand model',size=11.7)
arrow(ax,(.25,.555),(.378,.555),TEAL)
box(ax,.85,.555,.25,.12,'Defined score\nand any marks',edge=NAVY,size=12.1)
arrow(ax,(.63,.555),(.715,.555),NAVY)
arrow(ax,(.84,.782),(.55,.625),TEAL,style='--',rad=.13)
txt(ax,.67,.70,'Frozen settings',size=11.2,color=TEAL,bbox={'facecolor':'white','edgecolor':'none','pad':1.5})
# Human decision path.
ax.add_patch(Circle((.85,.285),.075,edgecolor=NAVY,facecolor='white',lw=1.6))
txt(ax,.85,.285,'Reader',size=12.6,weight='bold')
arrow(ax,(.85,.49),(.85,.367),NAVY)
box(ax,.50,.285,.26,.115,'Record assessment\ndecision',edge=NAVY,size=12.1)
arrow(ax,(.767,.285),(.637,.285),NAVY)
box(ax,.50,.085,.26,.10,'Outcome\nfollow-up',edge=NAVY,size=12)
arrow(ax,(.50,.223),(.50,.141),NAVY)
# Failure is visibly a separate state, not a numerical score.
box(ax,.15,.285,.25,.115,'Explicit failure\nand fallback',edge=TERRA,size=12.1)
arrow(ax,(.15,.428),(.15,.349),TERRA)
txt(ax,.16,.39,'If unsupported\nor failed',size=11,color=TERRA,ha='left')
txt(ax,.15,.116,'Service follows its\npredefined fallback',size=11.2,ha='center')
txt(ax,.85,.116,'Uses original exam\nand model output',size=11.2,ha='center')
fig.text(.055,.025,'Conceptual workflow; no trained imaging model or performance is implied',fontsize=11,color=GRAY)
save(fig,'ch04_02')

# 3 Auditing uses a visible synthetic pattern pair and distinct evidence branches.
fig,ax=canvas('Separate utility from copying and release risk',7.0)
box(ax,.50,.925,.46,.085,'Documented generated batch',edge=NAVY,size=12.7)
arrow(ax,(.40,.883),(.245,.812),TEAL);arrow(ax,(.60,.883),(.755,.812),TERRA)
txt(ax,.245,.77,'UTILITY',size=14,weight='bold',color=TEAL)
txt(ax,.755,.77,'PRIVACY',size=14,weight='bold',color=TERRA)
ax.plot([.5,.5],[.22,.75],color=LIGHT,lw=1.1)
# Utility pictograms: content, variation and independent real evaluation.
for y,k,title,sub in [(.64,'1','Content','Intended finding and context'),(.48,'2','Coverage','Relevant image variation'),(.32,'3','Real test','Independent downstream task')]:
    ax.add_patch(Circle((.065,y),.028,facecolor=TEAL,edgecolor=TEAL))
    txt(ax,.065,y,k,size=11.5,color='white',weight='bold')
    txt(ax,.12,y+.02,title,size=12.8,weight='bold',ha='left')
    txt(ax,.12,y-.038,sub,size=11.2,ha='left')
# Right branch: an explicitly abstract matrix pair with a similar pattern.
pattern=np.zeros((6,6));pattern[1:5,1]=1;pattern[4,1:5]=1;pattern[1:3,4]=.45
copy=pattern.copy();copy[0,5]=.25
for cx,arr,label in [(.65,pattern,'Training record'),(.87,copy,'Generated sample')]:
    x0=cx-.075;y0=.505;w=.15;h=.15
    for i in range(6):
        for j in range(6):
            v=arr[5-i,j]; col=plt.cm.Greys(.08+.78*v)
            ax.add_patch(Rectangle((x0+j*w/6,y0+i*h/6),w/6,h/6,facecolor=col,edgecolor='white',lw=.4))
    ax.add_patch(Rectangle((x0,y0),w,h,fill=False,edgecolor=GRAY,lw=1))
    txt(ax,cx,.684,label,size=11.1)
arrow(ax,(.735,.58),(.785,.58),TERRA,lw=1.6)
txt(ax,.76,.458,'Investigate close matches',size=11.8,color=TERRA,weight='bold')
txt(ax,.76,.389,'Test specified privacy threats',size=11.2)
txt(ax,.76,.329,'Check release permissions',size=11.2)
arrow(ax,(.245,.26),(.40,.165),TEAL)
arrow(ax,(.755,.26),(.60,.165),TERRA)
box(ax,.50,.115,.76,.085,'Review evidence for the proposed use and sharing',size=12.4)
fig.text(.055,.025,'The pixel patterns are schematic, not medical images or audit results',fontsize=11,color=GRAY)
save(fig,'ch04_03')

# 4 One publication timeline, with distinct outcome tracks rather than false pooled effects.
fig,ax=canvas('MASAI follow-up changes the question answered',6.5)
txt(ax,.50,.965,'ONE RANDOMIZED SCREENING TRIAL',size=12.5,weight='bold',color=TEAL)
xs=[.16,.50,.84]
ax.plot([.16,.84],[.84,.84],color=NAVY,lw=2)
arrow(ax,(.84,.84),(.96,.84),NAVY,lw=2)
for x,year in zip(xs,['2023','2025','2026']):
    ax.scatter([x],[.84],s=130,color=TEAL,zorder=4)
    txt(ax,x,.915,year,size=16,weight='bold')
txt(ax,.16,.726,'Clinical safety\nanalysis',size=13,weight='bold')
txt(ax,.50,.726,'Screening\nperformance',size=13,weight='bold')
txt(ax,.84,.726,'Primary interval-\ncancer analysis',size=13,weight='bold')
txt(ax,.16,.64,'80,033\nrandomized',size=12.2)
txt(ax,.16,.553,'Interval outcome\npending',size=11,color=GRAY)
txt(ax,.50,.608,'105,915\nanalyzed',size=12.2)
txt(ax,.84,.608,'Rate ratio 0.88\n95% CI 0.65–1.18',size=12.2)
ax.plot([0,1],[.505,.505],color=LIGHT,lw=1.2)
# Explicit year columns keep endpoint availability distinct from effect sizes.
for x,year in zip([.57,.75,.93],['2023','2025','2026']):
    txt(ax,x,.452,year,size=11.5,weight='bold')
labels=[('Screening detection',.365),('Primary interval cancers',.235),('Mortality reduction',.105)]
for label,y in labels:
    txt(ax,.01,y,label,size=12.0,ha='left')
    ax.plot([.48,.99],[y,y],color=LIGHT,lw=1.3)
for x in [.57,.75]:ax.scatter([x],[.365],s=95,color=TEAL,zorder=4)
ax.scatter([.93],[.235],s=95,color=TEAL,zorder=4)
txt(ax,.74,.171,'Non-inferiority margin 1.20',size=11,color=TEAL)
txt(ax,.74,.043,'Not established by these analyses',size=11,color=TERRA)
fig.text(.055,.025,'Dots mark the endpoint highlighted in each report.\nPublication sequence is not to scale.',fontsize=11,color=GRAY,va='bottom')
save(fig,'ch04_04')

combined=io.BytesIO()
with PdfPages(combined) as pdf:
    for f in FIGS:pdf.savefig(f)
atomic_bytes(OUT/'ch04_figures.pdf',combined.getvalue())
for f in FIGS:plt.close(f)
print('Wrote 4 PNGs, 4 individual vector PDFs, and ch04_figures.pdf')
