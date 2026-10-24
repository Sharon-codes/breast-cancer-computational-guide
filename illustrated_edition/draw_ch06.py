"""Draw four original scientific schematics for Chapter 6.

Run with Python 3.12 and the recorded dependencies. No generative image model, patient
images, synthetic survival curves, or reconstructed individual event times are
used. Published counts in figure 4 are attributed in the accompanying brief.
"""

from __future__ import annotations

from pathlib import Path
import math
from io import BytesIO
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image


ROOT = Path(__file__).resolve().parent
ART = ROOT / "art"
ART.mkdir(parents=True, exist_ok=True)
NAVY = "#162B3C"
TEAL = "#176B73"
TERRA = "#B65E45"
GRAY = "#68757D"
LIGHT = "#E7ECEF"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "text.color": NAVY,
    "axes.labelcolor": NAVY,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.facecolor": WHITE,
})


def canvas(height=7.4):
    fig = plt.figure(figsize=(8, height), facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    return fig, ax


def text(ax, x, y, value, size=13, weight="normal", color=NAVY,
         ha="center", va="center", **kwargs):
    return ax.text(x, y, value, fontsize=size, fontweight=weight, color=color,
                   ha=ha, va=va, linespacing=1.18, **kwargs)


def arrow(ax, start, end, color=NAVY, lw=1.8, dashed=False,
          connectionstyle="arc3,rad=0"):
    p = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15,
                        linewidth=lw, color=color,
                        linestyle=(0, (4, 3)) if dashed else "solid",
                        connectionstyle=connectionstyle)
    ax.add_patch(p)
    return p


def line(ax, start, end, color=GRAY, lw=1.3, dashed=False):
    ax.plot([start[0], end[0]], [start[1], end[1]], color=color, lw=lw,
            linestyle=(0, (4, 3)) if dashed else "solid")


def rounded(ax, x, y, w, h, edge=GRAY, face=WHITE, radius=.012, lw=1.5):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.004,rounding_size={radius}",
                       edgecolor=edge, facecolor=face, linewidth=lw)
    ax.add_patch(p)
    return p


def virus(ax, x, y, r=.042):
    for theta in [k * math.pi / 6 for k in range(12)]:
        a = (x + r * math.cos(theta), y + r * math.sin(theta))
        b = (x + 1.36*r * math.cos(theta), y + 1.36*r * math.sin(theta))
        line(ax, a, b, color=TEAL, lw=1.8)
        ax.add_patch(Circle(b, .004, facecolor=TEAL, edgecolor=TEAL))
    ax.add_patch(Circle((x, y), r, facecolor=WHITE, edgecolor=NAVY, lw=2))
    ax.add_patch(Circle((x-.011, y+.008), .006, facecolor=LIGHT, edgecolor=GRAY))
    ax.add_patch(Circle((x+.015, y-.008), .006, facecolor=LIGHT, edgecolor=GRAY))


def tumour(ax, x, y, r=.029):
    for dx, dy in [(-.025, .010), (.020, .017), (.000, -.021)]:
        ax.add_patch(Circle((x+dx, y+dy), r, facecolor=WHITE, edgecolor=NAVY, lw=1.7))
        ax.add_patch(Circle((x+dx+.004, y+dy-.002), r*.30,
                            facecolor=LIGHT, edgecolor=GRAY, lw=1))
    for dx, dy in [(-.048, .010), (.046, .017), (.004, -.049)]:
        ax.add_patch(Rectangle((x+dx-.005, y+dy-.004), .011, .009,
                               facecolor=TEAL, edgecolor=TEAL))


def tcells(ax, x, y):
    for dx, dy, r in [(-.022, .014, .024), (.023, -.012, .026)]:
        ax.add_patch(Circle((x+dx, y+dy), r, facecolor=WHITE, edgecolor=TEAL, lw=1.9))
        ax.add_patch(Circle((x+dx+.004, y+dy+.001), r*.48,
                            facecolor=LIGHT, edgecolor=GRAY, lw=.9))


def shield(ax, x, y):
    xy = [(x-.045, y+.043), (x+.045, y+.043), (x+.039, y-.007),
          (x, y-.052), (x-.039, y-.007)]
    ax.add_patch(Polygon(xy, closed=True, facecolor=WHITE, edgecolor=TEAL, lw=2))
    line(ax, (x-.019, y-.002), (x-.003, y-.017), color=TEAL, lw=2)
    line(ax, (x-.003, y-.017), (x+.023, y+.019), color=TEAL, lw=2)


def testtube(ax, x, y, color=TEAL):
    rounded(ax, x-.017, y-.037, .034, .075, edge=NAVY, radius=.010, lw=1.4)
    ax.add_patch(Rectangle((x-.014, y-.030), .028, .031,
                           facecolor=LIGHT, edgecolor="none"))
    line(ax, (x-.022, y+.038), (x+.022, y+.038), color=color, lw=3)


def draw01():
    fig, ax = canvas(6.6)
    text(ax, .5, .955, "Different vaccination goals", 18, "bold")
    text(ax, .055, .865, "A   Infection prevention", 14, "bold", ha="left")
    text(ax, .945, .865, "Before relevant exposure", 12, color=GRAY, ha="right")
    virus(ax, .15, .705)
    tcells(ax, .49, .705)
    shield(ax, .83, .705)
    arrow(ax, (.225, .705), (.407, .705))
    arrow(ax, (.565, .705), (.748, .705))
    text(ax, .15, .580, "Infectious agent\nantigens", 13)
    text(ax, .49, .580, "Immune\npreparation", 13)
    text(ax, .83, .580, "Goal: fewer infections\nand associated disease", 12.5)
    line(ax, (.055, .470), (.945, .470), color=GRAY, lw=1)
    text(ax, .055, .410, "B   Therapeutic cancer vaccination", 14, "bold", ha="left")
    text(ax, .055, .365, "After diagnosis, including investigation after surgery", 12, color=GRAY, ha="left")
    tumour(ax, .15, .245)
    tcells(ax, .49, .245)
    # A follow-up record, with no check mark or invented effect-size bars.
    rounded(ax, .790, .196, .080, .102, edge=NAVY, radius=.005, lw=1.7)
    rounded(ax, .811, .289, .038, .015, edge=TEAL, radius=.003, lw=1.4)
    for yy in [.271, .246, .221]:
        ax.add_patch(Circle((.804, yy), .003, facecolor=WHITE, edgecolor=TEAL, lw=1))
        line(ax, (.814, yy), (.857, yy), color=GRAY, lw=1.1)
    arrow(ax, (.225, .245), (.407, .245))
    arrow(ax, (.565, .245), (.748, .245))
    text(ax, .15, .120, "Selected tumour\nantigens", 13)
    text(ax, .49, .120, "Antigen-directed\nimmune response", 13)
    text(ax, .83, .120, "Goal: tumour control\nor lower recurrence", 12.5)
    text(ax, .5, .035, "Conceptual purposes; clinical effects require intervention-specific evidence.", 11.3, color=GRAY)
    return fig


def draw02():
    fig, ax = canvas(8.0)
    text(ax, .5, .958, "From a candidate target to clinical evidence", 17, "bold")
    text(ax, .24, .905, "Biological dependency", 12, "bold", color=TEAL)
    text(ax, .74, .905, "Corresponding evidence", 12, "bold", color=TEAL)
    ys = [.805, .645, .485, .325, .165]
    labels = ["Tumour alteration\nand expression", "Presentation and\nT-cell priming",
              "Antigen-specific\nT-cell response", "Tumour recognition\nand local function",
              "Clinical outcomes"]
    evidence = ["Sequencing and\nexpression support", "Presentation assays\nand priming evidence",
                "Specified immune assays\nand longitudinal samples", "Tumour-cell recognition\nand tissue evidence",
                "Appropriate comparison:\nrecurrence, survival, harms"]
    for i, (y, label, ev) in enumerate(zip(ys, labels, evidence), 1):
        ax.add_patch(Circle((.070, y), .024, facecolor=NAVY, edgecolor=NAVY))
        text(ax, .070, y, str(i), 13, "bold", color=WHITE)
        text(ax, .15, y, label, 13, "bold", ha="left")
        line(ax, (.505, y), (.565, y), color=TEAL, lw=1.5, dashed=True)
        text(ax, .735, y, ev, 12.8)
        if i < 5:
            arrow(ax, (.070, y-.032), (.070, ys[i]+.035), color=NAVY, lw=1.6)
            line(ax, (.14, y-.080), (.94, y-.080), color=LIGHT, lw=1.1)
    text(ax, .5, .052, "Each transition needs support; a blood response is not a clinical outcome.",
         11.5, color=GRAY)
    return fig


def draw03():
    fig, ax = canvas(8.1)
    text(ax, .5, .958, "The boundaries of a personalized research workflow", 16.7, "bold")
    text(ax, .045, .905, "SPECIMENS AND CLINICAL CONTEXT", 11.5, "bold", color=GRAY, ha="left")
    testtube(ax, .19, .825)
    testtube(ax, .49, .825)
    # Clinical record icon.
    rounded(ax, .750, .785, .080, .082, edge=NAVY)
    for yy in [.846, .826, .806]:
        line(ax, (.767, yy), (.816, yy), color=GRAY, lw=1.2)
    text(ax, .19, .755, "Tumour material", 12.5)
    text(ax, .49, .755, "Matched normal", 12.5)
    text(ax, .79, .755, "Study context", 12.5)
    # Group the study inputs before branching to derived molecular evidence.
    # This deliberately avoids a false one-to-one mapping from normal to RNA,
    # or from a clinical record to HLA typing.
    for xx in [.19, .49, .79]:
        line(ax, (xx, .733), (xx, .715), color=GRAY, lw=1.2)
    line(ax, (.19, .715), (.79, .715), color=GRAY, lw=1.3)
    text(ax, .49, .685, "Linked study inputs", 11.5, "bold", color=GRAY)
    line(ax, (.045, .650), (.955, .650), dashed=True)
    nodes = [(.19, "Somatic\nvariants"), (.49, "RNA\nexpression"), (.79, "HLA\ncontext")]
    for x, label in nodes:
        rounded(ax, x-.105, .520, .210, .080, edge=TEAL, radius=.018)
        text(ax, x, .560, label, 13)
        arrow(ax, (x, .671), (x, .607), color=GRAY, lw=1.3)
    for x in [.19, .49, .79]:
        arrow(ax, (x, .517), (.49, .465), color=TEAL, lw=1.5)
    rounded(ax, .268, .385, .444, .080, edge=NAVY, radius=.018)
    text(ax, .49, .425, "Candidate prioritization\nand documented review", 13, "bold")
    line(ax, (.045, .350), (.955, .350), dashed=True)
    # Assay wells are symbolic only: no protocol or quantitative values.
    rounded(ax, .185, .218, .100, .065, edge=TEAL, radius=.006)
    for xx in [.205, .235, .265]:
        for yy in [.262, .238]:
            ax.add_patch(Circle((xx, yy), .007, facecolor=WHITE, edgecolor=TEAL, lw=1.1))
    testtube(ax, .67, .250)
    text(ax, .235, .168, "Biological testing\nspecified by protocol", 12.5)
    text(ax, .825, .250, "Controlled\npreparation and\nproduct release", 11.5)
    arrow(ax, (.380, .382), (.25, .289), color=TEAL)
    arrow(ax, (.600, .382), (.67, .294), color=NAVY)
    # Optional feedback is deliberately dashed and labelled as such in the caption.
    arrow(ax, (.175, .267), (.265, .420), color=GRAY, lw=1.2, dashed=True,
          connectionstyle="arc3,rad=-.22")
    arrow(ax, (.670, .201), (.590, .090), color=NAVY, lw=1.5)
    text(ax, .49, .073, "Clinical evaluation", 13, "bold")
    text(ax, .49, .030, "Safety  |  immune measurements  |  clinical outcomes", 11.5, color=GRAY)
    return fig


def draw04():
    fig, ax = canvas(8.0)
    text(ax, .5, .959, "Read the population before interpreting follow-up", 16.7, "bold")
    rounded(ax, .065, .820, .870, .092, edge=GRAY, face=WHITE)
    text(ax, .5, .880, "NCT02316457: 42 enrolled", 14.5, "bold")
    text(ax, .5, .845, "Broader registered study with several experimental arms", 12)
    line(ax, (.075, .780), (.925, .780), color=GRAY, dashed=True)
    text(ax, .5, .752, "The publication reports an individualized-vaccine analysis", 12, color=GRAY)
    ax.add_patch(Circle((.24, .662), .036, facecolor=NAVY, edgecolor=NAVY))
    text(ax, .24, .662, "15", 16, "bold", color=WHITE)
    text(ax, .315, .662, "Consented to the reported study arm", 13, "bold", ha="left")
    arrow(ax, (.24, .620), (.24, .518), color=NAVY)
    line(ax, (.24, .580), (.76, .580), color=GRAY, lw=1.4)
    arrow(ax, (.76, .580), (.76, .518), color=TERRA, lw=1.5)
    ax.add_patch(Circle((.24, .475), .038, facecolor=TEAL, edgecolor=TEAL))
    text(ax, .24, .475, "14", 16, "bold", color=WHITE)
    text(ax, .24, .412, "Per-protocol\nevaluable participants", 12.7)
    ax.add_patch(Circle((.76, .475), .038, facecolor=WHITE, edgecolor=TERRA, lw=1.8))
    text(ax, .76, .475, "1", 16, "bold", color=TERRA)
    text(ax, .76, .412, "Discontinued following\ntreatment-emergent events", 12.1)
    text(ax, .5, .337, "Reported clinical status at the February 2025 cutoff", 12.5, "bold")
    x, w, y, h = .080, .840, .243, .064
    categories = [(10, TEAL), (1, LIGHT), (3, TERRA)]
    centres = []
    cur = x
    for count, color in categories:
        ww = w*count/14
        ax.add_patch(Rectangle((cur, y), ww, h, facecolor=color, edgecolor=WHITE, lw=1.4))
        text(ax, cur+ww/2, y+h/2, str(count), 15, "bold", color=NAVY if count == 1 else WHITE)
        centres.append(cur+ww/2)
        cur += ww
    line(ax, (centres[0], y), (.180, .205), color=TEAL, lw=1.2)
    line(ax, (centres[1], y), (.510, .205), color=GRAY, lw=1.2)
    line(ax, (centres[2], y), (.840, .205), color=TERRA, lw=1.2)
    text(ax, .180, .155, "10 relapse-free\nat cutoff", 12.5, color=TEAL)
    text(ax, .510, .155, "1 death of unknown cause\n15 months after last vaccination,\nwithout prior relapse", 11.7)
    text(ax, .840, .155, "3 recurrences", 12.5, color=TERRA)
    text(ax, .5, .055, "Aggregate status counts, not a survival curve or vaccine-efficacy estimate.", 11.3, color=GRAY)
    return fig


DRAWERS = {"ch06_01": draw01, "ch06_02": draw02, "ch06_03": draw03, "ch06_04": draw04}


def main():
    figures = []
    bundle_temporary = ART / ".ch06_diagrams.pdf.tmp"
    with PdfPages(bundle_temporary) as bundle:
        for key, drawer in DRAWERS.items():
            fig = drawer()
            fig.canvas.draw()
            # Check that every rendered text extent remains inside its page.
            renderer = fig.canvas.get_renderer()
            bounds = fig.bbox
            for artist in fig.findobj(match=plt.Text):
                if not artist.get_text():
                    continue
                box = artist.get_window_extent(renderer=renderer)
                if box.x0 < -1 or box.y0 < -1 or box.x1 > bounds.x1+1 or box.y1 > bounds.y1+1:
                    raise ValueError(f"Out-of-page text in {key}: {artist.get_text()!r}")
            for extension in ("png", "pdf"):
                buffer = BytesIO()
                fig.savefig(buffer, format=extension, dpi=300)
                data = buffer.getvalue()
                if extension == "png":
                    Image.open(BytesIO(data)).verify()
                temporary = ART / f".{key}.{extension}.tmp"
                with temporary.open("wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                temporary.replace(ART / f"{key}.{extension}")
            bundle.savefig(fig)
            figures.append(key)
            plt.close(fig)
    bundle_temporary.replace(ART / "ch06_diagrams.pdf")
    print("Created", ", ".join(figures), "at 300 dpi plus vector PDFs")


if __name__ == "__main__":
    main()
