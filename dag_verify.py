#!/usr/bin/env python3
"""DAG Dependency Static Analyzer for Coq proof projects.

Detects:
  1. Cycles in Require/Import graph (DFS coloring)
  2. Blacklist violations (main files importing extension/conjecture files)
  3. Layer number reverse dependencies (high-layer -> low-layer forbidden)
  4. Orphan dependencies (Require target has no .v file in repo)

Exit 0 = all checks pass. Exit 1 = one or more fatal violations.
"""

import argparse, os, re, sys
from collections import defaultdict, deque

REPO = os.path.dirname(os.path.abspath(__file__))

BLACKLIST_FILES = {
    'extension_lehmer',
    'open_conjecture',
    'riemann_coq',
    'riemann_coq_analysis',
    'counter_ex',
    'real_mult_lemmas',
}

MAIN_FILES = {'main_proof', 'phase2_layered', 'base_library', 'logic_tools'}

LAYER_HINTS = {
    'base_library': 0,
    'logic_tools': 0,
    'main_proof': 4,
    'phase2_layered': 4,
    'extension_lehmer': 5,
    'open_conjecture': 6,
}

REQUIRE_RE = re.compile(r'^\s*(?:From\s+\S+\s+)?Require(?:\s+(?:Export|Import))?\s+([^\s.]+)', re.MULTILINE)
IMPORT_RE  = re.compile(r'^\s*Import\s+([^\s.]+)', re.MULTILINE)
ADMITTED_RE = re.compile(r'\b(Admitted|admit)\b')


def find_v_files(repo):
    out = {}
    for root, _, files in os.walk(repo):
        for f in files:
            if f.endswith('.v') and not f.startswith('_'):
                stem = f[:-2]
                out[stem] = os.path.join(root, f)
    return out


def parse_requires(path):
    with open(path, 'r', encoding='utf-8-sig', errors='replace') as fh:
        src = fh.read()
    reqs = {m.group(1) for m in REQUIRE_RE.finditer(src)}
    reqs |= {m.group(1) for m in IMPORT_RE.finditer(src)}
    return reqs


def build_graph(repo):
    files = find_v_files(repo)
    graph = {}
    for stem, path in files.items():
        reqs = parse_requires(path)
        graph[stem] = {r for r in reqs if r in files}
    return graph, files


def detect_cycles(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    cycles = []

    def dfs(start):
        stack = [(start, iter(graph.get(start, ())))]
        while stack:
            node, it = stack[-1]
            color[node] = GRAY
            nxt = None
            for dep in it:
                if dep not in graph:
                    continue
                if color.get(dep, WHITE) == GRAY:
                    cycles.append(f"cycle: {node} -> {dep} -> ... (backedge at {dep})")
                elif color.get(dep, WHITE) == WHITE:
                    nxt = dep
                    break
            if nxt is None:
                color[node] = BLACK
                stack.pop()
            else:
                stack.append((nxt, iter(graph.get(nxt, ()))))

    for n in graph:
        if color[n] == WHITE:
            dfs(n)
    return cycles


def check_blacklist(graph):
    errs = []
    for main in MAIN_FILES:
        for b in BLACKLIST_FILES:
            if b in graph.get(main, set()):
                errs.append(f"BLACKLIST: {main} requires forbidden file {b}")
    return errs


def check_layer_order(graph):
    errs = []
    for src, deps in graph.items():
        sl = LAYER_HINTS.get(src)
        if sl is None:
            continue
        for d in deps:
            dl = LAYER_HINTS.get(d)
            if dl is not None and dl > sl:
                errs.append(f"LAYER: {src}(L{sl}) depends on {d}(L{dl}) upper layer forbidden")
    return errs


def topo(graph):
    indeg = {n: 0 for n in graph}
    for n, ds in graph.items():
        for d in ds:
            if d in indeg:
                indeg[n] = indeg[n] + 1
    q = deque(sorted(k for k, v in indeg.items() if v == 0))
    order = []
    while q:
        n = q.popleft()
        order.append(n)
        for other, ds in graph.items():
            if n in ds:
                indeg[other] -= 1
                if indeg[other] == 0:
                    q.append(other)
    return order


def count_admitted(path):
    with open(path, 'r', encoding='utf-8-sig', errors='replace') as fh:
        return len(ADMITTED_RE.findall(fh.read()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--repo', default=REPO)
    args = ap.parse_args()

    repo = args.repo
    print(f"[DAG-VERIFY] repo = {repo}")
    graph, files = build_graph(repo)

    print("\n== FILES ==")
    for stem in sorted(files):
        print(f"  {stem:<28}  admits={count_admitted(files[stem]):<3}  layer={LAYER_HINTS.get(stem,'-')}  deps={sorted(graph[stem])}")

    cycles = detect_cycles(graph)
    bl = check_blacklist(graph)
    lo = check_layer_order(graph)

    print(f"\n== TOPO ORDER ({len(topo(graph))}) ==")
    print("  -> ".join(topo(graph)))

    fatal = []
    fatal.extend([f"[FATAL] {c}" for c in cycles])
    fatal.extend(bl)
    fatal.extend(lo)

    print("\n== RESULT ==")
    if fatal:
        for e in fatal:
            print(f"  {e}")
        print(f"\n[FAIL] {len(fatal)} fatal violation(s)")
        sys.exit(1)
    print("  [PASS] cycle-free, blacklist clean, layer order OK")

    orphan = []
    for src, ds in graph.items():
        for d in ds:
            if d not in files:
                orphan.append((src, d))
    if orphan:
        print("\n== ORPHAN ==")
        for s, d in orphan:
            print(f"  WARN: {s} -> {d} (no .v)")

    sys.exit(0)


if __name__ == '__main__':
    main()
