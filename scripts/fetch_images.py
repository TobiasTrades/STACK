#!/usr/bin/env python3
"""Find a product photo for each packaged item in the app's data, using the free
Open Food Facts / Open Beauty Facts / Open Products Facts databases.
Results are cached in data/images.json so each item is looked up once."""
import json, os, re, time, datetime, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "images.json")
UA = "StackDealsApp/1.0 (personal grocery app; https://github.com/TobiasTrades/stack)"
MAX_LOOKUPS = int(os.environ.get("MAX_LOOKUPS", "140"))
PAUSE = 6.5            # Open Food Facts asks for at most 10 searches a minute
RETRY_DAYS = 14        # look again for items that had no photo after this long
SKIP_CATS = {"produce", "meat", "deli", "bakery"}   # mostly unbranded: the app keeps its picture icons
STOP = set("the and or of with for a an in on fresh select varieties variety assorted family size pack pk ct count oz lb lbs fl gal each bag box original our great value kirkland signature member's members mark".split())
BEAUTY = re.compile(r"tooth|deodorant|antiperspirant|body wash|soap|shampoo|conditioner|lotion|razor|shave|mouthwash|floss|crest|colgate|oral-b|secret|old spice|degree|native|dove|olay|clairol|safeguard|ivory", re.I)
HOUSE = re.compile(r"detergent|softener|dryer|laundry|scent|beads|paper towel|toilet|bath tissue|tissue|napkin|trash|bag|foil|wrap|parchment|plates|cups|dish|cascade|cleaner|wipes|lysol|clorox|febreze|bleach|pods", re.I)

def key(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def query_for(name):
    q = re.split(r"\bor\b|,|\(|/| — | - ", name, flags=re.I)[0]
    q = re.sub(r"\d+(\.\d+)?\s*(oz|ct|lb|lbs|pk|count|fl|gal|l|ml|g)?\b\.?", " ", q, flags=re.I)
    words = [w for w in re.findall(r"[A-Za-z&'\-]+", q) if w.lower() not in STOP]
    return " ".join(words[:6])

def host_for(name, cat):
    if BEAUTY.search(name): return "world.openbeautyfacts.org"
    if cat == "household" or HOUSE.search(name): return "world.openproductsfacts.org"
    return "world.openfoodfacts.org"

def search(host, q):
    url = f"https://{host}/cgi/search.pl?" + urllib.parse.urlencode({"search_terms": q, "search_simple": 1, "action": "process", "json": 1, "page_size": 5, "fields": "product_name,brands,image_front_small_url,image_front_url"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("products", [])

def pick(products, q):
    qw = [w.lower() for w in q.split() if len(w) > 2]
    if not qw: return None
    best, best_score = None, 0
    for p in products:
        img = p.get("image_front_small_url") or p.get("image_front_url")
        if not img: continue
        text = (p.get("product_name", "") + " " + p.get("brands", "")).lower()
        score = sum(1 for w in qw if w in text)
        if qw[0] in text: score += 1           # the brand/first word matters most
        if score > best_score: best, best_score = img, score
    need = 2 if len(qw) >= 2 else 1
    return best if best_score >= need else None

def items():
    out = []
    for f in ["deals-current.json", "deals-extra.json", "deals-sams.json", "deals-prices.json"]:
        p = os.path.join(DATA, f)
        if not os.path.exists(p): continue
        for it in json.load(open(p)).get("items", []):
            if it.get("c") in SKIP_CATS: continue
            out.append((it.get("n", ""), it.get("c", "")))
    p = os.path.join(DATA, "coupons.json")
    if os.path.exists(p):
        for c in json.load(open(p)).get("items", []):
            out.append((f"{c.get('b','')} {c.get('n','')}", c.get("c", "")))
    return out

def main():
    cache = json.load(open(OUT)) if os.path.exists(OUT) else {}
    images, checked = cache.get("images", {}), cache.get("checked", {})
    today = datetime.date.today()
    looked = 0
    for name, cat in items():
        k = key(name)
        if not k or images.get(k): continue
        last = checked.get(k)
        if last and (today - datetime.date.fromisoformat(last)).days < RETRY_DAYS: continue
        if looked >= MAX_LOOKUPS: break
        q = query_for(name)
        if len(q) < 3:
            checked[k] = today.isoformat(); continue
        try:
            url = pick(search(host_for(name, cat), q), q)
        except Exception as e:
            print("lookup failed:", name, e); time.sleep(PAUSE); continue
        looked += 1
        checked[k] = today.isoformat()
        if url: images[k] = url
        print(("✓ " if url else "· ") + name + " → " + q)
        time.sleep(PAUSE)
    json.dump({"updated": today.isoformat(), "images": images, "checked": checked}, open(OUT, "w"), indent=0, sort_keys=True)
    print(f"looked up {looked}; {sum(1 for v in images.values() if v)} items have photos")

if __name__ == "__main__":
    main()
