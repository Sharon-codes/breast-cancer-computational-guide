"""Draw original Chapter 7 scientific schematics and executed-data figures.

Uses Python 3.12, Matplotlib and the saved companion CSV files.
No image generator, fabricated assay results, or generated molecular coordinates
are used. Figures 1–3 are explicitly schematic. Figure 4 recomputes rankings
from the saved fictional input features and sampled weights.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle
import numpy as np
import pandas as pd
from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
ART = ROOT / "art"
ART.mkdir(parents=True, exist_ok=True)
DATA = ROOT.parent / "results"
NAVY, TEAL, TERRA, GRAY = "#162B3C", "#176B73", "#B65E45", "#68757D"
LIGHT, PALE, WHITE = "#E5EBEF", "#EEF5F4", "#FFFFFF"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13,
    "text.color": NAVY, "axes.labelcolor": NAVY, "axes.edgecolor": GRAY,
    "xtick.color": NAVY, "ytick.color": NAVY, "pdf.fonttype": 42,
    "ps.fonttype": 42, "savefig.facecolor": WHITE,
})


def canvas(height):
    fig = plt.figure(figsize=(7.5, height), facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    return fig, ax


def text(ax, x, y, s, size=13.5, weight="normal", color=NAVY, ha="center", **kw):
    return ax.text(x, y, s, fontsize=size, fontweight=weight, color=color,
                   ha=ha, va="center", linespacing=1.14, **kw)


def arrow(ax, a, b, color=NAVY, lw=1.7, dashed=False, rad=0):
    p = FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14,
                        linewidth=lw, color=color,
                        linestyle=(0, (3, 3)) if dashed else "solid",
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(p)
    return p


def token(ax, x, y, label, color=TEAL, w=.053, h=.055):
    ax.add_patch(Rectangle((x-w/2, y-h/2), w, h, facecolor=WHITE,
                           edgecolor=color, lw=1.5))
    text(ax, x, y, label, size=13, color=color)


def mini_table(ax, x, y, arr, cellw=.043, cellh=.039):
    for i, row in enumerate(arr):
        for j, v in enumerate(row):
            ax.add_patch(Rectangle((x+j*cellw, y-i*cellh), cellw, cellh,
                                   facecolor=WHITE, edgecolor=GRAY, lw=.8))
            text(ax, x+(j+.5)*cellw, y+(.5-i)*cellh, v, size=12.5)


def figure_1():
    fig, ax = canvas(6.0)
    text(ax, .5, .955, "Different operations change different objects", 15.5, "bold")
    ys = [.77, .49, .205]
    labels = ["A  Generation", "B  Prediction", "C  Heuristic ranking"]
    for y, lab in zip(ys, labels):
        text(ax, .055, y+.12, lab, 14.2, "bold", ha="left")
    for y in [.65, .36]:
        ax.plot([.05, .95], [y, y], color=LIGHT, lw=1.3)

    # A: a learned rule samples new objects, rather than selecting one input row.
    for r in range(3):
        for k in range(4):
            ax.add_patch(Circle((.11+.036*k, .79-.035*r), .010,
                                facecolor=[TEAL, LIGHT, NAVY, LIGHT][(k+r)%4],
                                edgecolor=GRAY, lw=.5))
    text(ax, .165, .68, "Example collection", 13)
    arrow(ax, (.28, .755), (.40, .755))
    ax.add_patch(Circle((.49, .755), .055, facecolor=PALE, edgecolor=TEAL, lw=1.6))
    text(ax, .49, .755, "θ", 21)
    text(ax, .49, .675, "Learned distribution", 13)
    arrow(ax, (.56, .755), (.68, .755))
    for x, y, c in [(.74,.78,TEAL),(.81,.745,TERRA),(.87,.79,NAVY)]:
        ax.add_patch(Polygon([(x-.022,y-.018),(x+.022,y-.018),(x,y+.024)],
                             facecolor=WHITE, edgecolor=c, lw=1.7))
    text(ax, .81, .68, "New proposals", 13)

    # B: existing object and context -> one explicitly named property estimate.
    for i, h in enumerate([.032,.069,.050]):
        ax.add_patch(Rectangle((.10+.043*i,.445), .027, h,
                               facecolor=TEAL, edgecolor=WHITE))
    text(ax, .165, .405, "Existing object x", 13)
    arrow(ax, (.28,.485),(.405,.485))
    ax.add_patch(Ellipse((.49,.485), .13, .085, facecolor=WHITE, edgecolor=NAVY,lw=1.6))
    text(ax,.49,.485,"f(x, c)",14.5)
    text(ax,.49,.405,"Context c supplied",13)
    arrow(ax,(.565,.485),(.68,.485))
    ax.plot([.73,.91],[.46,.46],color=GRAY,lw=1.5)
    ax.plot([.73,.73],[.45,.47],color=GRAY,lw=1.3)
    ax.plot([.91,.91],[.45,.47],color=GRAY,lw=1.3)
    ax.scatter([.845],[.46],s=75,color=TERRA,zorder=3)
    text(ax,.82,.515,"Property estimate",13)
    text(ax,.82,.405,"Output definition matters",12.5)

    # C: fixed records -> declared weighted score -> order of the same records.
    mini_table(ax,.095,.195,[[".7",".8",".6"],[".9",".6",".2"],[".3",".4",".9"]])
    text(ax,.165,.095,"Fixed feature table",13)
    arrow(ax,(.28,.18),(.34,.18))
    text(ax,.49,.185,"w₁x₁ + w₂x₂ + w₃x₃",13.5)
    text(ax,.49,.105,"Declared preferences w",12.7)
    arrow(ax,(.62,.18),(.69,.18))
    for y, lab, length, c in [(.235,"1",.11,TEAL),(.18,"2",.075,TERRA),(.125,"3",.04,GRAY)]:
        text(ax,.73,y,lab,13)
        ax.plot([.77,.77+length],[y,y],lw=4,color=c,solid_capstyle="round")
    text(ax,.825,.07,"Ranked records",13)
    text(ax,.5,.022,"Schematic operations; displayed features and estimates are illustrative",12.2,color=GRAY)
    return fig


def figure_2():
    fig,ax=canvas(6.3)
    text(ax,.5,.958,"Two mechanisms for proposing an object",15.5,"bold")
    text(ax,.05,.885,"A  Append the next token",14.2,"bold",ha="left")
    for x,lab in zip([.105,.17,.235],["t₁","t₂","t₃"]): token(ax,x,.765,lab)
    text(ax,.17,.687,"Current prefix",13)
    arrow(ax,(.28,.765),(.355,.765))
    # Normalized toy probabilities; deliberately abstract tokens, not amino acids.
    bx=[.40,.46,.52]; probs=[.40,.35,.25]
    for x,p,lab in zip(bx,probs,["a","b","c"]):
        ax.add_patch(Rectangle((x-.017,.688),.034,p*.24,facecolor=TEAL,edgecolor=WHITE))
        text(ax,x,.663,lab,13)
        text(ax,x,.688+p*.24+.020,f"{p:.2f}",12)
    text(ax,.46,.855,"Next-token distribution",12.7)
    text(ax,.46,.615,"Illustrative probabilities",12.3,color=GRAY)
    arrow(ax,(.565,.765),(.65,.765))
    for x,lab in zip([.705,.77,.835,.90],["t₁","t₂","t₃","b"]):
        token(ax,x,.765,lab,color=TERRA if lab=="b" else TEAL)
    text(ax,.802,.687,"One sampled continuation",12.5)
    text(ax,.79,.875,"Repeat with a longer prefix",12.3,color=TERRA)

    ax.plot([.05,.95],[.55,.55],color=LIGHT,lw=1.3)
    text(ax,.05,.49,"B  Refine a noisy representation",14.2,"bold",ha="left")
    pts=np.array([[-.045,-.023],[-.024,.022],[.000,-.005],[.023,.032],[.045,.005]])
    rng=np.random.default_rng(17)
    noise=rng.normal(0,.024,pts.shape)
    for x,scale,lab in zip([.14,.38,.62,.86],[2.3,1.1,.35,0],["Noisy state","Update 1","Update 2","Proposal"]):
        q=pts+noise*scale
        ax.plot(q[:,0]+x,q[:,1]+.33,color=TEAL,lw=1.3,alpha=.85)
        ax.scatter(q[:,0]+x,q[:,1]+.33,s=35,color=TEAL,zorder=3)
        text(ax,x,.225,lab,13)
    for x in [.22,.46,.70]: arrow(ax,(x,.33),(x+.075,.33))
    text(ax,.5,.15,"A learned update can use a specified condition c",13.2)
    text(ax,.5,.075,"Abstract token and point examples, not a protein simulation",12.5,color=GRAY)
    text(ax,.5,.033,"Training teaches the update rule; sampling applies that rule",12.5,color=GRAY)
    return fig


def cell(ax,x,y,r,label,display_kind):
    ax.add_patch(Circle((x,y),r,facecolor=PALE,edgecolor=NAVY,lw=1.8))
    ax.add_patch(Circle((x-r*.3,y-r*.20),r*.3,facecolor=LIGHT,edgecolor=GRAY,lw=1))
    # Schematic HLA pedestal and groove. Peptide symbols are abstract.
    gy=y+r+.03
    ax.plot([x,x],[y+r-.008,gy-.015],color=NAVY,lw=2)
    ax.plot([x-.065,x-.045,x+.045,x+.065],[gy+.025,gy-.003,gy-.003,gy+.025],color=NAVY,lw=2)
    for i in range(5):
        xx=x-.043+i*.0215
        if i==2 and display_kind=="altered":
            ax.add_patch(Rectangle((xx-.008,gy+.004),.016,.016,facecolor=TERRA,edgecolor=TERRA))
        else:
            ax.add_patch(Circle((xx,gy+.012),.008,facecolor=TEAL,edgecolor=TEAL))
    text(ax,x,y-r-.055,label,13.3)
    return (x,gy+.028)


def figure_3():
    fig,ax=canvas(6.2)
    text(ax,.5,.96,"Changing a target creates a recognition question",15.1,"bold")
    text(ax,.5,.905,"T = original tumour target     T* = altered research proposal",12.8)
    left=cell(ax,.23,.39,.11,"Antigen-presenting cell\nshows altered target T*","altered")
    right=cell(ax,.77,.39,.11,"Tumour cell shows\noriginal target T","original")
    ax.add_patch(Circle((.50,.735),.077,facecolor=WHITE,edgecolor=TEAL,lw=2))
    text(ax,.50,.735,"T-cell\nresponse",13.2,"bold")
    # Dashed arrows encode questions, not guaranteed activation or cross-recognition.
    arrow(ax,(left[0]+.025,left[1]+.025),(.44,.68),color=TEAL,dashed=True)
    arrow(ax,(.56,.68),(right[0]-.02,right[1]+.025),color=TERRA,dashed=True)
    text(ax,.205,.73,"Can T* elicit\na response?",13.4)
    text(ax,.81,.73,"Does it recognize\ntumour target T?",13.4,color=TERRA)
    text(ax,.14,.58,"HLA",12.5)
    text(ax,.865,.58,"HLA",12.5)
    ax.plot([.08,.92],[.17,.17],color=LIGHT,lw=1.3)
    text(ax,.5,.12,"Binding to HLA, T-cell activation and tumour recognition",13)
    text(ax,.5,.078,"are different experimental questions",13,"bold")
    text(ax,.5,.025,"Schematic cell and presentation geometry; symbols are not peptide sequences",12.1,color=GRAY)
    return fig


def figure_4():
    records=pd.read_csv(DATA/"fictional_priority_sensitivity.csv")
    names=["expression_support","presentation_support","clonality_support"]
    weights=pd.read_csv(DATA/"fictional_weights.csv")[names].to_numpy()
    vals=records[names].to_numpy()
    ids=records.candidate_id.to_numpy()
    winners=ids[(vals@weights.T).argmax(axis=0)]
    counts=pd.Series(winners).value_counts()
    expected={"fictional_12":1230,"fictional_01":707,"fictional_08":52,"fictional_05":11}
    assert counts.to_dict()==expected,counts.to_dict()
    assert weights.shape==(2000,3) and np.allclose(weights.sum(axis=1),1)
    colors={"fictional_12":TEAL,"fictional_01":NAVY,"fictional_08":TERRA,"fictional_05":GRAY}
    markers={"fictional_12":"o","fictional_01":"s","fictional_08":"^","fictional_05":"D"}
    fig=plt.figure(figsize=(7.5,7.1),facecolor=WHITE)
    fig.text(.06,.97,"A  Which record ranks first at each sampled priority?",fontsize=14.2,fontweight="bold",va="top")
    ax=fig.add_axes([.08,.455,.84,.445])
    h=np.sqrt(3)/2
    ax.plot([0,1,.5,0],[0,0,h,0],color=GRAY,lw=1.5)
    xy=np.c_[weights[:,1]+.5*weights[:,2],h*weights[:,2]]
    for key in expected:
        ix=winners==key
        ax.scatter(xy[ix,0],xy[ix,1],s=9 if key!="fictional_05" else 21,
                   color=colors[key],marker=markers[key],alpha=.72,linewidths=0,label=key)
    ax.scatter([.5],[h/3],marker="*",s=120,color="white",edgecolor="black",linewidth=1,zorder=5)
    ax.annotate("Equal weights",(.5,h/3),(.89,.40),fontsize=12.6,
                arrowprops={"arrowstyle":"-","color":GRAY},ha="left",color=NAVY)
    ax.text(-.015,-.075,"Expression\nweight = 1",fontsize=12.5,ha="center",va="top",color=NAVY)
    ax.text(1.015,-.075,"Presentation\nweight = 1",fontsize=12.5,ha="center",va="top",color=NAVY)
    ax.text(.5,h+.045,"Clonality weight = 1",fontsize=12.5,ha="center",va="bottom",color=NAVY)
    ax.set(xlim=(-.16,1.16),ylim=(-.18,1.03),aspect="equal")
    ax.axis("off")

    fig.text(.06,.405,"B  First-place counts among the 2,000 saved weight draws",fontsize=14.2,fontweight="bold",va="top")
    bx=fig.add_axes([.26,.12,.66,.225])
    for i,key in enumerate(expected):
        count=expected[key]
        bx.barh(i,count,color=colors[key],height=.58)
        bx.text(count+24,i,f"{count:,}  ({count/20:.2f}%)",va="center",fontsize=12.6,color=NAVY)
    bx.set_yticks(range(4),list(expected),fontsize=12.7)
    bx.invert_yaxis()
    bx.set_xlim(0,1620)
    bx.set_xticks([0,500,1000,1500],labels=["0","500","1,000","1,500"],fontsize=12)
    bx.set_xlabel("Number of sampled weight scenarios",fontsize=12.8,labelpad=5)
    for side in ["top","right","left"]: bx.spines[side].set_visible(False)
    bx.tick_params(axis="y",length=0,pad=7)
    fig.text(.5,.025,"Executed fictional arithmetic: ranking frequency is not vaccine efficacy",ha="center",fontsize=12.2,color=GRAY)
    return fig


def save(fig,stem):
    fig.canvas.draw()
    # Check all visible text against figure bounds before writing fixed-size files.
    renderer=fig.canvas.get_renderer()
    fw,fh=fig.canvas.get_width_height()
    outside=[]
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text(): continue
        b=t.get_window_extent(renderer)
        if b.x0 < -1 or b.y0 < -1 or b.x1 > fw+1 or b.y1 > fh+1:
            outside.append(t.get_text())
    if outside: raise RuntimeError(f"Text outside {stem}: {outside}")
    png,pdf=ART/f"{stem}.png",ART/f"{stem}.pdf"
    # Render fully in memory, then verify the complete bytes were persisted.
    for path, fmt in [(png, "png"), (pdf, "pdf")]:
        buf=io.BytesIO()
        fig.savefig(buf,format=fmt,dpi=300,facecolor=WHITE)
        payload=buf.getvalue()
        with path.open("wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        if path.read_bytes()!=payload:
            raise RuntimeError(f"Incomplete file write: {path}")
    plt.close(fig)
    if len(PdfReader(pdf).pages)!=1:
        raise RuntimeError(f"Unexpected PDF page count: {pdf}")
    with Image.open(png) as im:
        im.verify()
    with Image.open(png) as im:
        meta={"png":str(png),"pdf":str(pdf),"png_dimensions_px":list(im.size),
              "png_dpi":list(im.info.get("dpi",[])),
              "png_sha256":hashlib.sha256(png.read_bytes()).hexdigest()}
    return meta


if __name__=="__main__":
    outputs={}
    for n,fn in enumerate([figure_1,figure_2,figure_3,figure_4],start=1):
        outputs[f"ch07_{n:02d}"]=save(fn(),f"ch07_{n:02d}")
    (ART/"ch07_render_checks.json").write_text(json.dumps({"figures":outputs,"status":"pass","data_counts_verified":True},indent=2)+"\n")
    print(json.dumps(outputs,indent=2))
