"""The documentation site's translations: docs/<lang>/<page>.md beside the English docs/<page>.md.

    python tools/docs_i18n.py hashes              write docs/_data/i18n_sources.yml (each English page's hash)
    python tools/docs_i18n.py status [--lang xx]  per language: pages missing, outdated (English changed since), current
    python tools/docs_i18n.py todo --lang xx      the pages of one language that need (re)translating, one per line
    python tools/docs_i18n.py svg-strings         write docs/assets/i18n/svg/en.json: every label of the drawn pictures
    python tools/docs_i18n.py svg-build [--lang xx]   docs/assets/img/<lang>/*.svg from docs/assets/i18n/svg/<lang>.json
    python tools/docs_i18n.py finish --lang xx [pages...]  stamp translated pages (lang, source, source_hash, menu
                                                  and search flags) and point their pictures and links at the right files
    python tools/docs_i18n.py check               exit 1 when i18n_sources.yml or svg/en.json is stale

A translation records the hash of the English text it was made from (`source_hash`, the first 12 hex
digits of sha256 of the English file). When the English page changes, the site marks the translation
as older and links the English page; a page with no translation falls back to the English one.
Terminal pictures (program output) stay English; drawn pictures get one copy per language.
Pages generated from the code (marked "generated" and "do not edit" near the top) are not translated.
See docs/maintaining.md for the whole workflow."""
import hashlib, html, json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DOCS = os.path.join(ROOT, "docs")
IMG = os.path.join(DOCS, "assets", "img")
SVGI18N = os.path.join(DOCS, "assets", "i18n", "svg")
LANGS = ["de", "fr", "es", "it", "pt", "nl", "pl", "cs", "sk", "sl", "hr", "bs", "sr", "mk", "bg", "ro", "hu", "el",
         "sq", "tr", "da", "sv", "no", "fi", "is", "et", "lv", "lt", "ga", "mt", "lb", "ca", "uk", "ru", "be", "ja",
         "ko", "zh", "zh-Hant"]
TEXT = re.compile(r"(<text\b[^>]*>)(.*?)(</text>)", re.S)
TSPAN = re.compile(r"(<tspan\b[^>]*>)(.*?)(</tspan>)", re.S)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def generated(text):
    body = re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.S)[:500].lower()
    return re.search(r"(?m)^\s*generated from the code", body) is not None or ("generated" in body and "do not edit" in body)


def english_pages():
    out = {}
    for n in sorted(os.listdir(DOCS)):
        p = os.path.join(DOCS, n)
        if n.endswith(".md") and os.path.isfile(p):
            t = read(p)
            if not generated(t):
                out[n] = hashlib.sha256(t.encode("utf-8")).hexdigest()[:12]
    return out


def front(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return {}, [], text
    lines = m.group(1).split("\n")
    d = {}
    for l in lines:
        k, _, v = l.partition(":")
        if _ and not l.startswith((" ", "\t", "-")):
            d[k.strip()] = v.strip()
    return d, lines, text[m.end():]


def hashes_yaml(pages):
    return "# The English pages' hashes; written by tools/docs_i18n.py hashes. Do not edit.\n" + "".join(
        f"{n}: \"{h}\"\n" for n, h in pages.items())


def cmd_hashes():
    write(os.path.join(DOCS, "_data", "i18n_sources.yml"), hashes_yaml(english_pages()))
    print("wrote docs/_data/i18n_sources.yml")


def lang_state(lang, pages):
    miss, old, ok = [], [], []
    for n, h in pages.items():
        p = os.path.join(DOCS, lang, n)
        if not os.path.exists(p):
            miss.append(n)
        else:
            (ok if front(read(p))[0].get("source_hash", "").strip('"') == h else old).append(n)
    return miss, old, ok


def cmd_status(args):
    pages = english_pages()
    for lang in ([args[args.index("--lang") + 1]] if "--lang" in args else LANGS):
        miss, old, ok = lang_state(lang, pages)
        print(f"{lang:8} current {len(ok):3}  outdated {len(old):3}  missing {len(miss):3}"
              + (f"  outdated: {' '.join(old)}" if old else ""))


def cmd_todo(args):
    lang = args[args.index("--lang") + 1]
    miss, old, _ = lang_state(lang, english_pages())
    print("\n".join(sorted(miss + old)))


def terminal(svg):
    return "#1e1f24" in svg[:2000]


def svg_files():
    return sorted(n for n in os.listdir(IMG) if n.endswith(".svg") and not terminal(read(os.path.join(IMG, n))))


def labels(svg):
    out = []
    for m in TEXT.finditer(svg):
        inner = m.group(2)
        parts = [t.group(2) for t in TSPAN.finditer(inner)] if "<tspan" in inner else [inner]
        for s in parts:
            s = html.unescape(re.sub(r"<[^>]+>", "", s)).replace(" ", " ").strip()
            if s and re.search(r"[A-Za-z]", s):
                out.append(s)
    return out


def strings_json():
    d = {}
    for n in svg_files():
        for s in labels(read(os.path.join(IMG, n))):
            d[s] = s
    return json.dumps(dict(sorted(d.items())), ensure_ascii=False, indent=1) + "\n"


def cmd_svg_strings():
    write(os.path.join(SVGI18N, "en.json"), strings_json())
    print("wrote docs/assets/i18n/svg/en.json")


def translate_svg(svg, table):
    def one(s):
        key = html.unescape(re.sub(r"<[^>]+>", "", s)).replace(" ", " ").strip()
        if key in table and table[key] and table[key] != key:
            lead = s[: len(s) - len(s.lstrip())]
            return lead + html.escape(table[key], quote=False)
        return s

    def text(m):
        inner = m.group(2)
        if "<tspan" in inner:
            inner = TSPAN.sub(lambda t: t.group(1) + one(t.group(2)) + t.group(3), inner)
        elif "<" not in inner:
            inner = one(inner)
        return m.group(1) + inner + m.group(3)
    return TEXT.sub(text, svg)


def cmd_svg_build(args):
    langs = [args[args.index("--lang") + 1]] if "--lang" in args else LANGS
    for lang in langs:
        p = os.path.join(SVGI18N, f"{lang}.json")
        if not os.path.exists(p):
            continue
        table = json.loads(read(p))
        for n in svg_files():
            write(os.path.join(IMG, lang, n), translate_svg(read(os.path.join(IMG, n)), table))
        print(lang, len(svg_files()), "pictures")


LINK = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")
SRC = re.compile(r"(<img\b[^>]*\bsrc=\")([^\"]+)(\")")


def fix_target(lang, t):
    if re.match(r"^[a-z][a-z0-9+.-]*:|^#|^/", t):
        return t
    path, sep, frag = t.partition("#")
    if path.startswith("../"):
        rest = path[3:]
        if "/" not in rest and rest.endswith(".md") and os.path.exists(os.path.join(DOCS, lang, rest)):
            return rest + sep + frag
        if rest.startswith("assets/img/") and rest.endswith(".svg") and os.path.exists(os.path.join(IMG, lang, rest[11:])):
            return f"../assets/img/{lang}/{rest[11:]}" + sep + frag
        return t
    if path.startswith("assets/img/") and path.endswith(".svg"):
        name = path[len("assets/img/"):]
        if os.path.exists(os.path.join(IMG, lang, name)):
            return f"../assets/img/{lang}/{name}" + sep + frag
        return "../" + path + sep + frag
    if path.endswith(".md") and "/" not in path:
        if os.path.exists(os.path.join(DOCS, lang, path)) or not os.path.exists(os.path.join(DOCS, path)):
            return t
        return "../" + t
    return "../" + t


HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


def headings(body):
    out, fence = [], False
    for i, l in enumerate(body.split(chr(10))):
        if l.lstrip().startswith(("```", "~~~")):
            fence = not fence
        elif not fence:
            m = HEAD.match(l)
            if m:
                out.append((i, len(m.group(1)), m.group(2)))
    return out


def slug(text, seen):
    m = re.search(r"\{#([\w-]+)\}\s*$", text)
    if m:
        return m.group(1)
    t = re.sub(r"<[^>]+>|`|\*|_(?=\w)|\[|\]\([^)]*\)|\]", "", text).lower()
    t = re.sub(r"^[^a-z]+", "", t)
    t = re.sub(r"[^a-z0-9 -]", "", t).replace(" ", "-") or "section"
    n = seen.get(t, 0)
    seen[t] = n + 1
    return t if n == 0 else f"{t}-{n}"


def keep_ids(body, english):
    """Give the translated headings the English headings' ids, so every #anchor still lands."""
    en, tr = headings(english), headings(body)
    if len(en) != len(tr) or any(a[1] != b[1] for a, b in zip(en, tr)):
        return body
    lines, seen = body.split(chr(10)), {}
    for (_, _, et), (i, _, tt) in zip(en, tr):
        sid = slug(et, seen)
        if not re.search(r"\{#[\w-]+\}\s*$", tt):
            lines[i] = lines[i].rstrip() + " {#" + sid + "}"
    return chr(10).join(lines)


def cmd_finish(args):
    lang = args[args.index("--lang") + 1]
    rest = [a for a in args if a not in ("--lang", lang)]
    pages = english_pages()
    folder = os.path.join(DOCS, lang)
    names = rest or sorted(n for n in os.listdir(folder) if n.endswith(".md"))
    for n in names:
        p = os.path.join(folder, n)
        d, lines, body = front(read(p))
        en_d = front(read(os.path.join(DOCS, n)))[0] if os.path.exists(os.path.join(DOCS, n)) else {}
        keep = {"title": d.get("title") or en_d.get("title", n[:-3])}
        if en_d.get("nav_order"):
            keep["nav_order"] = en_d["nav_order"]
        # Named pages were just (re)translated: they take the English page's hash now. Without names,
        # a page keeps the hash it has, so a fix-up run never hides that the English moved on.
        old = d.get("source_hash", "").strip('"')
        stamp = pages.get(n, "") if (rest or not old) else old
        title = keep["title"]
        if ":" in title and not title.startswith(('"', "'")):
            keep["title"] = '"' + title.replace('"', '\\"') + '"'
        keep.update({"lang": f"\"{lang}\"", "source": n, "source_hash": f"\"{stamp}\"",
                     "nav_exclude": "true", "search_exclude": "true"})
        if n == "index.md":
            keep["permalink"] = f"/{lang}/"
        if os.path.exists(os.path.join(DOCS, n)):
            body = keep_ids(body, front(read(os.path.join(DOCS, n)))[2])
        body = LINK.sub(lambda m: m.group(1) + fix_target(lang, m.group(2)) + m.group(3), body)
        body = SRC.sub(lambda m: m.group(1) + fix_target(lang, m.group(2)) + m.group(3), body)
        write(p, "---\n" + "".join(f"{k}: {v}\n" for k, v in keep.items()) + "---\n" + body.lstrip("\n").replace("\r\n", "\n"))
    print(lang, len(names), "pages stamped")


def cmd_check():
    bad = 0
    p = os.path.join(DOCS, "_data", "i18n_sources.yml")
    if not os.path.exists(p) or read(p) != hashes_yaml(english_pages()):
        print("docs/_data/i18n_sources.yml is stale: run `python tools/docs_i18n.py hashes`"); bad = 1
    p = os.path.join(SVGI18N, "en.json")
    if svg_files() and (not os.path.exists(p) or read(p) != strings_json()):
        print("docs/assets/i18n/svg/en.json is stale: run `python tools/docs_i18n.py svg-strings`"); bad = 1
    sys.exit(bad)


if __name__ == "__main__":
    a = sys.argv[1:]
    if "-h" in a or "--help" in a:
        a = []
    {"hashes": lambda: cmd_hashes(), "status": lambda: cmd_status(a), "todo": lambda: cmd_todo(a),
     "svg-strings": lambda: cmd_svg_strings(), "svg-build": lambda: cmd_svg_build(a),
     "finish": lambda: cmd_finish(a[1:]), "check": lambda: cmd_check()}.get(a[0] if a else "", lambda: print(__doc__))()
