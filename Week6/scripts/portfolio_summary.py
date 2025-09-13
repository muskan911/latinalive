import os, json, csv

BASE = "Week6/storage/portfolios"
OUT = "Week6/storage/portfolio_summary.csv"

def summarize():
    rows = []
    for f in os.listdir(BASE):
        if f.endswith(".json"):
            path = os.path.join(BASE, f)
            with open(path, encoding="utf-8") as fp:
                data = json.load(fp)
            student = data.get("student","?")
            panels = len(data.get("panels",[]))
            words = sum(len(p.get("latin","").split()) for p in data.get("panels",[]))
            score = data.get("score","-")
            rows.append([student, panels, words, score])
    with open(OUT, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out)
        w.writerow(["Student","Panels","Total Words","Exercise Score"])
        w.writerows(rows)
    print(f"Saved summary to {OUT}")

if __name__=="__main__":
    summarize()
