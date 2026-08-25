import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
DATA = json.loads((ROOT / "data/projects.json").read_text(encoding="utf-8"))

def score(item):
    text = (item.get("title","") + " " + item.get("description","")).lower()
    novelty_words = ["new", "smart", "ai", "portable", "modular", "innovative", "next"]
    commercial_words = ["launch", "preorder", "limited", "early bird", "price"]
    novelty = min(25, 8 + sum(w in text for w in novelty_words) * 3)
    market = min(20, 8 + len(item.get("title","")) // 12)
    commercial = min(20, 6 + sum(w in text for w in commercial_words) * 3)
    momentum = 10
    social = 5
    risk = 0
    total = min(100, novelty + market + commercial + momentum + social - risk)
    return total, novelty, market, commercial

def make_basic_report(items):
    now = datetime.now(timezone.utc).astimezone()
    scored = []
    for item in items[:100]:
        s = score(item)
        scored.append((s[0], item, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:CONFIG.get("top_n", 10)]

    lines = [
        f"# Kickstarter 每日新品雷达 — {now.strftime('%Y-%m-%d')}",
        "",
        "> 数据发现层：公开 RSS/新闻索引；本日报用于研究和发现，不代表 Kickstarter 官方推荐。",
        "",
        f"## 🔥 今日 TOP {len(top)}",
        ""
    ]
    for i, (total, item, s) in enumerate(top, 1):
        lines += [
            f"### {i}. {item['title']}",
            f"- **评分：** {total}/100",
            f"- **发现时间：** {item.get('published','')}",
            f"- **来源：** {item.get('source','')}",
            f"- **链接：** {item.get('link','')}",
            f"- **初步亮点：** 标题/摘要显示具有产品或项目创新线索，建议进一步打开项目页核实。",
            f"- **商业机会：** {s[3]}/20（基础规则评分）",
            f"- **风险：** 需要人工核实价格、交付能力、专利/竞品及评论区反馈。",
            ""
        ]
    lines += [
        "## 🚨 重点观察",
        "",
        "优先打开评分最高的 3 个项目，重点检查：产品是否真正解决痛点、首发价格、竞品差异、交付时间、评论区反馈。",
        "",
        "## ℹ️ 说明",
        "当前版本不会直接高频抓取 Kickstarter 项目页面。若要获得融资金额、支持人数、完成率等实时字段，需要接入允许使用的数据/API 来源。",
    ]
    return "\n".join(lines)

def main():
    report = make_basic_report(DATA)
    out = ROOT / "reports" / (datetime.now().strftime("%Y-%m-%d") + ".md")
    out.write_text(report, encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()
