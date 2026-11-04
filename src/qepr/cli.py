"""Command line entry point."""
import argparse
import json
from .runner import execute

def main():
    p = argparse.ArgumentParser(description="Pauli-masked quantum image recognition")
    p.add_argument("--mode",choices=["aer","ibm"],default="aer")
    p.add_argument("--backend",default=None)
    p.add_argument("--shots",type=int,default=4096)
    p.add_argument("--seed",type=int,default=7)
    p.add_argument("--output",default="results/run.json")
    args = p.parse_args()
    data = execute(args.mode,args.shots,args.backend,args.seed,args.output)
    print(json.dumps({"mode":data["mode"],"backend":data["backend"],
                      "job_id":data["job_id"],"prediction":data["prediction"],
                      "records":[{"template":r["template"],**r["estimate"],
                                  "exact_overlap":r["exact_overlap"]} for r in data["records"]]},indent=2))

if __name__ == "__main__": main()
