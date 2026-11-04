"""Plot overlap estimates and exact reference values from output JSON."""
import argparse,json
import numpy as np
import matplotlib.pyplot as plt
p=argparse.ArgumentParser()
p.add_argument("file",nargs="?",default="results/run.json")
a=p.parse_args()
with open(a.file,encoding="utf-8") as f: r=json.load(f)
names=[x["template"] for x in r["records"]]
means=[x["estimate"]["raw_overlap"] for x in r["records"]]
errors=[x["estimate"]["standard_error"] for x in r["records"]]
exact=[x["exact_overlap"] for x in r["records"]]
x=np.arange(len(names))
fig,ax=plt.subplots(figsize=(7,4))
ax.errorbar(x-.12,means,errors,fmt="o",capsize=4,label="sample estimate ± 1 s.e.")
ax.scatter(x+.12,exact,marker="x",label="exact")
ax.set_xticks(x,names);ax.set_ylim(-.1,1.1)
ax.set_ylabel("SWAP overlap");ax.set_title("Masked image-pattern comparison")
ax.legend();fig.tight_layout()
fig.savefig("results/overlaps.png",dpi=180)
