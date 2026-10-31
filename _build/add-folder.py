#!/usr/bin/env python3
"""
add-folder.py — install every page JSON in a folder, in one go.

    python3 _build/add-folder.py ~/Downloads/clinipd-drafts

Runs add-page.py's validation over each file, installs the clean ones,
skips the broken ones, and prints a table at the end telling you which
is which. Nothing half-installs: a file either passes or is left alone.

    --force    install files that have errors (not recommended)
"""
import io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADD = os.path.join(HERE, "add-page.py")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if not args:
        print("\n  Give me a folder:  python3 _build/add-folder.py <folder>\n")
        sys.exit(1)

    folder = os.path.expanduser(args[0])
    if not os.path.isdir(folder):
        print("\n  Not a folder: %s\n" % folder)
        sys.exit(1)

    files = sorted(f for f in os.listdir(folder)
                   if f.lower().endswith(".json") and not f.startswith("."))
    if not files:
        print("\n  No .json files in %s\n" % folder)
        sys.exit(1)

    print("\n  %d file(s) in %s" % (len(files), folder))
    print("  " + "-" * 68)

    done, failed = [], []
    for f in files:
        path = os.path.join(folder, f)
        cmd = [sys.executable, "-I", ADD, path]
        if force:
            cmd.append("--force")
        r = subprocess.run(cmd, capture_output=True, text=True)

        out = r.stdout + r.stderr
        pid = ""
        for line in out.splitlines():
            if line.strip().startswith("Page "):
                pid = line.split(None, 1)[1].strip()
        warns = [l.split("WARNING", 1)[1].strip() for l in out.splitlines() if "WARNING" in l]
        errs = [l.split("ERROR", 1)[1].strip() for l in out.splitlines() if "ERROR" in l]

        if r.returncode == 0:
            done.append((f, pid, warns))
            mark = "ok  " if not warns else "warn"
            print("  %-4s %-46s %s" % (mark, f[:46], pid or ""))
            for w in warns:
                print("       - %s" % w)
        else:
            failed.append((f, errs))
            print("  FAIL %-46s" % f[:46])
            for e in errs:
                print("       - %s" % e)
            if not errs:
                print("       - %s" % out.strip().splitlines()[-1][:70])

    print("  " + "-" * 68)
    print("  installed %d  ·  failed %d" % (len(done), len(failed)))

    man = os.path.join(os.path.dirname(HERE), "content", "index.json")
    if os.path.exists(man):
        import json
        d = json.load(io.open(man, encoding="utf-8"))
        written = sum(1 for v in d.values() if v.get("sections"))
        reviewed = sum(1 for v in d.values() if v.get("status") == "reviewed")
        print("  %d page(s) written across the site, %d verified" % (written, reviewed))

    if failed:
        print("\n  Fix the failures and re-run — the installed ones are left alone.")
    else:
        print("\n  Next:  open the DOIs, then  ./_build/deploy.sh")
    print()


main()
