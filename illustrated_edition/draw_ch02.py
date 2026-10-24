"""Draw Chapter 2 scientific teaching schematics with reproducible vector linework.
Run with CODEX_PRIMARY_RUNTIME_PYTHON. No image generation or clinical images.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Rectangle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'art'
OUT.mkdir(parents=True, exist_ok=True)
(ROOT/'reviews').mkdir(parents=True, exist_ok=True)
NAVY='#162B3C'; TEAL='#176B73'; TERRA='#B65E45'; GRAY='#6E7880'; LIGHT='#D9DFE3'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13.5,'text.color':NAVY,
 'axes.labelcolor':NAVY,'xtick.color':NAVY,'ytick.color':NAVY,
 'pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white'})
QA=[]

def text(ax,x,y,s,fs=13.5,weight='normal',color=NAVY,ha='center',va='center',**kw):
    return ax.text(x,y,s,fontsize=fs,fontweight=weight,color=color,ha=ha,va=va,**kw)

def arrow(ax,a,b,color=GRAY,lw=1.7,style='-',rad=0,ms=14):
    z=FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=ms,linewidth=lw,
       color=color,linestyle=style,connectionstyle=f'arc3,rad={rad}')
    ax.add_patch(z);return z

def node(ax,x,y,s,w=2.25,h=.85,edge=NAVY,shape='round',fs=13.5):
    if shape=='circle':
        p=Circle((x,y),h/2,facecolor='white',edgecolor=edge,linewidth=1.8)
    else:
        p=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.045,rounding_size=.1',
          facecolor='white',edgecolor=edge,linewidth=1.8)
    ax.add_patch(p);text(ax,x,y,s,fs=fs)

def save(fig,name):
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    canvas=fig.bbox
    offenders=[]
    for obj in fig.findobj(matplotlib.text.Text):
        if not obj.get_visible() or not obj.get_text():continue
        bb=obj.get_window_extent(renderer)
        if bb.x0<canvas.x0-1 or bb.y0<canvas.y0-1 or bb.x1>canvas.x1+1 or bb.y1>canvas.y1+1:
            offenders.append(obj.get_text())
    if offenders:raise ValueError(f'{name}: text outside canvas: {offenders}')
    png=OUT/f'{name}.png';pdf=OUT/f'{name}.pdf'
    fig.savefig(png,dpi=300,facecolor='white')
    fig.savefig(pdf,facecolor='white',metadata={'Title':name,'Creator':'Matplotlib scientific schematic'})
    QA.append({'id':name,'png':str(png),'pdf':str(pdf),'width_inches':fig.get_figwidth(),
       'height_inches':fig.get_figheight(),'dpi':300,'minimum_label_font_pt':13.5,'text_within_canvas':True})
    plt.close(fig)

# 1. Distinct entry routes with a selected-investigation branch.
fig=plt.figure(figsize=(7.8,6.2),facecolor='white')
ax=fig.add_axes([.035,.075,.93,.85]);ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
fig.text(.5,.965,'Two routes into breast assessment',ha='center',va='top',fontsize=17,fontweight='bold',color=NAVY)
node(ax,2.1,7.35,'No breast\nsymptoms',w=2.5,h=.85,edge=TEAL)
node(ax,7.5,7.35,'New breast\nchange',w=2.5,h=.85,edge=TERRA)
node(ax,2.1,5.95,'Screening\nprogramme',w=2.5,h=.85,edge=TEAL)
node(ax,7.5,5.95,'Clinical\nassessment',w=2.5,h=.85)
arrow(ax,(2.1,6.88),(2.1,6.45),TEAL)
arrow(ax,(7.5,6.88),(7.5,6.45),TERRA)
node(ax,2.1,3.85,'No concern\nidentified',w=2.5,h=.85,edge=TEAL)
arrow(ax,(2.1,5.48),(2.1,4.36),TEAL)
# Recall route bends toward assessment rather than being an automatic diagnosis.
arrow(ax,(3.4,5.95),(6.18,5.95),TERRA)
text(ax,4.8,6.33,'Recall',fs=13.5,color=TERRA)
node(ax,7.5,4.25,'Selected\nimaging',w=2.5,h=.85)
arrow(ax,(7.5,5.48),(7.5,4.76))
node(ax,7.5,2.55,'Biopsy if\nindicated',w=2.5,h=.85)
arrow(ax,(7.5,3.78),(7.5,3.06))
node(ax,7.5,.85,'Explained result\nand care plan',w=2.7,h=.85,edge=TEAL)
arrow(ax,(7.5,2.08),(7.5,1.36),TEAL)
# A concern can be resolved without biopsy.
ax.plot([8.8,9.55,9.55],[4.25,4.25,.85],color=GRAY,lw=1.5)
arrow(ax,(9.55,.85),(8.92,.85))
text(ax,9.65,2.55,'May resolve\nwithout biopsy',fs=13.5,ha='left',rotation=90)
node(ax,2.1,1.25,'Agreed\nscreening plan',w=2.65,h=.85,edge=TEAL)
arrow(ax,(2.1,3.38),(2.1,1.76),TEAL)
text(ax,2.5,2.6,'Within the\ntest\'s limits',fs=13.5,color=GRAY,ha='left')
fig.text(.5,.025,'Conceptual routes; clinicians select the investigations.',ha='center',fontsize=13.5,color=GRAY)
save(fig,'ch02_01')

# 2. Aligned timelines expose two observation biases.
fig=plt.figure(figsize=(7.8,6.3),facecolor='white')
fig.text(.5,.965,'Screening changes what is observed and when',ha='center',va='top',fontsize=17,fontweight='bold',color=NAVY)
fig.text(.06,.885,'A  Lead time',ha='left',fontsize=15,fontweight='bold',color=NAVY)
a=fig.add_axes([.27,.565,.67,.26]);a.set(xlim=(60,71),ylim=(0,2.6))
for y,label,diag,years in [(1.95,'Without\nscreening',65,5),(.65,'With\nscreening',62,8)]:
    a.plot([60,70],[y,y],color=LIGHT,lw=4,zorder=1)
    a.plot([diag,70],[y,y],color=TEAL,lw=4,zorder=2)
    a.scatter([diag],[y],s=72,color=TERRA,zorder=3)
    a.scatter([70],[y],marker='x',s=85,color=NAVY,zorder=3,linewidth=2)
    text(a,59.55,y,label,ha='right',fs=13.5)
    text(a,(diag+70)/2,y+.3,f'{years} years',fs=13.5)
    text(a,diag,y-.33,f'Diagnosis {diag}',fs=13.5,color=TERRA)
a.set_xticks([60,62,65,70]);a.set_xlabel('Age in years',fontsize=13.5,labelpad=5)
a.set_yticks([]);a.tick_params(axis='x',labelsize=13.5)
for spine in ['top','right','left']:a.spines[spine].set_visible(False)
a.spines['bottom'].set_color(LIGHT)
text(a,70,2.53,'Same death date',fs=13.5,ha='right')
fig.text(.06,.455,'B  Length bias',ha='left',fontsize=15,fontweight='bold',color=NAVY)
b=fig.add_axes([.27,.135,.67,.24]);b.set(xlim=(0,5),ylim=(0,2.6))
for x in [1,2,3,4]:b.axvline(x,.1,.84,color=GRAY,ls=(0,(3,3)),lw=1.2,zorder=1)
b.add_patch(Rectangle((.5,1.75),4,.3,facecolor=TEAL,edgecolor=TEAL,zorder=2))
b.add_patch(Rectangle((1.1,.55),.5,.3,facecolor=TERRA,edgecolor=TERRA,zorder=2))
text(b,-.12,1.9,'Longer\nwindow',ha='right',fs=13.5)
text(b,-.12,.7,'Shorter\nwindow',ha='right',fs=13.5)
text(b,2.5,2.42,'Scheduled examinations',fs=13.5,color=GRAY)
b.set_xticks([0,1,2,3,4,5]);b.set_xlabel('Fictional years',fontsize=13.5,labelpad=4)
b.set_yticks([]);b.tick_params(axis='x',labelsize=13.5)
for spine in ['top','right','left']:b.spines[spine].set_visible(False)
b.spines['bottom'].set_color(LIGHT)
fig.text(.5,.025,'Detectable windows and timings are invented teaching examples.',ha='center',fontsize=13.5,color=GRAY)
save(fig,'ch02_02')

# 3. Four physical measurement schematics, not synthetic clinical pictures.
fig=plt.figure(figsize=(7.8,6.8),facecolor='white')
fig.text(.5,.972,'Different images begin with different signals',ha='center',va='top',fontsize=17,fontweight='bold',color=NAVY)
positions=[(.045,.535,.425,.365),(.53,.535,.425,.365),(.045,.075,.425,.365),(.53,.075,.425,.365)]
axs=[]
for pos in positions:
    q=fig.add_axes(pos);q.set(xlim=(0,1),ylim=(0,1));q.axis('off');axs.append(q)
q=axs[0];text(q,0,.99,'A  Mammography',ha='left',va='top',fs=15,weight='bold')
q.add_patch(Circle((.1,.57),.045,facecolor=NAVY,edgecolor=NAVY))
q.add_patch(Rectangle((.38,.28),.2,.5,facecolor='white',edgecolor=GRAY,lw=1.5))
q.add_patch(Ellipse((.43,.56),.08,.18,facecolor='none',edgecolor=TERRA,lw=1.8))
q.add_patch(Ellipse((.53,.56),.08,.18,facecolor='none',edgecolor=TEAL,lw=1.8))
for y in [.4,.56,.72]:arrow(q,(.16,.57),(.82,y),NAVY,lw=1.1,ms=10)
q.plot([.85,.85],[.23,.83],color=NAVY,lw=3)
text(q,.19,.86,'X-rays',fs=13.5)
text(q,.85,.16,'Detector',fs=13.5)
text(q,.5,.045,'Projection with overlap',fs=13.5)
q=axs[1];text(q,0,.99,'B  Tomosynthesis',ha='left',va='top',fs=15,weight='bold')
for x,y in [(.17,.77),(.45,.84),(.73,.77)]:
    q.add_patch(Circle((x,y),.026,facecolor=NAVY,edgecolor=NAVY));arrow(q,(x,y-.035),(.45,.5),NAVY,lw=1.1,ms=10)
q.add_patch(Ellipse((.45,.45),.38,.18,facecolor='white',edgecolor=GRAY,lw=1.5))
q.add_patch(Ellipse((.43,.45),.05,.08,facecolor='none',edgecolor=TERRA,lw=1.7))
for k in range(3):q.add_patch(Rectangle((.68+k*.035,.19+k*.03),.17,.16,facecolor='white',edgecolor=TEAL,lw=1.5))
arrow(q,(.57,.4),(.68,.3),TEAL,lw=1.5,ms=11)
text(q,.125,.29,'Several\nangles',fs=13.5)
text(q,.5,.045,'Reconstructed sections',fs=13.5)
q=axs[2];text(q,0,.99,'C  Ultrasound',ha='left',va='top',fs=15,weight='bold')
q.add_patch(FancyBboxPatch((.08,.37),.12,.3,boxstyle='round,pad=.01,rounding_size=.03',facecolor=NAVY,edgecolor=NAVY))
q.plot([.28,.28],[.19,.79],color=GRAY,lw=2)
q.add_patch(Ellipse((.75,.53),.18,.24,facecolor='white',edgecolor=GRAY,lw=1.8))
arrow(q,(.22,.62),(.65,.62),TEAL,lw=2,ms=13)
arrow(q,(.65,.43),(.22,.43),TERRA,lw=2,ms=13)
text(q,.48,.76,'Pulse',fs=13.5,color=TEAL)
text(q,.48,.28,'Echo',fs=13.5,color=TERRA)
text(q,.5,.045,'Returning sound signals',fs=13.5)
q=axs[3];text(q,0,.99,'D  Breast MRI',ha='left',va='top',fs=15,weight='bold')
q.add_patch(Ellipse((.52,.55),.48,.43,facecolor='white',edgecolor=GRAY,lw=3))
q.add_patch(Ellipse((.52,.55),.32,.3,facecolor='white',edgecolor=LIGHT,lw=2))
q.add_patch(Ellipse((.52,.55),.1,.16,facecolor='none',edgecolor=TERRA,lw=1.8))
xx=np.linspace(.06,.3,150);q.plot(xx,.56+.035*np.sin(np.linspace(0,5*np.pi,150)),color=TEAL,lw=1.8)
arrow(q,(.27,.56),(.35,.56),TEAL,lw=1.5,ms=11)
arrow(q,(.69,.56),(.94,.56),TERRA,lw=1.8,ms=12)
text(q,.15,.72,'RF',fs=13.5,color=TEAL)
text(q,.86,.72,'Signal',fs=13.5,color=TERRA)
text(q,.52,.84,'Magnetic field',fs=13.5)
text(q,.5,.1,'Cancer detection usually\nuses IV contrast',fs=13.5)
# Light separators retain panel distinctions without turning the picture into boxes.
fig.lines.extend([plt.Line2D([.5,.5],[.07,.9],transform=fig.transFigure,color=LIGHT,lw=1),plt.Line2D([.045,.955],[.49,.49],transform=fig.transFigure,color=LIGHT,lw=1)])
save(fig,'ch02_03')

# 4. A closed information loop with a local support route for incomplete steps.
fig=plt.figure(figsize=(7.8,5.9),facecolor='white')
fig.text(.5,.965,'A recall episode needs a completed information loop',ha='center',va='top',fontsize=17,fontweight='bold',color=NAVY)
ax=fig.add_axes([.035,.085,.93,.815]);ax.set(xlim=(0,10),ylim=(0,7.5));ax.axis('off')
centres=[(5,6.55),(8,5.05),(8,2.45),(5,1.0),(2,2.45),(2,5.05)]
labels=['Recall\nshared','Assessment\narranged','Assessment\ncompleted','Outcome\nexplained','Plan\nagreed','Follow-through\nrecorded']
# Ring arrows are laid behind the labelled stages.
for i in range(6):
    x1,y1=centres[i];x2,y2=centres[(i+1)%6]
    dx=x2-x1;dy=y2-y1;dist=np.hypot(dx,dy)
    ux,uy=dx/dist,dy/dist
    cut=min(1.345/abs(ux) if ux else float('inf'),.54/abs(uy) if uy else float('inf'))+.1
    a=(x1+cut*dx/dist,y1+cut*dy/dist);b=(x2-cut*dx/dist,y2-cut*dy/dist)
    arrow(ax,a,b,TEAL,lw=1.8,rad=0,ms=14)
for i,((x,y),label) in enumerate(zip(centres,labels),1):
    node(ax,x,y,label,w=2.55,h=.9,edge=NAVY)
    ax.add_patch(Circle((x-1.05,y+.65),.2,facecolor=TEAL,edgecolor=TEAL,lw=1))
    text(ax,x-1.05,y+.65,str(i),fs=13.5,weight='bold',color='white')
node(ax,5,3.8,'Barrier or\nmissing step',w=2.55,h=.9,edge=TERRA)
text(ax,5,2.95,'Navigation and\naccess support',fs=13.5,color=TERRA)
arrow(ax,(6.34,4.02),(6.65,4.65),TERRA,lw=1.5,style=(0,(3,3)),ms=12)
arrow(ax,(6.34,3.57),(6.65,2.85),TERRA,lw=1.5,style=(0,(3,3)),ms=12)
fig.text(.5,.028,'Close the loop with the person and the care record.',ha='center',fontsize=13.5,color=GRAY)
save(fig,'ch02_04')

(ROOT/'reviews'/'ch02_art_build.json').write_text(json.dumps(QA,indent=2)+'\n')
print(json.dumps(QA,indent=2))
