from pathlib import Path
import csv, collections
base=Path(__file__).resolve().parent

def read(name):
    with (base/name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

r=read("run_manifest.csv");e=read("eval_manifest.csv")
assert len(r)==60 and len({x["run_id"] for x in r})==60,(len(r),"run duplicates")
assert len(e)==300 and len({x["eval_id"] for x in e})==300,(len(e),"eval duplicates")
rmap={x["run_id"]:x for x in r};group=collections.defaultdict(list)
for x in e:
    assert x["run_id"] in rmap
    group[x["run_id"]].append(x)
for run_id,events in group.items():
    run=rmap[run_id];expected=list(map(int,run["eval_positions"].split(";")))
    positions=[int(x["checkpoint_progress"]) for x in sorted(events,key=lambda x:int(x["eval_index"]))]
    assert positions==expected,(run_id,positions,expected)
    assert len(events)==5
assert sum(int(x["episodes"]) for x in e)==21000
print("PASS: 60 unique training runs, 300 scheduled eval points, 21000 rollout episodes")
