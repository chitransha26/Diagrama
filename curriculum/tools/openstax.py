"""Fetches OpenStax textbook text for fact-checking lessons, and searches it.

  python3 curriculum/tools/openstax.py fetch            # download all books to .cache/openstax
  python3 curriculum/tools/openstax.py find BOOK REGEX  # e.g. find biology-2e "sepals"

Text comes from openstax.org's public archive (CC BY 4.0). The cache is not committed.
"""
import concurrent.futures, html, json, os, re, sys, urllib.request

ARCHIVE = "https://openstax.org/apps/archive/20260604.144757/contents/"
BOOKS = {  # slug: book id@version, as served by the archive on 20 October 2026
    "biology-2e": "8d50a0af-948b-4204-a71d-4826cba765b8@63f8b6f",
    "chemistry-2e": "7fccc9cf-9b71-44f6-800b-f9457fd64335@3be4b60",
    "anatomy-and-physiology-2e": "4fd99458-6fdf-49bc-8688-a6dc17a1268d@716383a",
    "microbiology": "e42bd376-624b-4c0f-972f-e0c57998e765@6338502",
    "organic-chemistry": "6c2f7d1d-fbad-42e8-b977-9b903e6cb83b@8917713",
    "university-physics-volume-1": "d50f6e32-0fda-46ef-a362-9bd36ca7c97d@d0ed34a",
    "university-physics-volume-2": "7a0f9770-1c44-4acd-9920-1cd9a99f2a1e@d0ed34a",
    "university-physics-volume-3": "af275420-6050-4707-995c-57b9cc13c358@d0ed34a",
    "astronomy-2e": "4c29f9e5-a53d-42c0-bdb5-091990527d79@dff6acf",  # added 29 October 2026
}
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".cache", "openstax")


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def fetch():
    jobs = []
    for slug, book in BOOKS.items():
        tree = get(ARCHIVE + book + ".json")["tree"]
        def walk(n):
            if "contents" in n:
                for c in n["contents"]: walk(c)
            else:
                page = n["id"].split("@")[0]
                jobs.append((slug, n["slug"], ARCHIVE + f"{book}:{page}.json"))
        walk(tree)
    def one(job):
        slug, page, url = job
        path = os.path.join(CACHE, slug, page + ".json")
        if os.path.exists(path): return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        d = get(url)
        json.dump({"title": clean(d.get("title", "")), "slug": page, "text": clean(d.get("content", ""))}, open(path, "w"))
    with concurrent.futures.ThreadPoolExecutor(12) as ex:
        list(ex.map(one, jobs))
    print(f"{len(jobs)} pages cached in {os.path.normpath(CACHE)}")


def find(book, pattern, limit=8, width=220):
    rx = re.compile(pattern, re.I)
    folder = os.path.join(CACHE, book)
    for name in sorted(os.listdir(folder)):
        d = json.load(open(os.path.join(folder, name)))
        for m in rx.finditer(d["text"]):
            print(f"[{d['title']}] https://openstax.org/books/{book}/pages/{d['slug']}\n  …{d['text'][max(0, m.start() - width):m.end() + width]}…\n")
            limit -= 1
            if limit == 0: return


if __name__ == "__main__":
    if sys.argv[1] == "fetch": fetch()
    else: find(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 8)
