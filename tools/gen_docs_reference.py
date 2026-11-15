"""Write docs/cli-reference.md from the code itself, so the reference cannot drift.

The options come from the program's own `--help`; the columns and the match
document's keys from a conversion of the synthetic demo the tests build.

    python tools/gen_docs_reference.py          # rewrite the page
    python tools/gen_docs_reference.py --check  # exit 1 when the page is stale
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "cli-reference.md"
COMMAND = "heat3d-squad-demo"


def run(args):
    env = dict(os.environ, HEAT3D_NO_UPDATE="1", COLUMNS="88", PYTHONIOENCODING="utf-8",
               PYTHONPATH=str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    r = subprocess.run([sys.executable, "-m", "heat3d_ext_squad"] + args, capture_output=True, text=True,
                       env=env, encoding="utf-8", cwd=ROOT)
    return (r.stdout or r.stderr).rstrip().replace("__main__.py", COMMAND)


def outputs():
    sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
    import pyarrow.parquet as pq
    from test_stream import synthetic_demo
    from heat3d_ext_squad import load
    from heat3d_ext_squad.output import write
    lines = []
    with tempfile.TemporaryDirectory() as tmp:
        demo = Path(tmp) / "example.replay"
        demo.write_bytes(synthetic_demo())
        data, doc = write(load(demo), Path(tmp) / "out")
        for title, path in [("The table: `<demo>.parquet`", data),
                            ("Sidecar: `<demo>.entities.parquet`", data.with_name("example.entities.parquet")),
                            ("Sidecar: `<demo>.packets.parquet`", data.with_name("example.packets.parquet"))]:
            schema = pq.read_schema(path)
            lines += [f"### {title}", "", "| Column | Type |", "|---|---|"]
            lines += [f"| `{f.name}` | {str(f.type).replace('dictionary<values=string, indices=int32, ordered=0>', 'string')} |" for f in schema]
            lines.append("")
        keys = json.loads(doc.read_text(encoding="utf-8")).keys()
        lines += ["### The match document: `<demo>.match.json`", "", "Top-level keys: " + ", ".join(f"`{k}`" for k in keys) + ".", ""]
    return lines


def build():
    top = run(["--help"])
    out = ["---", "title: Command reference", "nav_order: 90", "---", "", "# Command reference", "",
           "Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.",
           "The other pages explain each step.", "", f"## `{COMMAND}`", "", "```text", top, "```", "",
           "## Output columns", ""]
    return "\n".join(out + outputs())


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text(encoding="utf-8") == text else 1)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT))
