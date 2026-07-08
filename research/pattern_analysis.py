import json
import os
from collections import Counter, defaultdict

def analyze_patterns():
    dataset_path = "/Users/aadityamohansamadhiya/Composio/composio-agent-research/dataset.json"
    if not os.path.exists(dataset_path):
        print(f"[Error] dataset.json not found at {dataset_path}")
        return

    with open(dataset_path, "r") as f:
        data = json.load(f)

    total_apps = len(data)
    
    # 1. Authentication Distribution
    auth_counter = Counter()
    for app in data:
        # Each app has a list of auth methods (e.g. ["OAuth2", "API Key"])
        for method in app["auth_methods"]:
            auth_counter[method] += 1
            
    auth_dist = {k: v for k, v in auth_counter.most_common()}
    
    # 2. Self-Serve vs Gated status
    self_serve_dist = Counter([app["self_serve"] for app in data])
    
    # 3. Category Analaysis (Self-Serve vs Gated per category, average buildability score)
    category_metrics = defaultdict(lambda: {"total": 0, "self_serve": 0, "gated": 0, "paid_plan": 0, "contact_sales": 0, "partner_only": 0, "free_trial": 0, "scores": []})
    
    for app in data:
        cat = app["category"]
        ss = app["self_serve"]
        score = app["buildability"]["score"]
        
        category_metrics[cat]["total"] += 1
        category_metrics[cat]["scores"].append(score)
        
        if ss == "Self-Serve":
            category_metrics[cat]["self_serve"] += 1
        elif ss == "Paid Plan":
            category_metrics[cat]["paid_plan"] += 1
        elif ss == "Contact Sales":
            category_metrics[cat]["contact_sales"] += 1
        elif ss == "Partner Only":
            category_metrics[cat]["partner_only"] += 1
        elif ss == "Free Trial":
            category_metrics[cat]["free_trial"] += 1
        else:
            category_metrics[cat]["gated"] += 1
            
    category_summary = {}
    for cat, metrics in category_metrics.items():
        avg_score = sum(metrics["scores"]) / len(metrics["scores"])
        self_serve_pct = (metrics["self_serve"] / metrics["total"]) * 100
        category_summary[cat] = {
            "total": metrics["total"],
            "self_serve_count": metrics["self_serve"],
            "self_serve_percentage": round(self_serve_pct, 1),
            "average_score": round(avg_score, 1),
            "breakdown": {
                "Self-Serve": metrics["self_serve"],
                "Paid Plan": metrics["paid_plan"],
                "Contact Sales": metrics["contact_sales"],
                "Partner Only": metrics["partner_only"],
                "Free Trial": metrics["free_trial"],
                "Other Gated": metrics["gated"]
            }
        }
        
    # 4. Main Blockers
    blockers_dist = Counter([app["buildability"]["blocker"] for app in data if app["buildability"]["blocker"] != "None"])
    
    # 5. API Surface type (REST, GraphQL, Both, CLI, None)
    api_type_dist = Counter([app["api_surface"]["type"] for app in data])
    
    # 6. API Scope (Broad, Medium, Narrow, None)
    api_scope_dist = Counter([app["api_surface"]["scope"] for app in data])
    
    # 7. MCP Availability
    mcp_dist = Counter([app["api_surface"]["has_mcp"] for app in data])
    
    # 8. Toolkit Readiness Verdict
    verdict_dist = Counter([app["buildability"]["verdict"] for app in data])

    # 9. Cluster identification / Key Observations
    # Easy wins: Buildability score >= 95 and has MCP or broad API and self-serve
    easy_wins = []
    outreach_needed = []
    
    for app in data:
        score = app["buildability"]["score"]
        name = app["name"]
        cat = app["category"]
        ss = app["self_serve"]
        blocker = app["buildability"]["blocker"]
        
        if score >= 95 and ss in ["Self-Serve", "Free Trial"]:
            easy_wins.append({
                "id": app["id"],
                "name": name,
                "category": cat,
                "score": score,
                "has_mcp": app["api_surface"]["has_mcp"],
                "api_type": app["api_surface"]["type"]
            })
        elif ss in ["Contact Sales", "Partner Only"] or blocker in ["Contact Sales", "Partner Program"]:
            outreach_needed.append({
                "id": app["id"],
                "name": name,
                "category": cat,
                "score": score,
                "blocker": blocker
            })
            
    report = {
        "total_apps": total_apps,
        "auth_distribution": auth_dist,
        "self_serve_distribution": dict(self_serve_dist),
        "category_summary": category_summary,
        "blockers_distribution": dict(blockers_dist),
        "api_type_distribution": dict(api_type_dist),
        "api_scope_distribution": dict(api_scope_dist),
        "mcp_distribution": dict(mcp_dist),
        "verdict_distribution": dict(verdict_dist),
        "metrics": {
            "easy_wins_count": len(easy_wins),
            "outreach_needed_count": len(outreach_needed),
            "ready_count": verdict_dist.get("Ready", 0),
            "gated_count": verdict_dist.get("Gated", 0),
            "blocked_count": verdict_dist.get("Blocked", 0)
        },
        "clusters": {
            "easy_wins": sorted(easy_wins, key=lambda x: x["score"], reverse=True)[:15],
            "outreach_needed": sorted(outreach_needed, key=lambda x: x["score"])[:15]
        }
    }
    
    report_path = "/Users/aadityamohansamadhiya/Composio/composio-agent-research/research/patterns_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print("="*60)
    print("             PATTERN ANALYSIS COMPLETED               ")
    print("="*60)
    print(f"Total SaaS Apps Analyzed: {total_apps}")
    print(f"Toolkit Ready Apps:       {verdict_dist.get('Ready', 0)}")
    print(f"Gated Apps:               {verdict_dist.get('Gated', 0)}")
    print(f"Blocked Apps:             {verdict_dist.get('Blocked', 0)}")
    print("-"*60)
    print("Top Authentication Methods:")
    for method, count in auth_counter.most_common(3):
        print(f"  {method}: {count} ({round(count/total_apps*100, 1)}%)")
    print("Top Integration Blockers:")
    for blocker, count in blockers_dist.most_common(3):
        print(f"  {blocker}: {count}")
    print("="*60)
    print(f"Patterns report saved to: {report_path}")

if __name__ == "__main__":
    analyze_patterns()
