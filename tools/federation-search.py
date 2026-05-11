#!/usr/bin/env python3
"""
federation-search.py — Search the leviathan-meta federation for existing work.

Solves the "founder bottleneck" problem: when starting work on a new task,
query the federation first to surface existing related artifacts before
designing from scratch.

Usage:
    federation-search.py <query>
    federation-search.py <query> --category=contracts
    federation-search.py <query> --json
    federation-search.py --list-categories
    federation-search.py --discover <topic>   # multi-keyword discovery mode

Examples:
    federation-search.py "ConstitutionRegistry"
    federation-search.py "capability_class" --category=kernel
    federation-search.py --discover "on-chain bridge"
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict


# Categories with priority weight (higher = more authoritative)
# Reflects kernel/03-constellation §3 federation hierarchy
CATEGORIES = {
    "kernel":     {"path": "kernel",       "weight": 10, "desc": "Abstract substrate (canonical)"},
    "federation": {"path": "federation",   "weight": 9,  "desc": "Federation's own constitution"},
    "contracts":  {"path": "contracts",    "weight": 8,  "desc": "Master governance contracts"},
    "briefings":  {"path": "briefings",    "weight": 7,  "desc": "Inter-agent briefings (append-only)"},
    "templates":  {"path": "templates",    "weight": 5,  "desc": "Onboarding templates"},
    "companion":  {"path": "companion",    "weight": 6,  "desc": "Master POS instance"},
    "liveprob":   {"path": "liveprob",     "weight": 6,  "desc": "Trade specialty (Polymarket)"},
    "security":   {"path": "security",     "weight": 6,  "desc": "Security domain"},
    "tasma":      {"path": "tasma",        "weight": 6,  "desc": "Animal welfare beachhead"},
    "atlas":      {"path": "atlas",        "weight": 6,  "desc": "Digital twin"},
    "anima":      {"path": "anima",        "weight": 6,  "desc": "Mass-distribution Android app"},
}

# Multi-keyword discovery: when given a topic, expand to related terms
DISCOVERY_EXPANSIONS = {
    "on-chain": ["on-chain", "onchain", "chain_writer", "ConstitutionRegistry",
                 "snapshot_hash", "Solidity", "Avalanche", "Fuji", "smart contract"],
    "contract": ["contract", "interface", "Solidity", ".sol",
                 "ICitizen", "IGovernance", "IProposal"],
    "task layer": ["task", "DecisionEntry", "capability_class",
                   "evidence_hash", "lifecycle", "outcome", "lesson"],
    "agent": ["agent", "specialty agent", "builder", "Companion",
              "ElizaOS", "moltbook"],
    "constitutional company": ["Constitutional Company", "anayasal şirket",
                                "Tasma", "Animal Welfare", "VC"],
    "sync": ["sync", "federation", "report_status", "read_member",
             ".federation", "auto-sync"],
}


def find_meta_repo() -> Path:
    """Find the leviathan-meta repo. Try common locations."""
    candidates = [
        Path.home() / "caba_yasasi" / "leviathan-meta",
        Path.home() / "leviathan-meta",
        Path.cwd().parent / "leviathan-meta",
        Path.cwd(),
    ]
    for c in candidates:
        if (c / "federation" / "manifest.yaml").exists():
            return c
        if (c / "kernel" / "manifest.yaml").exists() and (c / "federation").exists():
            return c
    raise RuntimeError(
        "leviathan-meta not found. Set LEVIATHAN_META env var or "
        "run from a directory adjacent to it."
    )


SEARCHABLE_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".sol", ".py",
                         ".toml", ".txt", ".sh"}


def python_search(path: Path, query: str) -> list:
    """Pure-Python recursive case-insensitive search.
    No external deps. Fast enough for federation docs (~1MB).
    Returns list of {file, line, snippet} matches.
    """
    if not path.exists():
        return []

    query_lower = query.lower()
    matches = []

    for filepath in path.rglob("*"):
        if not filepath.is_file():
            continue
        if filepath.suffix.lower() not in SEARCHABLE_EXTENSIONS:
            continue
        # Skip hidden files / .git
        if any(part.startswith(".git") for part in filepath.parts):
            continue

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for line_num, line in enumerate(f, 1):
                    if query_lower in line.lower():
                        matches.append({
                            "file": str(filepath),
                            "line": line_num,
                            "snippet": line.strip()[:240],
                        })
        except (PermissionError, OSError):
            continue

    return matches


def search_federation(query: str, category_filter: str = None) -> dict:
    """Search the entire federation (or a single category)."""
    repo = find_meta_repo()
    results = {}

    categories = [category_filter] if category_filter else CATEGORIES.keys()
    for cat in categories:
        if cat not in CATEGORIES:
            continue
        path = repo / CATEGORIES[cat]["path"]
        matches = python_search(path, query)
        if matches:
            results[cat] = matches

    return results


def discover(topic: str) -> dict:
    """Multi-keyword discovery mode. Expands topic to related terms."""
    expansion_keys = [k for k in DISCOVERY_EXPANSIONS if k.lower() in topic.lower()]

    # If no exact expansion, fall back to the topic itself
    keywords = []
    if expansion_keys:
        for k in expansion_keys:
            keywords.extend(DISCOVERY_EXPANSIONS[k])
    else:
        keywords = [topic]

    aggregated = defaultdict(lambda: defaultdict(list))
    seen_files = defaultdict(set)

    for kw in keywords:
        results = search_federation(kw)
        for cat, matches in results.items():
            for m in matches:
                key = f"{m['file']}:{m['line']}"
                if key not in seen_files[cat]:
                    seen_files[cat].add(key)
                    aggregated[cat][kw].append(m)

    return {
        "topic": topic,
        "keywords_used": keywords,
        "results_by_category": {
            cat: {kw: matches for kw, matches in by_kw.items()}
            for cat, by_kw in aggregated.items()
        },
    }


def format_human(results: dict, query: str) -> str:
    """Human-readable output for federation search."""
    if not results:
        return f"\n[ Federation Search ]  '{query}'  →  NO MATCHES\n"

    out = [f"\n[ Federation Search ]  '{query}'"]
    total = sum(len(v) for v in results.values())
    out.append(f"  → {total} match(es) across {len(results)} category(ies)\n")

    # Sort by category weight
    sorted_cats = sorted(results.keys(), key=lambda c: -CATEGORIES[c]["weight"])

    for cat in sorted_cats:
        matches = results[cat]
        info = CATEGORIES[cat]
        out.append(f"  ─── {cat.upper()} [{info['desc']}] — {len(matches)} match(es)")
        for m in matches[:6]:
            rel = Path(m["file"]).name
            try:
                rel = m["file"].split("leviathan-meta/")[-1]
            except Exception:
                pass
            out.append(f"    {rel}:{m['line']}")
            out.append(f"      └─ {m['snippet']}")
        if len(matches) > 6:
            out.append(f"    … and {len(matches) - 6} more")
        out.append("")

    return "\n".join(out)


def format_discover(disco: dict) -> str:
    """Human-readable output for discovery mode."""
    out = [f"\n[ Federation Discovery ]  topic='{disco['topic']}'"]
    out.append(f"  → expanded to {len(disco['keywords_used'])} keyword(s): "
               f"{', '.join(disco['keywords_used'][:10])}"
               f"{'...' if len(disco['keywords_used']) > 10 else ''}")
    out.append("")

    if not disco["results_by_category"]:
        out.append("  → NO RELATED EXISTING WORK FOUND")
        out.append("    This topic appears NEW to the federation. Proceed without")
        out.append("    rediscovery risk. (Or: try different keywords.)")
        return "\n".join(out)

    sorted_cats = sorted(
        disco["results_by_category"].keys(),
        key=lambda c: -CATEGORIES[c]["weight"]
    )

    out.append("  ⚠ EXISTING WORK FOUND — review before starting from scratch:")
    out.append("")

    for cat in sorted_cats:
        by_kw = disco["results_by_category"][cat]
        info = CATEGORIES[cat]
        total = sum(len(m) for m in by_kw.values())
        out.append(f"  ─── {cat.upper()} [{info['desc']}] — {total} hit(s)")

        for kw, matches in by_kw.items():
            for m in matches[:3]:
                rel = m["file"]
                try:
                    rel = m["file"].split("leviathan-meta/")[-1]
                except Exception:
                    pass
                out.append(f"    [{kw}] {rel}:{m['line']}")
                out.append(f"      └─ {m['snippet']}")
        out.append("")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Search the leviathan-meta federation for existing work.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("query", nargs="?", help="Search term (or topic for --discover)")
    parser.add_argument("--category", choices=list(CATEGORIES.keys()),
                        help="Limit to one category")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--list-categories", action="store_true",
                        help="List available categories with weights")
    parser.add_argument("--discover", action="store_true",
                        help="Discovery mode — multi-keyword expansion of topic")
    args = parser.parse_args()

    if args.list_categories:
        try:
            repo = find_meta_repo()
            print(f"Federation root: {repo}\n")
        except RuntimeError as e:
            print(f"WARN: {e}\n")

        print("Categories (sorted by authority weight):")
        for cat, info in sorted(CATEGORIES.items(), key=lambda x: -x[1]["weight"]):
            print(f"  {cat:12s} → {info['path']:12s} weight={info['weight']:2d}  {info['desc']}")
        print("\nDiscovery topic expansions available:")
        for topic, keywords in DISCOVERY_EXPANSIONS.items():
            print(f"  '{topic}' → {len(keywords)} keywords: "
                  f"{', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    if args.discover:
        result = discover(args.query)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_discover(result))
    else:
        results = search_federation(args.query, args.category)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(format_human(results, args.query))


if __name__ == "__main__":
    main()
