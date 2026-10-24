"""Draw four original scientific teaching diagrams for Chapter 1.

Use the Codex primary Python runtime. No network or external images are used.
PNGs are 300 dpi; matching PDFs retain vector linework and text.
"""

from pathlib import Path
import argparse
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, PathPatch,
    Polygon, Rectangle,
)
from matplotlib.path import Path as MplPath


NAVY = "#162B3C"
TEAL = "#176B73"
TERRA = "#B65E45"
GRAY = "#66737B"
LIGHT = "#EFF3F4"
TISSUE = "#F5F0E9"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13.5,
    "text.color": NAVY,
    "axes.edgecolor": NAVY,
    "savefig.facecolor": WHITE,
    "figure.facecolor": WHITE,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def canvas(height, xlim=(0, 10), ylim=(0, 10)):
    fig, ax = plt.subplots(figsize=(7.6, height))
    fig.subplots_adjust(left=.025, right=.975, bottom=.025, top=.975)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def text(ax, x, y, label, size=13.5, weight="normal", ha="center", va="center", color=NAVY, **kwargs):
    return ax.text(x, y, label, fontsize=size, fontweight=weight,
                   ha=ha, va=va, color=color, linespacing=1.2, **kwargs)


def arrow(ax, start, end, label=None, label_xy=None, color=GRAY,
          style="-", connectionstyle="arc3,rad=0", scale=13):
    patch = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=scale,
                            linewidth=1.5, color=color, linestyle=style,
                            connectionstyle=connectionstyle, zorder=2)
    ax.add_patch(patch)
    if label and label_xy:
        text(ax, *label_xy, label, color=color, size=13.5,
             bbox={"facecolor": WHITE, "edgecolor": "none", "pad": 1.5}, zorder=5)
    return patch


def line(ax, points, color=GRAY, lw=1.3, style="-", zorder=2):
    ax.plot([p[0] for p in points], [p[1] for p in points],
            color=color, lw=lw, ls=style, zorder=zorder)


def box(ax, x, y, width, height, label, edge=TEAL, fill=WHITE,
        size=13.5, weight="normal"):
    ax.add_patch(FancyBboxPatch((x-width/2, y-height/2), width, height,
                                boxstyle="round,pad=0.04,rounding_size=0.10",
                                linewidth=1.6, edgecolor=edge, facecolor=fill,
                                zorder=3))
    return text(ax, x, y, label, size=size, weight=weight, zorder=4)


def leader(ax, label, xy, xytext, ha="left", color=NAVY, size=13.5):
    return ax.annotate(label, xy=xy, xytext=xytext, ha=ha, va="center",
                       fontsize=size, color=color, linespacing=1.15,
                       arrowprops={"arrowstyle": "-", "color": color,
                                   "lw": 1.1, "shrinkA": 4, "shrinkB": 3},
                       zorder=7)


def curve(ax, points, color=TEAL, lw=2.0, zorder=4):
    path = MplPath(points, [MplPath.MOVETO] + [MplPath.CURVE4] * (len(points)-1))
    ax.add_patch(PathPatch(path, facecolor="none", edgecolor=color, lw=lw, zorder=zorder))


def anatomy():
    fig, ax = canvas(6.9, ylim=(0, 9.4))
    text(ax, 5, 9.08, "Breast structures from surface to gland", size=16.5, weight="bold")
    text(ax, .18, 8.58, "A  Cross section", size=14, weight="bold", ha="left")
    text(ax, 7.82, 8.58, "B  Lymphatic context", size=14, weight="bold")

    # The pectoral muscle and chest wall lie behind, rather than within, the gland.
    ax.add_patch(Rectangle((5.65, 1.35), .54, 6.45,
                           facecolor="#E3E8EB", edgecolor=NAVY, lw=1.2, zorder=1))
    ax.add_patch(Polygon([(5.65, 7.80), (5.26, 7.40), (5.23, 2.00), (5.65, 1.35)],
                         facecolor="#E6BFB4", edgecolor=TERRA, lw=1.4, zorder=2))
    for y in [2.0, 2.7, 3.4, 4.1, 4.8, 5.5, 6.2, 6.9]:
        line(ax, [(5.30, y), (5.56, y+.28)], color=TERRA, lw=.8)

    outline = MplPath(
        [(5.25, 7.45), (4.05, 7.55), (3.30, 7.02), (2.72, 6.05),
         (2.18, 5.25), (2.02, 4.86), (1.93, 4.67),
         (1.56, 4.57), (1.91, 4.36), (2.00, 3.18),
         (3.53, 2.00), (5.23, 2.00), (5.25, 7.45)],
        [MplPath.MOVETO] + [MplPath.CURVE4]*6 + [MplPath.LINETO]*2
        + [MplPath.CURVE4]*3 + [MplPath.CLOSEPOLY])
    ax.add_patch(PathPatch(outline, facecolor=TISSUE, edgecolor=NAVY, lw=1.7, zorder=3))
    ax.add_patch(Ellipse((1.96, 4.53), .18, .85,
                         facecolor="#DAB5A8", edgecolor=TERRA, lw=1.1, zorder=4))
    # Schematic lobular clusters connect to a shared ductal opening.
    for cx, cy in [(3.80, 6.30), (4.45, 5.45), (4.28, 3.83), (3.65, 2.80)]:
        curve(ax, [(2.02, 4.54), (2.70, 4.54), (cx-.70, cy), (cx-.08, cy)], lw=2.1)
        for angle in range(0, 360, 60):
            a = math.radians(angle)
            ax.add_patch(Ellipse((cx+.22*math.cos(a), cy+.20*math.sin(a)),
                                 .28, .23, angle=angle,
                                 facecolor="#CDE3DF", edgecolor=TEAL, lw=1.1, zorder=5))
        ax.add_patch(Circle((cx, cy), .09, facecolor=TEAL, edgecolor=TEAL, zorder=6))

    leader(ax, "Skin", (2.72, 6.05), (.14, 7.52))
    leader(ax, "Duct", (2.96, 4.86), (.14, 5.92))
    leader(ax, "Nipple", (1.57, 4.57), (.14, 4.73))
    leader(ax, "Areola", (1.96, 4.22), (.14, 3.45))
    leader(ax, "Lobules", (3.81, 6.47), (3.64, 8.02), ha="center")
    leader(ax, "Fat and\nfibrous tissue", (4.55, 3.05), (6.58, 3.82))
    leader(ax, "Pectoral\nmuscle", (5.42, 2.94), (6.58, 2.43))
    leader(ax, "Chest wall", (5.93, 1.91), (6.58, 1.05))

    # Separate lymphatic inset. No tumour or cancer-spread arrows are drawn.
    line(ax, [(6.87, 6.05), (6.90, 7.15), (7.40, 7.48),
              (8.10, 7.48), (8.63, 7.15), (8.83, 6.00)], color=GRAY, lw=1.1)
    ax.add_patch(Ellipse((7.65, 6.34), 1.12, .84,
                         facecolor=TISSUE, edgecolor=GRAY, lw=1.1))
    ax.add_patch(Circle((7.65, 6.34), .06, facecolor=TERRA, edgecolor=TERRA))
    for yy in [6.11, 6.35, 6.56]:
        curve(ax, [(7.85, yy), (8.17, yy+.23), (8.36, 6.94), (8.60, 6.96)], lw=1.4)
    for cx, cy in [(8.60, 6.96), (8.83, 7.12), (8.88, 6.83)]:
        ax.add_patch(Ellipse((cx, cy), .17, .24,
                             facecolor="#CDE3DF", edgecolor=TEAL, lw=1.0, zorder=5))
    leader(ax, "Axillary\nlymph nodes", (8.83, 7.12), (9.00, 7.91), ha="center")
    leader(ax, "Lymphatic\nvessels", (8.255, 6.614), (8.20, 4.92), ha="center")
    leader(ax, "Underarm", (8.76, 6.78), (9.58, 5.75), ha="right")
    text(ax, 7.42, 5.66, "Breast", size=13.5)
    text(ax, 3.12, .48, "Original schematic; not to scale", size=13.5, color=GRAY)
    return fig


def pathway():
    fig, ax = canvas(8.5, xlim=(0, 12), ylim=(0, 11.3))
    text(ax, 6, 10.98, "Two routes into assessment", size=17, weight="bold")
    box(ax, 2.45, 10.05, 3.85, .80, "New breast change", weight="bold")
    box(ax, 8.90, 10.05, 5.10, 1.03,
        "No symptoms\nScreening under\napplicable guidance", weight="bold")
    box(ax, 8.90, 8.45, 3.50, .70, "Screening result")
    arrow(ax, (8.90, 9.49), (8.90, 8.83))
    box(ax, 6.95, 7.10, 3.65, 1.00, "Further assessment\nrecommended")
    box(ax, 10.30, 5.95, 2.90, 1.18, "Follow local\nscreening plan")
    arrow(ax, (8.35, 8.07), (7.36, 7.63))
    arrow(ax, (9.52, 8.07), (10.28, 6.59))

    box(ax, 2.45, 7.10, 3.85, .80, "Clinical assessment", weight="bold")
    arrow(ax, (2.45, 9.62), (2.45, 7.54),
          "Report the\nchange", (1.04, 8.57))
    arrow(ax, (5.08, 7.10), (4.42, 7.10))
    text(ax, 4.88, 7.91, "Investigate", size=13.5, color=GRAY)
    text(ax, 10.60, 7.50, "Otherwise", size=13.5, color=GRAY,
         bbox={"facecolor": WHITE, "edgecolor": "none", "pad": 1.5})

    box(ax, 6.00, 5.13, 5.10, 1.12,
        "Clinician-selected tests\nImaging or tissue assessment\nas indicated")
    arrow(ax, (3.55, 6.66), (5.54, 5.75),
          "When needed", (4.36, 6.32))
    # Direct assessment-information route makes testing conditional, not compulsory.
    line(ax, [(1.30, 6.67), (1.30, 3.45), (3.56, 3.45)], color=GRAY)
    arrow(ax, (3.30, 3.45), (3.58, 3.45))
    text(ax, 1.43, 5.10, "Assessment\ninformation", ha="left", size=13.5, color=GRAY)
    box(ax, 6.00, 3.45, 4.75, .74, "Integrate findings", weight="bold")
    arrow(ax, (6.00, 4.53), (6.00, 3.87),
          "Test findings", (7.71, 4.03))
    box(ax, 6.00, 2.10, 6.15, .85, "Explain the result and next step")
    arrow(ax, (6.00, 3.03), (6.00, 2.58))
    box(ax, 6.00, .70, 6.90, .90,
        "Complete the agreed follow-up or care", weight="bold")
    arrow(ax, (6.00, 1.63), (6.00, 1.20))
    text(ax, 10.25, 4.53, "Report any\nnew change", size=13.5, color=TERRA)
    line(ax, [(10.30, 5.30), (10.30, 4.98)], color=TERRA, style="--")
    text(ax, 9.97, 3.24, "A new concern\nreturns to clinical\nassessment", size=13.5, color=GRAY)
    return fig


def distinctions():
    fig, ax = canvas(7.8, ylim=(0, 11))
    text(ax, 5, 10.64, "Different descriptions of disease", size=17, weight="bold")
    text(ax, .20, 10.05, "A  Boundary relationship", size=14, weight="bold", ha="left")
    for cx, invasive in [(2.50, False), (7.48, True)]:
        if invasive:
            ax.add_patch(Arc((cx, 8.30), 2.02, 2.02, theta1=25, theta2=325,
                             color=NAVY, lw=2.0))
        else:
            ax.add_patch(Circle((cx, 8.30), 1.01, facecolor=WHITE,
                                edgecolor=NAVY, lw=2.0))
        for dx, dy in [(-.42, -.33), (-.43, .25), (-.03, -.48),
                       (.00, .00), (.12, .49), (.43, .24), (.43, -.31)]:
            ax.add_patch(Circle((cx+dx, 8.30+dy), .16,
                                facecolor="#CDE3DF", edgecolor=TEAL, lw=1.0))
        if invasive:
            for dx, dy in [(1.00, .03), (1.36, -.16), (1.17, -.48)]:
                ax.add_patch(Circle((cx+dx, 8.30+dy), .16,
                                    facecolor="#E4B8A9", edgecolor=TERRA, lw=1.0))
    text(ax, 2.50, 9.55, "In situ", size=15, weight="bold", color=TEAL)
    text(ax, 7.48, 9.55, "Invasive", size=15, weight="bold", color=TERRA)
    text(ax, 2.50, 6.88, "Abnormal cells remain\nwithin duct", size=13.5)
    text(ax, 7.48, 6.88, "Abnormal cells extend into\nsurrounding tissue", size=13.5)
    text(ax, 5.00, 8.45, "Duct\nboundary", size=13.5,
         bbox={"facecolor": WHITE, "edgecolor": "none", "pad": 2}, zorder=5)
    line(ax, [(4.39, 8.36), (3.53, 8.36)], color=NAVY)
    line(ax, [(5.63, 8.36), (6.43, 8.36)], color=NAVY)
    text(ax, 5, 6.10, "Schematic comparison, not an inevitable progression", size=13.5, color=GRAY)
    line(ax, [(.20, 5.75), (9.80, 5.75)], color="#CCD4D8", lw=.8)
    text(ax, .20, 5.39, "B  Complementary descriptions", size=14, weight="bold", ha="left")
    box(ax, 5, 4.65, 4.9, .66, "Confirmed breast cancer", weight="bold", edge=NAVY)
    for x, name, detail in [
        (1.75, "Anatomical\nextent", "Primary tumour T\nRegional nodes N\nDistant spread M"),
        (5.00, "Microscopic\ngrade", "Appearance of\ncells and tissue"),
        (8.25, "Tumour\nbiomarkers", "ER   PR   HER2"),
    ]:
        arrow(ax, (5, 4.26), (x, 3.63))
        box(ax, x, 3.05, 2.95, .99, name, weight="bold")
        text(ax, x, 1.98, detail, size=13.5)
        arrow(ax, (x, 1.20), (5, .82), color=GRAY)
    box(ax, 5, .47, 6.45, .65, "Applicable breast staging system", edge=NAVY)
    return fig


def records():
    fig, ax = canvas(5.9, xlim=(0, 11), ylim=(0, 8.2))
    text(ax, 5.50, 7.84, "A record answers a question at a particular time", size=16.5, weight="bold")
    text(ax, 5.50, 7.28, "Fictional timeline for a research task", size=13.5, color=GRAY)
    points = [1.15, 3.95, 6.75, 9.55]
    labels = ["Change\nreported", "Diagnostic\nimage acquired", "Tissue result\navailable", "Further\ncharacterisation\nand care"]
    for i, (x, label) in enumerate(zip(points, labels), 1):
        ax.add_patch(Circle((x, 5.95), .105, facecolor=TEAL, edgecolor=TEAL, zorder=4))
        text(ax, x, 6.65, f"Event {i}", size=14, weight="bold")
        text(ax, x, 5.18, label, size=13.5)
        if i < 4:
            arrow(ax, (x+.16, 5.95), (points[i]-.16, 5.95), color=TEAL)
    line(ax, [(3.95, 5.75), (3.95, 6.35)], color=TERRA, lw=1.4, style="--")
    line(ax, [(3.95, 4.44), (3.95, 4.69)], color=TERRA, lw=1.4, style="--")
    text(ax, 4.90, 4.02, "Prediction time", size=13.5, color=TERRA, weight="bold")
    # Two slim document marks link record type to its methodological role.
    for x, y in [(2.42, 2.72), (7.75, 2.72)]:
        ax.add_patch(Rectangle((x-.23, y-.37), .46, .74,
                               facecolor=WHITE, edgecolor=GRAY, lw=1.1))
        for dy in [-.17, 0, .17]:
            line(ax, [(x-.14, y+dy), (x+.14, y+dy)], color=GRAY, lw=.8)
    text(ax, 2.42, 1.81, "Inputs available at\nimage acquisition", size=13.5)
    text(ax, 7.75, 1.81, "Linked later result\nfor evaluation", size=13.5)
    arrow(ax, (3.25, 4.50), (2.56, 3.17), color=TERRA)
    arrow(ax, (6.75, 4.62), (7.60, 3.17), color=GRAY, style="--")
    text(ax, 5.50, .87, "Later results are not earlier inputs", size=14, weight="bold", color=TERRA)
    text(ax, 5.50, .37, "Future risk asks a different question with a defined time period", size=13.5)
    return fig


def save(fig, name, outdir):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    outside = []
    for ax in fig.axes:
        for item in ax.texts:
            if item.get_visible() and item.get_text():
                bb = item.get_window_extent(renderer)
                if (bb.x0 < bounds.x0 or bb.y0 < bounds.y0 or
                        bb.x1 > bounds.x1 or bb.y1 > bounds.y1):
                    outside.append(item.get_text())
    if outside:
        raise ValueError(f"{name}: labels outside canvas: {outside}")
    outdir.mkdir(parents=True, exist_ok=True)
    for fmt in ["png", "pdf"]:
        target = outdir / f"{name}.{fmt}"
        temporary = outdir / f"{name}.pending.{fmt}"
        fig.savefig(temporary, format=fmt, dpi=300, facecolor=WHITE)
        temporary.replace(target)
    size = list(fig.get_size_inches())
    plt.close(fig)
    return {"id": name, "size_inches": size, "png_dpi": 300,
            "vector_pdf": True, "labels_outside_canvas": []}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent / "art")
    args = parser.parse_args()
    report = []
    for name, draw in [("ch01_01", anatomy), ("ch01_02", pathway),
                       ("ch01_03", distinctions), ("ch01_04", records)]:
        report.append(save(draw(), name, args.out_dir))
    (args.out_dir / "ch01_render_checks.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
