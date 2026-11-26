#!/usr/bin/env python3
"""Static Sphinx toctree reachability check.

Walks a docs tree (``docs`` or ``docs_zh``), follows every ``toctree`` starting
from ``index`` and reports

* orphans: source files that no toctree reaches (and that are not marked
  ``orphan: true``), and
* broken entries: toctree entries that point to a file that does not exist.

Exit status is 1 when either is found.  Standard library only.

Usage: python3 scripts/check_toctree.py [docs] [docs_zh] ...
"""
import fnmatch
import json
import os
import posixpath
import re
import sys

EXCL_DIRS = {"_build", ".ipynb_checkpoints", "_templates", "_static", "site"}
EXCL_FILES = {"overrides.mkdocs.backed", "css.mkdocs.backed"}
SUFFIXES = (".md", ".ipynb", ".rst")

BLOCK = re.compile(r"(`{3,}|:{3,})\s*\{toctree\}[^\n]*\n(.*?)\n\1", re.S)
RST = re.compile(r"\.\. toctree::[^\n]*\n((?:[ \t]+[^\n]*\n|\n)+)")
FRONT = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
ORPHAN = re.compile(r"^orphan:\s*(true|yes)\s*$", re.M | re.I)


def collect(root):
    """Map docname -> file path for every source document under ``root``."""
    docs = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # exclusions match whole path segments, never substrings
        dirnames[:] = [d for d in dirnames if d not in EXCL_DIRS]
        for fn in filenames:
            if fn in EXCL_FILES or not fn.endswith(SUFFIXES):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            docs[posixpath.splitext(rel)[0]] = path
    return docs


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def is_orphan(path):
    """True for ``orphan: true`` in md front matter / notebook metadata."""
    try:
        if path.endswith(".ipynb"):
            meta = json.loads(read(path)).get("metadata", {})
            return bool(meta.get("orphan") or (meta.get("myst") or {}).get("orphan"))
        text = read(path)
        m = FRONT.match(text)
        if m:
            return bool(ORPHAN.search(m.group(1)))
        return bool(re.match(r"\s*:orphan:", text))  # rst
    except (OSError, ValueError):
        return False


def entries(doc, path, docs):
    if path.endswith(".ipynb"):
        return []
    text = read(path)
    bodies = [m.group(2) for m in BLOCK.finditer(text)]
    bodies += [m.group(1) for m in RST.finditer(text)]
    out = []
    for body in bodies:
        glob = ":glob:" in body
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith((":", "#")):
                continue
            m = re.match(r".*<(.+)>$", line)
            tgt = m.group(1) if m else line
            if tgt.startswith(("http:", "https:", "mailto:")):
                continue
            if tgt.endswith(SUFFIXES):
                tgt = posixpath.splitext(tgt)[0]
            if tgt.startswith("/"):
                base = tgt[1:]
            else:
                base = posixpath.normpath(posixpath.join(posixpath.dirname(doc), tgt))
            if glob or "*" in base:
                out += [d for d in docs if fnmatch.fnmatch(d, base)]
            else:
                out.append(base)
    return out


def check(root):
    docs = collect(root)
    seen, stack, broken = set(), ["index"], set()
    while stack:
        d = stack.pop()
        if d in seen:
            continue
        seen.add(d)
        if d not in docs:
            broken.add(d)
            continue
        for e in entries(d, docs[d], docs):
            if e in docs:
                stack.append(e)
            else:
                broken.add(f"{d} -> {e}")
    orphans = sorted(d for d in docs if d not in seen and not is_orphan(docs[d]))
    marked = sum(1 for d in docs if d not in seen and is_orphan(docs[d]))
    return len(docs), len(seen & set(docs)), marked, orphans, sorted(broken)


def main(argv):
    roots = argv or ["docs", "docs_zh"]
    bad = False
    for root in roots:
        n, reach, marked, orphans, broken = check(root)
        print(f"{root}: docs={n} reachable={reach} marked_orphan={marked} "
              f"orphans={len(orphans)} broken={len(broken)}")
        for o in orphans:
            print(f"  ORPHAN  {o}  (add to a toctree or mark `orphan: true`)")
        for b in broken:
            print(f"  BROKEN  {b}")
        bad = bad or bool(orphans or broken)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
