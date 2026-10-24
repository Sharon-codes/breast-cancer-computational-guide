"""Exact scientific teaching figures for Chapter 3. No generated imagery.

Run with the project's recorded Python environment. Figure 4 reads the saved
heldout predictions and reliability bins; it does not fit or select a model.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

ROOT = Path(__file__).resolve().parent
ART = ROOT / "art"
NAVY = "#162B3C"
TEAL = "#176B73"
TERRA = "#B65E45"
GRAY = "#7F8991"
LIGHT = "#E8EDF0"
PALE = "#F4F7F8"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13,
    "axes.labelsize": 13, "axes.titlesize": 14,
    "xtick.labelsize": 12.5, "ytick.labelsize": 12.5,
    "text.color": NAVY, "axes.labelcolor": NAVY,
    "xtick.color": NAVY, "ytick.color": NAVY,
    "axes.edgecolor": NAVY, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
    "pdf.fonttype": 42, "ps.fonttype": 42,
})


def save(fig, stem):
    ART.mkdir(parents=True, exist_ok=True)
    fig.savefig(ART / f"{stem}.png", dpi=300, facecolor="white")
    fig.savefig(ART / f"{stem}.pdf", facecolor="white")
    plt.close(fig)


def figure_01():
    """Membership matrix makes shared sources visible across two split designs."""
    fig = plt.figure(figsize=(7.2, 6.1))
    fig.suptitle("Related patches must follow their source", fontsize=15, weight="bold", y=.97)
    fig.text(.5, .915, "Illustrative grouping example", ha="center", fontsize=13)
    ax = fig.add_axes([.055, .18, .90, .65])
    ax.set(xlim=(0, 9.35), ylim=(-.65, 9.5))
    ax.axis("off")
    for x, label in [(0.0, "Patient"), (1.45, "Specimen"), (2.95, "Patch")]:
        ax.text(x, 8.9, label, fontsize=12.5, weight="bold", va="center")
    ax.text(5.25, 9.35, "Split by patch", ha="center", weight="bold", fontsize=12.5)
    ax.text(8.25, 9.35, "Split by patient", ha="center", weight="bold", fontsize=12.5)
    for x, label in [(4.75, "Train"), (5.75, "Test"), (7.75, "Train"), (8.75, "Test")]:
        ax.text(x, 8.7, label, ha="center", fontsize=12.5)
    for patient in range(4):
        ys = [7.5 - 2*patient, 6.5 - 2*patient]
        if patient % 2 == 0:
            ax.add_patch(Rectangle((-.06, ys[1]-.48), 9.35, 1.98, facecolor=PALE, edgecolor="none"))
        center = sum(ys)/2
        ax.text(0.0, center, f"P{patient+1:02d}", va="center")
        ax.text(1.45, center, f"S{patient+1:02d}", va="center")
        for j, y in enumerate(ys):
            ax.text(3.05, y, "a" if j == 0 else "b", ha="center", va="center")
            selected_patch = 4.75 if j == 0 else 5.75
            selected_patient = 7.75 if patient < 2 else 8.75
            for x in [4.75, 5.75, 7.75, 8.75]:
                active = x in [selected_patch, selected_patient]
                color = TEAL if x in [4.75, 7.75] else TERRA
                ax.plot(x, y, "o", markersize=12, markerfacecolor=color if active else "white",
                        markeredgecolor=color if active else "#BBC4CA", markeredgewidth=1.3)
        ax.plot([-.06, 9.29], [ys[1]-.50, ys[1]-.50], color=LIGHT, linewidth=.9)
    ax.plot([6.55, 6.55], [-.45, 9.45], color=GRAY, linewidth=1, linestyle=(0,(3,4)))
    fig.text(.56, .13, "Every patient appears\non both sides", ha="center", fontsize=12.5, color=TERRA)
    fig.text(.84, .13, "Each patient stays\non one side", ha="center", fontsize=12.5, color=TEAL)
    fig.legend(handles=[Line2D([],[],marker="o",linestyle="",color=TEAL,label="Training"),
                        Line2D([],[],marker="o",linestyle="",color=TERRA,label="Evaluation")],
               loc="lower left", bbox_to_anchor=(.06,.025), frameon=False, ncol=2, fontsize=12.5)
    save(fig, "ch03_01")


def figure_02():
    """A fold matrix and ruler flow explain training-local transformations."""
    fig = plt.figure(figsize=(7.2, 6.3))
    fig.suptitle("Fit a new scaler within each training fold", fontsize=15, weight="bold", y=.97)
    fig.text(.36, .90, "426 development cases", ha="center", weight="bold")
    ax = fig.add_axes([.14,.40,.59,.43])
    ax.set(xlim=(-.02,5.02),ylim=(-.3,5.6))
    ax.axis("off")
    for j in range(5):
        ax.text(j+.5,5.35,f"F{j+1}",ha="center",va="center",fontsize=12.5)
    for fold in range(5):
        y=4.25-fold
        ax.text(-.10,y+.35,f"Fold {fold+1}",ha="right",va="center",fontsize=12.5)
        for j in range(5):
            ax.add_patch(Rectangle((j+.025,y),.95,.72,facecolor=TERRA if j==fold else TEAL,
                                   edgecolor="white",linewidth=1.5))
    fig.text(.83,.73,"143 cases\nheld out",ha="center",va="center",fontsize=13,weight="bold",color=NAVY)
    fig.text(.85,.57,"Outside\nmodel\nselection",ha="center",va="center",fontsize=12.5,color=GRAY)
    fig.lines.append(Line2D([.755,.755],[.43,.87],transform=fig.transFigure,
                            color=GRAY,linestyle=(0,(3,4)),linewidth=1))
    fig.legend(handles=[Rectangle((0,0),1,1,facecolor=TEAL,label="Fit using these folds"),
                        Rectangle((0,0),1,1,facecolor=TERRA,label="Validate on this fold")],
               loc="lower left",bbox_to_anchor=(.08,.335),frameon=False,ncol=1,fontsize=12.5)
    fig.text(.5,.305,"Four C settings × five folds = 20 fitted comparisons",ha="center",fontsize=12.5)
    ax2=fig.add_axes([.06,.08,.90,.19]);ax2.set(xlim=(0,10),ylim=(0,1));ax2.axis("off")
    labels=["Fit scaler + model\non training folds", "Transform + predict\non validation fold", "Score validation\nROC AUC"]
    for x,t in zip([1.4,5.0,8.6],labels):
        ax2.text(x,.68,t,ha="center",va="center",fontsize=12.5)
    for a,b in [(2.95,3.50),(6.55,7.10)]:
        ax2.add_patch(FancyArrowPatch((a,.68),(b,.68),arrowstyle="-|>",mutation_scale=16,color=NAVY,lw=1.5))
    fig.text(.5,.055,"After selection: refit on 426 cases, then evaluate the 143-case holdout",ha="center",fontsize=12.5)
    save(fig, "ch03_02")


def figure_03():
    """Recondition positive decisions using exact hypothetical expected counts."""
    fig = plt.figure(figsize=(7.2, 6.0))
    fig.suptitle("A positive result changes the denominator",fontsize=15,weight="bold",y=.97)
    fig.text(.5,.91,"Hypothetical: 100,000 people, prevalence 0.5%",ha="center",fontsize=13)
    ax=fig.add_axes([.08,.16,.86,.68])
    ax.set(xlim=(0,100),ylim=(-.65,3.15));ax.axis("off")
    h=.33
    # Each bar has a different, explicitly stated denominator.
    ax.text(0,2.95,"500 affected people",weight="bold",fontsize=13)
    ax.barh(2.55,90,height=h,left=0,color=TEAL)
    ax.barh(2.55,10,height=h,left=90,color=LIGHT,edgecolor=GRAY,lw=.7)
    ax.text(38,2.55,"450 true positives · 90%",ha="center",va="center",color="white",fontsize=12.5)
    ax.annotate("50 false negatives",xy=(95,2.55),xytext=(100,2.18),ha="right",fontsize=12.5,
                arrowprops={"arrowstyle":"-","color":GRAY,"lw":1})
    ax.text(0,1.65,"99,500 unaffected people",weight="bold",fontsize=13)
    ax.barh(1.25,95,height=h,left=0,color=NAVY)
    ax.barh(1.25,5,height=h,left=95,color=TERRA)
    ax.text(42,1.25,"94,525 true negatives · 95%",ha="center",va="center",color="white",fontsize=12.5)
    ax.annotate("4,975 false positives",xy=(97.5,1.25),xytext=(100,.88),ha="right",fontsize=12.5,
                arrowprops={"arrowstyle":"-","color":TERRA,"lw":1})
    ppv=450/5425*100
    ax.text(0,.35,"5,425 positive results from both groups",weight="bold",fontsize=13)
    ax.barh(-.05,ppv,height=h,left=0,color=TEAL)
    ax.barh(-.05,100-ppv,height=h,left=ppv,color=TERRA)
    ax.text(57,-.05,"4,975 false positives",ha="center",va="center",color="white",fontsize=12.5)
    ax.annotate("450 true positives",xy=(ppv/2,-.05),xytext=(0,-.49),ha="left",fontsize=12.5,
                arrowprops={"arrowstyle":"-","color":TEAL,"lw":1})
    fig.text(.5,.095,"PPV = 450 / 5,425 = 8.29%",ha="center",fontsize=16,weight="bold",color=TEAL)
    fig.text(.5,.035,"Each bar represents 100% of its labelled group.",ha="center",fontsize=12.5,color=GRAY)
    save(fig, "ch03_03")


def figure_04():
    """Actual ROC and occupied reliability bins from saved heldout predictions."""
    pred=pd.read_csv(ROOT.parent/"results/heldout_predictions.csv")
    rel=pd.read_csv(ROOT.parent/"results/reliability_bins.csv")
    analysis=json.loads((ROOT.parent/"results/analysis.json").read_text())
    y=pred.malignant.to_numpy();p=pred.probability_malignant.to_numpy()
    fpr,tpr,_=roc_curve(y,p)
    auc=roc_auc_score(y,p)
    assert len(y)==143 and np.isclose(auc,analysis["diagnostic"]["model"]["roc_auc"])
    tn,fp,fn,tp=confusion_matrix(y,(p>=.5).astype(int),labels=[0,1]).ravel()
    assert (tn,fp,fn,tp)==(90,0,5,48)
    assert int(rel.n.sum())==143
    # Reconstruct the saved fixed-bin summaries from the saved predictions.
    # This checks that the plotted CSV and case-level scores still agree.
    edges=np.linspace(0,1,6)
    groups=np.minimum(np.digitize(p,edges[1:-1],right=False),4)
    for row in rel.itertuples():
        mask=groups==(row.bin-1)
        assert int(mask.sum())==row.n
        if mask.any():
            assert np.isclose(p[mask].mean(),row.mean_prediction)
            assert np.isclose(y[mask].mean(),row.observed_fraction)
        else:
            assert pd.isna(row.mean_prediction) and pd.isna(row.observed_fraction)
    fig,axes=plt.subplots(1,2,figsize=(7.2,5.0))
    fig.subplots_adjust(left=.105,right=.97,bottom=.26,top=.82,wspace=.48)
    for ax in axes:
        ax.spines[["top","right"]].set_visible(False)
        ax.set(xlim=(-.03,1.03),ylim=(-.03,1.03))
        ax.set_xticks([0,.5,1]);ax.set_yticks([0,.5,1])
        ax.tick_params(length=3)
        ax.plot([0,1],[0,1],linestyle=(0,(3,3)),color=GRAY,lw=1.1,zorder=1)
    axes[0].plot(fpr,tpr,color=TEAL,lw=2.1,zorder=3)
    axes[0].scatter([fp/(tn+fp)],[tp/(tp+fn)],marker="D",s=34,color=TERRA,zorder=4)
    axes[0].annotate("Threshold 0.5",xy=(0,tp/(tp+fn)),xytext=(.20,.68),fontsize=12.5,
                     arrowprops={"arrowstyle":"-","color":TERRA,"lw":1},color=NAVY)
    axes[0].text(.96,.10,f"AUC {auc:.4f}",ha="right",fontsize=12.5,color=TEAL)
    axes[0].set(title="A  Score ordering",xlabel="False-positive rate",ylabel="True-positive rate")
    occupied=rel[rel.n>0]
    axes[1].scatter(occupied.mean_prediction,occupied.observed_fraction,s=43,color=TERRA,zorder=3)
    for row in occupied.itertuples():
        shift={1:(8,7),2:(-6,28),3:(7,-17),5:(-46,-18)}[row.bin]
        axes[1].annotate(f"n={row.n}",(row.mean_prediction,row.observed_fraction),
                         xytext=shift,textcoords="offset points",fontsize=12.5,color=NAVY)
    axes[1].set(title="B  Probability agreement",xlabel="Mean predicted probability",ylabel="Observed malignant fraction")
    fig.text(.5,.94,"Actual WDBC holdout · 143 selected diagnostic cases",ha="center",fontsize=13.5,weight="bold")
    fig.text(.5,.055,"Probability groups are descriptive; the 0.6–0.8 group is empty.",ha="center",fontsize=12.5,color=GRAY)
    save(fig,"ch03_04")


if __name__=="__main__":
    figure_01();figure_02();figure_03();figure_04()
    print(json.dumps({"output_directory":str(ART),"figures":[f"ch03_{i:02d}" for i in range(1,5)],
                      "actual_data_figure":"ch03_04","new_model_fits":0},indent=2))
