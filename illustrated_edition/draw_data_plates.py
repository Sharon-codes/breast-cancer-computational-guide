"""Additional scientific views of saved calculations and published statistics."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT.parent/'results'
ART=ROOT/'art'
NAVY='#162B3C';TEAL='#176B73';CORAL='#B65E45'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':NAVY,'text.color':NAVY,'xtick.color':NAVY,'ytick.color':NAVY})

def save(fig,name):
    fig.savefig(ART/(name+'.png'),dpi=300,bbox_inches='tight',facecolor='white')
    fig.savefig(ART/(name+'.pdf'),bbox_inches='tight',facecolor='white')
    plt.close(fig)

def main():
    a=json.loads((RESULTS/'analysis.json').read_text())['diagnostic']
    names=['sensitivity','specificity','positive_predictive_value','negative_predictive_value','accuracy']
    labels=['Sensitivity','Specificity','Positive predictive value','Negative predictive value','Accuracy']
    ints=a['proportion_intervals']['intervals']
    estimates=np.array([a['model'][k] for k in names]);low=np.array([ints[k]['lower'] for k in names]);up=np.array([ints[k]['upper'] for k in names])
    fig,ax=plt.subplots(figsize=(7.6,4.8));fig.subplots_adjust(left=.29,right=.80,top=.81,bottom=.20)
    ys=np.arange(5)[::-1]
    ax.errorbar(100*estimates,ys,xerr=[100*np.maximum(0,estimates-low),100*np.maximum(0,up-estimates)],fmt='o',color=TEAL,ecolor=TEAL,ms=7,capsize=5,lw=2)
    ax.set_yticks(ys,labels);ax.set_xlim(75,101);ax.set_ylim(-.6,4.6);ax.set_xlabel('Proportion percent');ax.set_xticks([75,80,85,90,95,100]);ax.grid(axis='x',color='#DFE5E8',lw=.6)
    for y,k,e in zip(ys,names,estimates):
        ax.text(102,y,f"{ints[k]['numerator']} / {ints[k]['denominator']}\n{100*e:.2f}%",va='center',ha='left',fontsize=10.5,clip_on=False)
    fig.suptitle('Internal holdout proportions and sampling uncertainty',x=.04,y=.98,ha='left',fontsize=14,weight='bold')
    fig.text(.04,.87,'Executed internal holdout  •  143 diagnostic cases  •  threshold 0.5',fontsize=11)
    fig.text(.04,.035,'Points are observed proportions; lines are 95% Wilson intervals.\nThese intervals do not measure training instability or performance in a new population.',fontsize=10.5)
    save(fig,'ch08_plate')
    p=pd.read_csv(RESULTS/'hypothetical_prevalence.csv')
    fig,ax=plt.subplots(figsize=(7.2,3.5));fig.subplots_adjust(left=.12,right=.96,bottom=.23,top=.81)
    ax.plot(100*p.prevalence,100*p.ppv,'o-',color=TEAL,lw=2,ms=6)
    ax.set(xlabel='Assumed prevalence percent',ylabel='PPV (%)',xlim=(-.2,10.4),ylim=(0,100))
    ax.grid(axis='y',color='#DFE5E8')
    fig.text(.04,.96,'The denominator changes with prevalence',fontsize=14,weight='bold',va='top')
    fig.text(.04,.865,'Hypothetical fixed sensitivity 90% and specificity 95%',fontsize=11)
    save(fig,'legacy_prevalence')
    fig,ax=plt.subplots(figsize=(7.2,3.2));fig.subplots_adjust(left=.08,right=.95,bottom=.25,top=.75)
    ax.errorbar(.88,0,xerr=[[.23],[.30]],fmt='o',color=TEAL,ms=8,capsize=6,lw=2)
    ax.axvline(1,ls='--',color=CORAL,lw=1.2);ax.text(1.01,.35,'Ratio 1',fontsize=10.5,color=CORAL)
    ax.set(xlim=(.5,1.4),ylim=(-.6,.6),xlabel='Interval cancer ratio',yticks=[])
    fig.text(.04,.96,'MASAI interval cancer endpoint',fontsize=14,weight='bold',va='top')
    fig.text(.04,.835,'Reported ratio 0.88  •  95% confidence interval 0.65 to 1.18',fontsize=11)
    save(fig,'legacy_masai')
    records=json.loads((ROOT/'scientific_plate_sources.json').read_text());records=[r for r in records if r['chapter']!=8]
    records.append({'chapter':8,'file':'ch08_plate.png','original_file':'analysis.json','source_page':'https://github.com/Sharon-codes/breast-cancer-computational-guide/commit/64f8e9996d8d7c940b8ac26177ced6fd8702c7f6','artist':'Original plot of the recorded companion analysis','license':'Original numerical analysis figure','changes':'Saved estimates and Wilson intervals plotted without refitting','retrieved':'2026-10-24','kind':'Executed internal diagnostic analysis'})
    (ROOT/'scientific_plate_sources.json').write_text(json.dumps(sorted(records,key=lambda x:x['chapter']),indent=2))
    print('Created the Chapter 8 uncertainty plate and two redesigned data plots')

if __name__=='__main__':main()
