"""Original scientific teaching diagrams for Chapter 8.

Conceptual relationships only. No clinical images or invented measurements.
Run with the book's primary Python runtime. Outputs are PNG and vector PDF.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

BASE = Path(__file__).resolve().parent
OUT = BASE / "art"
OUT.mkdir(parents=True, exist_ok=True)
NAVY = "#162B3C"
TEAL = "#176B73"
TERRA = "#B65E45"
GRAY = "#697780"
LIGHT = "#E3E8EA"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13,
                     "text.color": NAVY, "axes.labelcolor": NAVY,
                     "pdf.fonttype": 42, "ps.fonttype": 42,
                     "savefig.facecolor": "white"})


def canvas(height, title, subtitle=None):
    fig = plt.figure(figsize=(7.4, height), facecolor="white")
    ax = fig.add_axes([0.025, 0.08, 0.95, 0.79])
    ax.set_xlim(0, 7.4)
    ax.set_ylim(0, 6.8)
    ax.axis("off")
    fig.text(.5, .963, title, ha="center", va="top", fontsize=16, weight="bold")
    if subtitle:
        fig.text(.5, .918, subtitle, ha="center", va="top", fontsize=12.5, color=GRAY)
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=300)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)


def arrow(ax, p, q, color=GRAY, style="-", curve=0, width=1.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13,
                 lw=width, color=color, linestyle=style,
                 connectionstyle=f"arc3,rad={curve}"))


def box(ax, center, width, height, text, color=NAVY, fill="white", size=13):
    x,y=center
    ax.add_patch(FancyBboxPatch((x-width/2,y-height/2),width,height,
                 boxstyle="round,pad=0.04,rounding_size=0.07", ec=color,
                 fc=fill,lw=1.6))
    ax.text(x,y,text,ha="center",va="center",fontsize=size,linespacing=1.3)


def evidence_staircase():
    fig,ax=canvas(6.3,"One model, several evidence questions",
                  "Higher steps ask new questions; they do not guarantee success")
    rows=[
       (.55,.72,"Repeat the computation","Same inputs and configuration",
        "Scientific values match",True),
       (.88,1.95,"Internal evaluation","Reserved cases from the available dataset",
        "143 diagnostic cases evaluated",True),
       (1.21,3.18,"External evaluation","A relevant independent population",
        "Transport of performance",False),
       (1.54,4.41,"Prospective workflow","Observe use as the process occurs",
        "Users, inputs and follow-up",False),
       (1.87,5.64,"Clinical outcomes","An appropriate comparative study",
        "Benefits and harms in people",False)]
    for i,(x,y,title,question,measure,done) in enumerate(rows):
        if i:
            px,py=rows[i-1][0:2]
            ax.plot([px,px,x],[py+.13,y,y],color=LIGHT,lw=5,zorder=0)
        ax.add_patch(Circle((x,y),.10,fc=TEAL if done else "white",
                           ec=TEAL if done else TERRA,lw=2,zorder=3))
        ax.text(x+.24,y+.18,title,fontsize=14,weight="bold",va="bottom")
        ax.text(x+.24,y-.11,question,fontsize=12.5,va="top")
        ax.text(x+.24,y-.43,measure,fontsize=12.5,va="top",color=TEAL if done else GRAY)
    ax.plot([.42,1.32],[6.45,6.45],color=TEAL,lw=3)
    ax.text(1.43,6.45,"Executed companion questions",va="center",fontsize=12.5)
    fig.text(.5,.026,"Open markers: additional studies not performed by the companion.",
             ha="center",fontsize=12.5,color=GRAY)
    save(fig,"ch08_01")


def data_lineage():
    fig,ax=canvas(6.7,"Trace a number back to its inputs",
                  "Executed companion lineage; arrows show computational dependence")
    box(ax,(3.70,6.26),3.15,.66,"UCI diagnostic dataset",color=GRAY)
    box(ax,(3.70,5.18),4.25,.74,"Loader and recoding\n569 rows; malignant = 1")
    arrow(ax,(3.70,5.91),(3.70,5.59))
    box(ax,(3.70,4.10),3.65,.68,"Fixed row split + input hash")
    arrow(ax,(3.70,4.77),(3.70,4.47))
    box(ax,(1.70,2.94),2.85,.82,"426 training rows\nTraining-only selection",color=TEAL)
    box(ax,(5.70,2.94),2.85,.82,"143 heldout rows\nNo setting selection",color=TERRA)
    arrow(ax,(2.75,3.72),(1.90,3.38),color=TEAL)
    arrow(ax,(4.65,3.72),(5.50,3.38),color=TERRA)
    box(ax,(1.70,1.65),2.85,.82,"Fitted scaler\n+ logistic parameters",color=TEAL)
    box(ax,(5.70,1.65),2.85,.82,"Saved probabilities\n+ observed labels",color=TERRA)
    arrow(ax,(1.70,2.48),(1.70,2.11),color=TEAL)
    arrow(ax,(5.70,2.48),(5.70,2.11),color=TERRA)
    arrow(ax,(3.18,1.65),(4.22,1.65),color=TEAL)
    box(ax,(5.70,.50),2.85,.64,"Counts + intervals")
    arrow(ax,(5.70,1.19),(5.70,.88))
    ax.text(1.70,.42,"Saved parameters let us\nreconstruct predictions",ha="center",va="center",
            fontsize=12.5,color=GRAY)
    fig.text(.5,.022,"Rows are separated; the loader omits original patient identifiers.",
             ha="center",fontsize=12.5,color=GRAY)
    save(fig,"ch08_02")


def endpoints_change():
    fig=plt.figure(figsize=(7.4,7.2),facecolor="white")
    fig.text(.5,.965,"Keep endpoints and versions connected",ha="center",va="top",
             fontsize=16,weight="bold")
    fig.text(.06,.905,"A  Measurements answer different questions",fontsize=14,weight="bold")
    ax=fig.add_axes([.04,.54,.92,.33])
    ax.set_xlim(0,7.4); ax.set_ylim(0,3.4); ax.axis("off")
    columns=["Model\nbehaviour","Immune\nresponse","Clinical\nevents"]
    xs=[3.25,4.86,6.47]
    for x,t in zip(xs,columns): ax.text(x,3.05,t,ha="center",va="center",fontsize=12.5)
    rows=[("Ranking score",2.15),("T-cell assay",1.35),("Outcome follow-up",.55)]
    for i,(t,y) in enumerate(rows):
        ax.text(.05,y,t,va="center",fontsize=12.5)
        ax.plot([2.4,7.25],[y-.39,y-.39],color=LIGHT,lw=1)
        for j,x in enumerate(xs):
            if i==j: ax.add_patch(Circle((x,y),.13,fc=TEAL,ec=TEAL))
            else: ax.text(x,y,"—",ha="center",va="center",fontsize=14,color=GRAY)
    fig.text(.5,.512,"Filled circle: direct measurement domain, not proof of efficacy.",
             ha="center",fontsize=12.5,color=GRAY)
    fig.text(.06,.465,"B  A change triggers an evidence review",fontsize=14,weight="bold")
    a=fig.add_axes([.04,.08,.92,.35])
    a.set_xlim(0,7.4); a.set_ylim(0,3.6); a.axis("off")
    centers=[(1.30,2.75),(5.95,2.75),(5.95,.75),(1.30,.75)]
    labels=["Define\nthe change","Identify\naffected\nclaims","Choose\nnew checks","Record\nnew\nversion"]
    for c,t in zip(centers,labels):
        a.add_patch(Circle(c,.60,fc="white",ec=TEAL,lw=1.7))
        a.text(*c,t,ha="center",va="center",fontsize=12.5)
    arrow(a,(1.95,2.75),(5.30,2.75))
    arrow(a,(5.95,2.10),(5.95,1.40))
    arrow(a,(5.30,.75),(1.95,.75))
    arrow(a,(1.30,1.40),(1.30,2.10))
    a.text(3.65,1.75,"Input, model, threshold\nor product-process change",ha="center",va="center",
           fontsize=12.5,color=TERRA)
    fig.text(.5,.025,"The review determines which evidence must be renewed.",
             ha="center",fontsize=12.5,color=GRAY)
    save(fig,"ch08_03")


def permission_intersection():
    fig,ax=canvas(6.25,"Permission is an intersection of conditions",
                  "Conceptual map for a proposed research use, not a legal determination")
    circles=[((2.62,4.08),TEAL),((4.78,4.08),NAVY),((3.70,2.46),TERRA)]
    for center,col in circles:
        ax.add_patch(Circle(center,1.78,fc=col,alpha=.10,ec="none"))
        ax.add_patch(Circle(center,1.78,fc="none",ec=col,lw=1.8))
    ax.text(2.02,4.70,"Consent or\nother lawful\nbasis",ha="center",va="center",fontsize=13)
    ax.text(5.38,4.70,"Approved\nresearch\npurpose",ha="center",va="center",fontsize=13)
    ax.text(3.70,1.72,"Access and\nsharing terms",ha="center",va="center",fontsize=13)
    ax.text(3.70,3.67,"Proposed\nuse",ha="center",va="center",fontsize=14,weight="bold")
    ax.text(3.70,.10,"Assess data, derived outputs and model parameters separately.",
            ha="center",va="bottom",fontsize=12.5,color=GRAY)
    fig.text(.5,.024,"Applicable law and institutional review can add further conditions.",
             ha="center",fontsize=12.5,color=GRAY)
    save(fig,"ch08_04")


if __name__=="__main__":
    evidence_staircase()
    data_lineage()
    endpoints_change()
    permission_intersection()
    print("Created Chapter 8 diagrams as four PNG and four vector PDF files.")
