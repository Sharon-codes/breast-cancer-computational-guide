"""Create original monochrome teaching figures from executed or declared inputs."""
from pathlib import Path
import json
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'book_figures'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
manifest=[]


def save(fig,name,chapter,caption,source_keys,kind):
    fig.savefig(OUT/(name+'.png'),dpi=220,bbox_inches='tight',facecolor='white')
    plt.close(fig)
    manifest.append(dict(name=name,chapter=chapter,file=name+'.png',caption=caption,source_keys=source_keys,kind=kind))


def panels(name,chapter,title,items,caption,keys,kind='original conceptual diagram'):
    fig,ax=plt.subplots(figsize=(7.2,3.2));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
    ax.text(.5,.97,title,ha='center',va='top',weight='bold',fontsize=12)
    positions=[(.02,.50),(.52,.50),(.02,.03),(.52,.03)]
    for (heading,body),(x,y) in zip(items,positions):
        ax.add_patch(FancyBboxPatch((x,y),.46,.37,boxstyle='round,pad=0.015',facecolor='white',edgecolor='black',linewidth=1))
        ax.text(x+.23,y+.30,heading,ha='center',va='center',weight='bold')
        ax.text(x+.23,y+.16,textwrap.fill(body,34),ha='center',va='center',fontsize=9)
    save(fig,name,chapter,caption,keys,kind)


def flow(name,chapter,title,items,caption,keys,kind='original conceptual diagram'):
    fig,ax=plt.subplots(figsize=(6.6,4.3));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
    ax.text(.5,.98,title,ha='center',va='top',weight='bold',fontsize=12)
    ys=np.linspace(.82,.12,len(items))
    for i,(head,body) in enumerate(items):
        y=ys[i]
        ax.add_patch(FancyBboxPatch((.13,y-.055),.74,.11,boxstyle='round,pad=.015',facecolor='white',edgecolor='black'))
        ax.text(.5,y+.018,head,ha='center',va='center',weight='bold')
        ax.text(.5,y-.022,body,ha='center',va='center',fontsize=8.5)
        if i<len(items)-1:ax.annotate('',xy=(.5,ys[i+1]+.07),xytext=(.5,y-.07),arrowprops={'arrowstyle':'->','color':'black'})
    save(fig,name,chapter,caption,keys,kind)


panels('01_clinical_questions',1,'Different questions require different evidence',[
('Breast awareness','What new or unusual change needs clinical assessment?'),
('Screening','Who may benefit from testing without symptoms?'),
('Diagnosis','What explains a symptom or abnormal test?'),
('Staging','What is the extent of a confirmed cancer?')],
'A conceptual separation of clinical questions. This is not a self-diagnosis or staging algorithm. The relevant clinical pathway depends on the person and findings.',
['https://www.cancer.gov/types/breast/symptoms','https://www.cancer.gov/types/breast/diagnosis'])

flow('02_screening_evidence',2,'Interpreting a screening claim',[
('Intended population','Symptoms, age, risk, setting and access'),
('Test and comparator','Define what is compared and how'),
('Diagnostic follow-up','Resolve findings and record outcomes'),
('Patient outcomes and harms','Detection is one endpoint among several')],
'Questions for appraising a screening claim. Improved test performance does not by itself answer every question about benefit, harm or implementation.',
['https://www.cancer.gov/types/breast/screening'])

pred=pd.read_csv(ROOT/'results/heldout_predictions.csv')
fig,ax=plt.subplots(figsize=(5.5,3.6));ax.axis('off')
cells=[['90','0'],['5','48']]
t=ax.table(cellText=cells,rowLabels=['Benign','Malignant'],colLabels=['Predicted benign','Predicted malignant'],loc='center',cellLoc='center')
t.scale(1,3);t.auto_set_font_size(False);t.set_fontsize(12)
for cell in t.get_celld().values():cell.set_edgecolor('black');cell.set_facecolor('white')
ax.set_title('Internal holdout confusion counts',pad=20)
save(fig,'03_confusion_counts',3,
'Executed internal holdout counts at threshold 0.5, with malignant as the positive class. The 143 selected diagnostic cases are not a population screening cohort.',
['results/analysis.json'],'executed analysis')

flow('04_training_and_holdout',3,'Keeping model selection inside the training data',[
('All 569 diagnostic records','Recode malignant as the positive class'),
('Freeze the stratified row split','426 training cases and 143 holdout cases'),
('Select using training folds','Fit scaling and the classifier within each fold'),
('Evaluate the frozen model','Prespecified threshold and untouched holdout')],
'The executed evaluation design. The bundled data omit original identifiers; row separation does not independently verify grouped patient separation.',
['run_analysis.py'],'executed analysis')

prev=pd.read_csv(ROOT/'results/hypothetical_prevalence.csv')
fig,ax=plt.subplots(figsize=(6.5,3.5));ax.plot(100*prev.prevalence,100*prev.ppv,'o-',color='black')
ax.set(xlabel='Assumed prevalence percent',ylabel='Positive predictive value percent',title='Hypothetical fixed sensitivity 90 percent and specificity 95 percent',ylim=(0,100))
ax.grid(axis='y',color='.85')
save(fig,'05_prevalence_and_ppv',3,
'Mathematical illustration using assumed fixed sensitivity and specificity. These are not measured screening estimates and are not transported from the diagnostic classifier.',
['results/hypothetical_prevalence.csv'],'hypothetical arithmetic')

fig,ax=plt.subplots(figsize=(6.5,2.7));ax.errorbar(.88,0,xerr=[[.88-.65],[1.18-.88]],fmt='o',color='black',capsize=6)
ax.axvline(1,color='gray',ls='--');ax.set_xlim(.5,1.4);ax.set_yticks([0],['Interval cancer ratio']);ax.set_ylim(-.7,.7)
ax.set_xlabel('AI supported screening relative to standard double reading')
ax.set_title('MASAI reported interval cancer ratio and 95 percent interval')
save(fig,'06_masai_interval_ratio',4,
'A plot of the reported MASAI interval-cancer ratio 0.88 with 95% confidence interval 0.65 to 1.18. The trial established non-inferiority under its prespecified margin; this interval does not establish superior reduction or a mortality benefit. This figure is a visualization of published summary statistics, not a reanalysis of patient data.',
['https://pubmed.ncbi.nlm.nih.gov/41620232/'],'published summary statistics')

panels('07_synthetic_data_questions',4,'Synthetic images need their own evaluation',[
('Fidelity','Do generated findings correspond to the intended biological and imaging task?'),
('Diversity','Does generation cover relevant settings and populations?'),
('Privacy','Could examples reproduce or reveal training records?'),
('Evaluation','Does improvement persist on independent real patient data?')],
'A conceptual appraisal of synthetic imaging. Plausibility alone does not establish privacy, representative coverage or clinical usefulness.',
['https://pubmed.ncbi.nlm.nih.gov/40790276/'])

flow('08_target_evidence',5,'Evidence for a candidate immune target',[
('Tumour associated alteration','Sequence evidence and matched context'),
('Expression and presentation','Distinct biological and computational questions'),
('Relevant immune recognition','Test whether the tumour target is recognized'),
('Safety and clinical evaluation','Additional evidence is required')],
'A simplified evidence map rather than an executable vaccine pipeline. Binding, presentation, recognition, safety and clinical benefit are distinct endpoints.',
['https://pubmed.ncbi.nlm.nih.gov/33038342/'])

panels('09_vaccine_endpoints',6,'Different endpoints answer different questions',[
('Feasibility','Can the investigational workflow be completed in the stated setting?'),
('Safety','What adverse events are observed and how are they assessed?'),
('Immunogenicity','What measured immune response follows the intervention?'),
('Clinical benefit','Does an appropriate comparison support improved patient outcomes?')],
'These endpoints are related but not interchangeable. Immune responses alone do not establish lower recurrence or longer survival.',
['https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-considerations-therapeutic-cancer-vaccines'])

flow('10_generation_and_evaluation',7,'Separate proposal from evidence',[
('Define the research target','Patient and tumour relevance constrain the task'),
('Generate proposals','A generative model produces candidate objects'),
('Evaluate selected properties','Predictive models and filters have limited scope'),
('Test biological claims','Experimental and clinical evidence remain necessary')],
'Generative proposal and predictive estimation play different roles. The diagram does not assert that the companion implements a biological generator or produces a clinically usable vaccine.',
['https://pubmed.ncbi.nlm.nih.gov/37433327/','https://pubmed.ncbi.nlm.nih.gov/33038342/'])

rank=pd.read_csv(ROOT/'results/fictional_priority_sensitivity.csv').sort_values('fraction_ranked_first',ascending=False)
rank=rank.loc[rank.fraction_ranked_first>0]
fig,ax=plt.subplots(figsize=(6.5,3.5));ax.bar(rank.candidate_id,rank.fraction_ranked_first,color='white',edgecolor='black',hatch='//')
ax.set(ylabel='Fraction ranked first under sampled weights',ylim=(0,1),title='Fictional candidate records under arbitrary weights')
save(fig,'11_fictional_rank_sensitivity',7,
'Executed sensitivity analysis of fictional, unitless records under arbitrary weight draws. The fractions describe this scoring exercise and are not probabilities of immunogenicity, safety or vaccine efficacy.',
['results/fictional_priority_sensitivity.csv'],'fictional feature exercise')

flow('12_reproducible_project',8,'Making a research claim inspectable',[
('Inputs and permissions','Record provenance and intended use'),
('Code and configuration','Preserve versions, seeds and selection rules'),
('Outputs and uncertainty','Keep predictions, errors and relevant limitations'),
('Independent appraisal','Separate reporting quality from clinical validity')],
'A conceptual structure for an inspectable project. Reproducibility supports appraisal but does not by itself establish external validity or clinical benefit.',
['https://pubmed.ncbi.nlm.nih.gov/38626948/'])

(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'figures_created':len(manifest),'output':str(OUT)}))
