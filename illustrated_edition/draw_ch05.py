"""Draw four reviewed scientific schematics for Chapter 5.

These are deterministic explanatory diagrams, not patient data, biological
sequence designs, microscopy, or generated narrative artwork.
Run with Python 3.12 and the recorded dependencies.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Rectangle, Polygon
)
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "art"
OUT.mkdir(parents=True, exist_ok=True)
NAVY = "#162B3C"
TEAL = "#176B73"
TERRA = "#B65E45"
GRAY = "#68737B"
LIGHT = "#EEF2F3"
TEAL_LIGHT = "#E5F1F0"
TERRA_LIGHT = "#F5EAE4"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12.5,
    "text.color": NAVY, "axes.edgecolor": NAVY,
    "pdf.fonttype": 42, "ps.fonttype": 42,
})

def setup(height):
    fig, ax = plt.subplots(figsize=(8, height))
    fig.patch.set_facecolor("white")
    ax.set(xlim=(0, 10), ylim=(0, 10))
    ax.set_axis_off()
    fig.subplots_adjust(left=.025, right=.975, top=.975, bottom=.025)
    return fig, ax

def label(ax, x, y, s, size=12.5, weight="normal", color=NAVY,
          ha="center", va="center", **kwargs):
    return ax.text(x, y, s, fontsize=size, fontweight=weight, color=color,
                   ha=ha, va=va, linespacing=1.18, **kwargs)

def box(ax, x, y, w, h, s, fc="white", ec=NAVY, size=12.5,
        lw=1.4, radius=.12, weight="normal"):
    patch = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(patch)
    label(ax, x+w/2, y+h/2, s, size=size, weight=weight)
    return patch

def arrow(ax, start, end, color=NAVY, style="-|>", lw=1.5,
          connectionstyle="arc3", dashed=False):
    p = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=13,
        linewidth=lw, color=color, connectionstyle=connectionstyle,
        linestyle="--" if dashed else "-")
    ax.add_patch(p)
    return p

def vial(ax, x, y, code, subtitle):
    ax.add_patch(FancyBboxPatch((x-.32, y-.52), .64, .96,
        boxstyle="round,pad=.01,rounding_size=.10",
        fc="white", ec=NAVY, lw=1.6))
    ax.add_patch(Rectangle((x-.35, y+.35), .70, .16, fc=NAVY, ec=NAVY))
    ax.add_patch(Rectangle((x-.27, y-.44), .54, .36, fc=TEAL_LIGHT, ec="none"))
    label(ax, x, y+.02, code, 13, "bold")
    label(ax, x, y-.85, subtitle, 12)

def chain(ax, points, altered=None, radius=.065, color=TEAL):
    if len(points)>1:
        ax.plot([p[0] for p in points], [p[1] for p in points],
                color=color, lw=1.7, zorder=2)
    for i,(x,y) in enumerate(points):
        ax.add_patch(Circle((x,y), radius, fc=TERRA if i==altered else color,
                           ec="white", lw=.7, zorder=3))

def save(fig, stem):
    # Publish complete files atomically so a concurrent book build cannot read
    # a partially written PNG or PDF.
    png_tmp = OUT/f"{stem}.tmp.png"
    pdf_tmp = OUT/f"{stem}.tmp.pdf"
    fig.savefig(png_tmp, dpi=300, facecolor="white")
    with Image.open(png_tmp) as check:
        check.verify()
    fig.savefig(pdf_tmp, facecolor="white")
    png_tmp.replace(OUT/f"{stem}.png")
    pdf_tmp.replace(OUT/f"{stem}.pdf")
    return fig

def figure_one():
    fig, ax = setup(8)
    label(ax, 5, 9.65, "From a sample pair to candidate evidence", 18, "bold")
    label(ax, 5, 9.15, "Fictional sample labels T1, N1 and R1", 12, color=GRAY)
    vial(ax, 1.65, 8.22, "T1", "Tumour DNA")
    vial(ax, 4.95, 8.22, "N1", "Matched normal DNA")
    vial(ax, 8.25, 8.22, "R1", "Tumour RNA")
    ax.plot([1.65, 8.25], [6.97, 6.97], color=GRAY, lw=1.0)
    label(ax, 5, 6.65, "One investigation   Same individual   Defined specimen context",
          12, color=GRAY)
    box(ax, .65, 5.31, 5.95, .78, "DNA identity, alignment\nand quality review",
        fc=LIGHT, size=12)
    box(ax, 7.05, 5.31, 2.35, .78, "RNA quality\nand quantification",
        fc=TEAL_LIGHT, size=12)
    arrow(ax, (1.65,6.18), (1.65,6.09))
    arrow(ax, (4.95,6.18), (4.95,6.09))
    arrow(ax, (8.25,6.18), (8.25,6.09))
    box(ax, .65, 3.78, 5.95, .82,
        "Paired somatic calling\nEvaluate tumour and normal reads",
        fc=TEAL_LIGHT, size=12)
    arrow(ax, (3.6,5.31), (3.6,4.60))
    box(ax, .65, 2.25, 5.95, .82,
        "Variant interpretation\nAssembly, transcripts and local context",
        fc=LIGHT, size=12)
    arrow(ax, (3.6,3.78), (3.6,3.07))
    box(ax, 1.45, .58, 7.15, .94,
        "Candidate evidence table\nOrigin, expression and open questions",
        fc="white", size=13, weight="bold")
    arrow(ax, (3.6,2.25), (3.6,1.52))
    arrow(ax, (8.25,5.31), (8.25,1.52), color=TEAL)
    label(ax, 8.25, 3.35, "Expression\nevidence", 11.5, color=TEAL,
          ha="center", bbox={"facecolor":"white", "edgecolor":"none", "pad":3})
    label(ax, 5, .17, "A reference genome and a panel of normals are not the matched normal.",
          11.5, color=GRAY)
    return save(fig, "ch05_01")

def figure_two():
    fig, ax = setup(7.5)
    label(ax, 5, 9.68, "Follow a difference through related molecules", 18, "bold")
    label(ax, 5, 9.16, "A schematic relationship, not a biological sequence", 12, color=GRAY)
    label(ax, .45, 8.25, "DNA", 14, "bold", ha="left")
    ax.plot([2,9.5], [8.25,8.25], color=GRAY, lw=2, zorder=0)
    for x,w,name in [(2.1,1.8,"Exon 1"),(4.7,1.8,"Exon 2"),(7.5,1.8,"Exon 3")]:
        ax.add_patch(Rectangle((x,7.94),w,.62,fc=TEAL_LIGHT,ec=TEAL,lw=1.4))
        label(ax,x+w/2,8.25,name,12)
    # Keep the same within-exon offset in DNA and RNA, clear of both labels.
    alteration_offset = 1.55
    dna_mark = 4.7 + alteration_offset
    rna_mark = 4.1 + alteration_offset
    ax.plot([dna_mark,dna_mark],[7.83,8.67],color=TERRA,lw=3)
    label(ax,dna_mark,8.86,"Alteration",11.5,color=TERRA)
    label(ax,.45,6.64,"RNA",14,"bold",ha="left")
    arrow(ax,(5,7.7),(5,7.14),color=TEAL)
    label(ax,7.4,7.34,"Transcription and RNA processing",11.5,color=GRAY)
    ax.plot([2.1,7.9],[6.64,6.64],color=TEAL,lw=2,zorder=0)
    for x,w,name in [(2.1,1.8,"1"),(4.1,1.8,"2"),(6.1,1.8,"3")]:
        ax.add_patch(Rectangle((x,6.35),w,.58,fc=TEAL_LIGHT,ec=TEAL,lw=1.4))
        label(ax,x+w/2,6.64,name,12)
    ax.plot([rna_mark,rna_mark],[6.23,7.02],color=TERRA,lw=3)
    label(ax,8.25,6.64,"Transcript 1",11.5,ha="left")
    label(ax,7.75,6.10,"Alternative transcript 2",11.5)
    ax.plot([6.25,9.15],[5.58,5.58],color=TEAL,lw=2,zorder=0)
    for x,w,name in [(6.25,1.35,"1"),(7.8,1.35,"3")]:
        ax.add_patch(Rectangle((x,5.32),w,.52,fc="white",ec=TEAL,lw=1.4))
        label(ax,x+w/2,5.58,name,12)
    label(ax,7.75,4.91,"Exon 2 is absent.",11.5,color=GRAY)
    label(ax,.45,4.18,"Protein",14,"bold",ha="left")
    arrow(ax,(4.95,6.20),(4.95,4.65),color=TEAL)
    label(ax,3.70,5.45,"Translation",11.5,color=GRAY)
    points=[(2.35+i*.33,4.16+.18*math.sin(i*.75)) for i in range(20)]
    chain(ax,points,altered=8,radius=.09)
    label(ax,7.2,3.62,"A possible altered protein product",11.5,color=GRAY)
    label(ax,.45,2.68,"Peptides",14,"bold",ha="left")
    arrow(ax,(4.95,3.70),(4.95,3.08),color=TEAL)
    label(ax,7.1,3.08,"Protein processing",11.5,color=GRAY)
    chain(ax,[(2.25+i*.25,2.58) for i in range(5)],radius=.09)
    chain(ax,[(4.2+i*.25,2.58) for i in range(5)],altered=2,radius=.09)
    chain(ax,[(6.25+i*.25,2.58) for i in range(5)],radius=.09)
    label(ax,5,1.88,"Only some possible fragments contain the altered position.",12)
    label(ax,5,1.22,"DNA evidence, RNA support and peptide detection\nare different observations.",12.5,"bold")
    label(ax,5,.48,"Colours mark corresponding concepts; no nucleotide or amino-acid sequence is shown.",
          11.5,color=GRAY)
    return save(fig, "ch05_02")

def membrane(ax, x, y0, y1, color=TEAL):
    ax.plot([x-.035,x-.035],[y0,y1],color=color,lw=2.0)
    ax.plot([x+.035,x+.035],[y0,y1],color=color,lw=2.0)

def surface_complex(ax, x, y, class_two=False):
    # Abstract bound complex, not an atomic or chain-stoichiometry model.
    stems=[y-.10,y+.10] if class_two else [y]
    for yy in stems:
        ax.plot([x-.23,x+.28],[yy,yy],color=TEAL,lw=2)
    ax.add_patch(Ellipse((x+.40,y),.54,.45,fc=TEAL_LIGHT,ec=TEAL,lw=1.5))
    ax.plot([x+.60,x+.60],[y-.12,y+.12],color=TERRA,lw=3.2)

def tcell(ax,x,y,cd_label):
    ax.add_patch(Ellipse((x,y),1.50,1.74,fc=LIGHT,ec=NAVY,lw=1.6))
    # Abstract TCR at the T-cell boundary, facing the presented complex.
    ax.plot([x-.75,x-.98],[y,y],color=NAVY,lw=1.8)
    ax.plot([x-.98,x-1.10],[y,y+.13],color=NAVY,lw=1.8)
    ax.plot([x-.98,x-1.10],[y,y-.13],color=NAVY,lw=1.8)
    label(ax,x,y-.10,cd_label,11.5,"bold")
    label(ax,x-.85,y+.55,"TCR",11.5)

def figure_three():
    fig, ax = setup(9.6)
    label(ax,5,9.76,"Processing, display and possible recognition",18,"bold")
    label(ax,.35,9.23,"A  Common class I route",14,"bold",ha="left")
    # Cell boundary on right; compartments are geometrically distinct.
    ax.add_patch(Rectangle((.40,5.25),6.58,3.55,fc="white",ec=TEAL,lw=1.2))
    membrane(ax,6.98,5.25,8.80)
    label(ax,5.65,8.58,"Cytosol",11.5,color=GRAY)
    chain(ax,[(.95+i*.18,8.22+.12*math.sin(i)) for i in range(9)],altered=4)
    label(ax,1.65,8.60,"Altered protein",11.5)
    ax.add_patch(Ellipse((1.65,7.22),1.04,.70,fc=LIGHT,ec=NAVY,lw=1.4))
    ax.plot([1.26,2.04],[7.08,7.36],color=GRAY,lw=1.1)
    label(ax,1.65,6.72,"Proteasome",11.5)
    arrow(ax,(1.65,7.94),(1.65,7.58),color=TEAL)
    chain(ax,[(2.43+i*.13,7.22) for i in range(3)],altered=1,radius=.06)
    arrow(ax,(2.15,7.22),(2.36,7.22),color=TEAL)
    # ER compartment and a transporter embedded in its membrane.
    ax.add_patch(FancyBboxPatch((3.35,6.25),2.55,1.96,
        boxstyle="round,pad=.01,rounding_size=.18",
        fc=TEAL_LIGHT,ec=TEAL,lw=1.6))
    label(ax,4.62,7.93,"Endoplasmic\nreticulum",11.5,"bold")
    ax.add_patch(Rectangle((3.18,6.94),.35,.56,fc="white",ec=TEAL,lw=1.5))
    label(ax,2.95,6.62,"TAP",11.5,color=TEAL)
    arrow(ax,(2.83,7.22),(3.96,7.22),color=TERRA)
    chain(ax,[(4.02+i*.14,7.22) for i in range(3)],altered=1,radius=.06)
    label(ax,4.80,6.65,"Loading\nand editing",11.5)
    # Loaded complex symbol inside ER, followed by trafficking.
    ax.add_patch(Ellipse((5.18,7.22),.50,.34,fc="white",ec=TEAL,lw=1.3))
    ax.plot([5.32,5.32],[7.13,7.31],color=TERRA,lw=2.4)
    arrow(ax,(5.47,7.24),(6.70,7.24),color=TEAL,dashed=True)
    label(ax,6.10,5.93,"Trafficking",11.5,color=GRAY)
    surface_complex(ax,6.98,7.24)
    label(ax,7.95,8.50,"Peptide–\nHLA I",11.5)
    tcell(ax,8.85,7.24,"CD8\nT cell")
    ax.plot([7.60,7.75],[7.24,7.24],color=TERRA,lw=1.8,linestyle=":")
    label(ax,8.3,5.83,"Recognition\nis conditional",11.5,color=GRAY)
    label(ax,.65,5.56,"Presenting cell",11.5,color=TEAL,ha="left")
    # Class II route.
    label(ax,.35,4.73,"B  Common class II route in an antigen-presenting cell",
          13.5,"bold",ha="left")
    ax.add_patch(Rectangle((.40,1.05),6.58,2.90,fc="white",ec=TEAL,lw=1.2))
    membrane(ax,6.98,1.05,3.95)
    label(ax,2.20,4.15,"Material taken up",11.5,ha="left")
    chain(ax,[(1.0+i*.15,4.15) for i in range(6)],altered=3)
    arrow(ax,(1.75,4.10),(2.32,2.88),color=TEAL)
    ax.add_patch(Ellipse((3.15,2.47),2.60,1.80,fc=TEAL_LIGHT,ec=TEAL,lw=1.6))
    label(ax,3.40,3.60,"Endosome / lysosome",11.5,"bold")
    chain(ax,[(2.48+i*.13,2.30) for i in range(3)],altered=1,radius=.06)
    ax.add_patch(Ellipse((3.65,2.30),.50,.34,fc="white",ec=TEAL,lw=1.3))
    ax.plot([3.79,3.79],[2.21,2.39],color=TERRA,lw=2.4)
    label(ax,3.15,1.98,"HLA-DM assists\npeptide exchange",11.5)
    arrow(ax,(4.58,2.47),(6.72,2.47),color=TEAL,dashed=True)
    label(ax,5.55,2.03,"Trafficking",11.5,color=GRAY)
    surface_complex(ax,6.98,2.47,class_two=True)
    label(ax,7.95,3.70,"Peptide–\nHLA II",11.5)
    tcell(ax,8.85,2.47,"CD4\nT cell")
    ax.plot([7.60,7.75],[2.47,2.47],color=TERRA,lw=1.8,linestyle=":")
    label(ax,.65,1.27,"Antigen-presenting cell",11.5,color=TEAL,ha="left")
    label(ax,5,.43,"Simplified common routes with biological exceptions.\nDisplayed complexes are symbolic; arrows do not imply tumour elimination.",
          11.5,color=GRAY)
    return save(fig, "ch05_03")

def cell(ax,x,y,tumour,altered):
    if tumour:
        ax.add_patch(Circle((x,y),.235,fc=TEAL_LIGHT,ec=TEAL,lw=1.5))
    else:
        ax.add_patch(Rectangle((x-.21,y-.21),.42,.42,fc=LIGHT,ec=GRAY,lw=1.3))
    for dx,mut in [(-.075,altered),(.075,False)]:
        ax.add_patch(Circle((x+dx,y),.052,fc=TERRA if mut else GRAY,ec="none"))

def figure_four():
    fig, ax = setup(7.5)
    label(ax,5,9.66,"The same allele fraction can describe different mixtures",17.5,"bold")
    label(ax,5,9.08,"Invented ten-cell samples; two local DNA copies per cell",12,color=GRAY)
    scenarios=[
        (0.25,"A  Higher purity, clonal",6,6,"p = 0.60; f = 1.00","6 altered / 20 total","Expected VAF 0.30"),
        (3.58,"B  Higher purity, subclonal",6,3,"p = 0.60; f = 0.50","3 altered / 20 total","Expected VAF 0.15"),
        (6.91,"C  Lower purity, clonal",3,3,"p = 0.30; f = 1.00","3 altered / 20 total","Expected VAF 0.15"),
    ]
    for left,title,nt,na,params,fraction,vaf in scenarios:
        label(ax,left+1.42,8.36,title,11.7,"bold")
        for i in range(10):
            x=left+.35+(i%5)*.54
            y=7.52-(i//5)*.78
            cell(ax,x,y,i<nt,i<na)
        label(ax,left+1.42,5.93,params,12)
        label(ax,left+1.42,5.35,fraction,12)
        label(ax,left+1.42,4.76,vaf,12.5,"bold",color=TERRA)
    for x in [3.32,6.66]:
        ax.plot([x,x],[4.45,8.62],color="#CDD4D8",lw=1)
    # Explicit shared denominator rather than misleading read counts.
    box(ax,.85,3.09,8.30,.84,
        "B and C both have 3 altered DNA copies among 20 total copies.",
        fc=TERRA_LIGHT,size=12.5,ec=TERRA)
    label(ax,5,2.39,"Different tumour purity and cellular prevalence\ncan produce the same expected VAF.",13.5,"bold")
    cell(ax,1.17,1.52,True,False)
    label(ax,1.58,1.52,"Tumour cell",11.5,ha="left")
    cell(ax,4.11,1.52,False,False)
    label(ax,4.52,1.52,"Normal cell",11.5,ha="left")
    ax.add_patch(Circle((7.07,1.52),.075,fc=TERRA,ec="none"))
    label(ax,7.38,1.52,"Altered copy",11.5,ha="left")
    label(ax,5,.72,"Normal cells carry no altered copy. Counts are an idealized expectation,\nnot observed reads; equal sampling and no copy-number change are assumed.",
          11.5,color=GRAY)
    return save(fig, "ch05_04")

if __name__ == "__main__":
    figures=[figure_one(),figure_two(),figure_three(),figure_four()]
    combined_tmp=OUT/"ch05_diagrams.tmp.pdf"
    with PdfPages(combined_tmp) as pdf:
        for fig in figures:
            pdf.savefig(fig,facecolor="white")
    combined_tmp.replace(OUT/"ch05_diagrams.pdf")
    for fig in figures:
        plt.close(fig)
    print("Created four PNGs, four individual PDFs and ch05_diagrams.pdf")

