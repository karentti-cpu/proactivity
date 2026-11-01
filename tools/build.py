#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assembles index.html from the modules in this directory.

The app ships as one self-contained index.html; this script exists so the
five-language translation table stays editable and verifiable. Run:

    python3 tools/build.py

Edit the i18n_*.py tables (or the CSS/HTML/JS modules) and re-run.
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from i18n_ui import UI
from i18n_app import APP
from i18n_content import CONTENT
from i18n_plan import PLAN
from i18n_mini import MINI
from i18n_food import FOOD
from i18n_quiz import QUIZ
from i18n_home import HOME
from i18n_qbands import QBANDS
from i18n_chain import CHAIN
from i18n_suggest import SUGGEST
from i18n_ready import READY
from i18n_pro import PRO
from i18n_avatar import AVATAR
from assets import sprite
from css import CSS
from html import build_body, FAQ_SHOWN
from js_core import JS_CORE
from js_quiz import JS_QUIZ
from js_app import JS_APP
from js_chain import JS_CHAIN
from js_render import JS_RENDER
from js_mini import JS_MINI
from js_pro import JS_PRO
from js_data import JS_DATA
from js_avatar import JS_AVATAR
from js_self import JS_SELF

LANGS = ['he', 'en', 'fr', 'ru', 'ar']
OUT = os.path.join(ROOT, 'index.html')


def merged_table():
    table = {}
    for src, name in ((UI, 'i18n_ui'), (APP, 'i18n_app'),
                      (CONTENT, 'i18n_content'), (PLAN, 'i18n_plan'),
                      (MINI, 'i18n_mini'), (FOOD, 'i18n_food'),
                      (QUIZ, 'i18n_quiz'), (HOME, 'i18n_home'),
                      (QBANDS, 'i18n_qbands'), (CHAIN, 'i18n_chain'), (SUGGEST, 'i18n_suggest'), (READY, 'i18n_ready'),
                      (PRO, 'i18n_pro'), (AVATAR, 'i18n_avatar')):
        for k, v in src.items():
            if k in table:
                raise SystemExit(f'duplicate translation key {k!r} (in {name})')
            if len(v) != len(LANGS):
                raise SystemExit(f'key {k!r} has {len(v)} values, expected {len(LANGS)}')
            for j, s in enumerate(v):
                if not str(s).strip():
                    raise SystemExit(f'key {k!r} is empty for language {LANGS[j]!r}')
            table[k] = v
    return table


def i18n_js(table):
    per_lang = {L: {k: v[j] for k, v in table.items()} for j, L in enumerate(LANGS)}
    return 'var I18N=' + json.dumps(per_lang, ensure_ascii=False, separators=(',', ':')) + ';'


# {masculine|feminine}, resolved at runtime by gres() in js_core.py. The
# character classes forbid nesting: a branch may not contain a brace, so a
# {placeholder} can never hide inside one and the two syntaxes cannot overlap.
GENDER_SEG = re.compile(r'\{([^{}|]*)\|([^{}|]*)\}')
PLACEHOLDER = re.compile(r'\{[A-Za-z][A-Za-z0-9_]*\}')


def check_placeholders(table):
    """Every {var} in the Hebrew source must exist in the other four.

    Gender segments are stripped first: {a|b} is not a placeholder, and a
    language is free to need gender agreement where Hebrew does not (or the
    other way round), so they are checked separately by check_gender().
    """
    bad = []
    for k, v in table.items():
        want = set(re.findall(r'\{(\w+)\}', GENDER_SEG.sub('', v[0])))
        for j in range(1, len(LANGS)):
            got = set(re.findall(r'\{(\w+)\}', GENDER_SEG.sub('', v[j])))
            if got != want:
                bad.append(f'{k} [{LANGS[j]}]: expected {sorted(want)}, got {sorted(got)}')
    if bad:
        raise SystemExit('placeholder mismatch:\n  ' + '\n  '.join(bad))


def check_gender(table):
    """A gender segment must be well formed, or it renders as literal braces.

    A bare "|" in prose is legitimate (a title separator, say), so the check is
    not "does this string contain a pipe". It is: after removing every valid
    {placeholder} and every valid {m|f} segment, no brace may remain. That
    catches the shapes that actually break - {מתחילה} with the pipe forgotten,
    an unclosed {a|b, and a nested {a|{n}|c} - because each leaves a stray
    brace behind. t() fails open and prints the key, and esc() does not escape
    braces, so a malformed segment reaches the screen silently; this validator
    is the only thing standing between an author typo and a user seeing it.
    """
    bad = []
    for k, v in table.items():
        for j, s in enumerate(v):
            rest = GENDER_SEG.sub('', s)
            rest = PLACEHOLDER.sub('', rest)
            if '{' in rest or '}' in rest:
                bad.append(f'{k} [{LANGS[j]}]: stray brace - malformed gender segment '
                           f'or placeholder in {s!r}')
            for m, f in GENDER_SEG.findall(s):
                if m == f:
                    bad.append(f'{k} [{LANGS[j]}]: {{{m}|{f}}} has identical forms, drop the markup')
                if not m and not f:
                    bad.append(f'{k} [{LANGS[j]}]: {{|}} is empty on both sides')
    if bad:
        raise SystemExit('gender markup:\n  ' + '\n  '.join(bad))


QUIZ_BANDS = ('a13', 'a18', 'a30', 'a50')
QUIZ_N = 12
QUIZ_PARTS = ('q', 'a', 'b', 'c', 'd')


def check_quiz_bands(table):
    """Every band spells out all ten questions and all five parts, and nothing
    that looks like a question key can be a typo the runtime never reads.

    What this cannot check - and the reason the warning at the top of
    i18n_qbands.py exists - is that option a in band a30 means the same thing
    as option a in band a13. Scoring is by position; a band whose options
    were reordered to read better scores its users backwards, silently.
    """
    bad = []
    pat = re.compile(r'^qz\.(a\d+)\.(\d+)\.([a-z])$')
    seen = {b: set() for b in QUIZ_BANDS}
    for k in table:
        m = pat.match(k)
        if not m:
            continue
        band, n, part = m.group(1), int(m.group(2)), m.group(3)
        if band not in QUIZ_BANDS or not (1 <= n <= QUIZ_N) or part not in QUIZ_PARTS:
            bad.append(f'{k}: not a valid band/question/part - the runtime will never read it')
            continue
        seen[band].add((n, part))
    for band in QUIZ_BANDS:
        for n in range(1, QUIZ_N + 1):
            for part in QUIZ_PARTS:
                if (n, part) not in seen[band]:
                    bad.append(f'qz.{band}.{n}.{part} is missing')
    if bad:
        raise SystemExit('check-in bands:\n  ' + '\n  '.join(bad))


def gender_report(table):
    """Hebrew and Arabic have no genderless second person, so a Hebrew string
    that needed a segment almost always means Arabic needs one too. Not fatal -
    plenty of strings are impersonal - but worth seeing at every build."""
    he_seg = {k for k, v in table.items() if GENDER_SEG.search(v[0])}
    missing_ar = sorted(k for k in he_seg if not GENDER_SEG.search(table[k][4]))
    counts = {L: sum(1 for v in table.values() if GENDER_SEG.search(v[j]))
              for j, L in enumerate(LANGS)}
    return counts, missing_ar


SITE = 'https://karentti-cpu.github.io/proactivity/'

# Static <head> metadata. The page is a single document with a JS language
# switcher, so the markup carries the Hebrew default and applyLang() rewrites
# the title and description once a language is chosen.
SEO_TITLE = 'Proacty — להפסיק לדחות ולהתחיל לעשות'
SEO_DESC = ('מה זה פרואקטיביות ואיך נהיים פרואקטיביים? שאלון קצר שמראה איפה הדברים '
            'עומדים ביוזמה, במטרות, בניהול זמן ובתכנון — ואז יעד שנבנה ממה שאמרת, '
            'צעדים קטנים והרגלים שנבנים. בלי הרשמה.')


def structured_data(table):
    """WebApplication + FAQPage, built from the same strings the page shows so
    the markup can never drift from the visible content."""
    faq = [{'@type': 'Question',
            'name': table[f'l.faq.q{n}'][0],
            'acceptedAnswer': {'@type': 'Answer', 'text': table[f'l.faq.a{n}'][0]}}
           for n in FAQ_SHOWN]
    blocks = [
        {'@context': 'https://schema.org', '@type': 'WebApplication',
         'name': 'Proacty', 'url': SITE,
         'applicationCategory': 'LifestyleApplication',
         'operatingSystem': 'Any', 'inLanguage': ['he', 'en', 'fr', 'ru', 'ar'],
         'description': SEO_DESC,
         'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'ILS'}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq},
    ]
    return ''.join(
        '<script type="application/ld+json">'
        + json.dumps(b, ensure_ascii=False, separators=(',', ':')) + '</script>'
        for b in blocks)


def head_meta(table):
    tags = [
        '<meta name="description" content="' + SEO_DESC + '">',
        '<meta name="robots" content="index,follow,max-image-preview:large">',
        '<meta name="author" content="Proacty">',
        f'<link rel="canonical" href="{SITE}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Proacty">',
        f'<meta property="og:url" content="{SITE}">',
        f'<meta property="og:title" content="{SEO_TITLE}">',
        f'<meta property="og:description" content="{SEO_DESC}">',
        f'<meta property="og:image" content="{SITE}og.png">',
        '<meta property="og:locale" content="he_IL">',
        ''.join(f'<meta property="og:locale:alternate" content="{L}">'
                for L in ('en_US', 'fr_FR', 'ru_RU', 'ar_001')),
        '<meta name="twitter:card" content="summary">',
        f'<meta name="twitter:title" content="{SEO_TITLE}">',
        f'<meta name="twitter:description" content="{SEO_DESC}">',
        f'<meta name="twitter:image" content="{SITE}og.png">',
        '<meta name="apple-mobile-web-app-capable" content="yes">',
        '<meta name="apple-mobile-web-app-title" content="Proacty">',
    ]
    return '\n'.join(tags) + '\n' + structured_data(table)


# ---------------------------------------------------------------- PWA
# Pages serves this app from a sub-path, so the manifest scope and the worker
# scope are both relative. An absolute "/" would silently disable the install
# prompt and register a worker that controls nothing.
MANIFEST = {
    'name': 'Proacty',
    'short_name': 'Proacty',
    'id': './',
    'start_url': './',
    'scope': './',
    'display': 'standalone',
    'orientation': 'portrait',
    'background_color': '#FBF8F1',
    'theme_color': '#FBF9F5',
    'dir': 'rtl',
    'lang': 'he',
    # Android lists the installed app in the phone's Share menu; a shared
    # link opens the app with ?url=/?text=, and it asks which goal to keep it in
    'share_target': {'action': './', 'method': 'GET',
                     'params': {'title': 'title', 'text': 'text', 'url': 'url'}},
    'icons': [
        {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
        {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
        {'src': 'icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ],
}

# The shell is cached so the app opens with no signal, but index.html is fetched
# network-first: a cache-first HTML is how a PWA pins itself to a stale build
# forever, and there is no second chance to fix that once it ships.
SW = """/* generated by tools/build.py - do not edit */
var CACHE='proactivity-%(ver)s';
var SHELL=['./','./index.html','./icon-192.png','./icon-512.png','./manifest.webmanifest'];
self.addEventListener('install', function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(SHELL).catch(function(){}); }));
});
self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(ks){
    return Promise.all(ks.map(function(k){ return k===CACHE ? null : caches.delete(k); }));
  }).then(function(){ return self.clients.claim(); }));
});
self.addEventListener('fetch', function(e){
  var req=e.request;
  if(req.method!=='GET') return;
  var url=new URL(req.url);
  if(url.origin!==location.origin) return;        /* fonts and the licence API go straight out */
  var isDoc = req.mode==='navigate' || (req.headers.get('accept')||'').indexOf('text/html')>=0;
  if(isDoc){
    e.respondWith(fetch(req).then(function(r){
      /* only a real page is kept: a 404 or an error must never replace the app */
      if(!r || !r.ok) return caches.match('./index.html').then(function(hit){ return hit || r; });
      var copy=r.clone();
      caches.open(CACHE).then(function(c){ c.put('./index.html', copy); });
      return r;
    }).catch(function(){ return caches.match('./index.html'); }));
    return;
  }
  e.respondWith(caches.match(req).then(function(hit){
    return hit || fetch(req).then(function(r){
      if(r && r.status===200){ var copy=r.clone(); caches.open(CACHE).then(function(c){ c.put(req,copy); }); }
      return r;
    });
  }));
});
"""


def write_pwa(html):
    """Manifest + service worker, versioned by the build itself."""
    ver = hashlib.sha1(html.encode('utf-8')).hexdigest()[:12]
    with open(os.path.join(ROOT, 'manifest.webmanifest'), 'w', encoding='utf-8') as f:
        json.dump(MANIFEST, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(os.path.join(ROOT, 'sw.js'), 'w', encoding='utf-8') as f:
        f.write(SW % {'ver': ver})
    missing = [n for n in ('icon-192.png', 'icon-512.png', 'icon-maskable-512.png',
                           'apple-touch-icon.png')
               if not os.path.exists(os.path.join(ROOT, n))]
    if missing:
        raise SystemExit('missing icon(s): ' + ', '.join(missing))
    return ver


def main():
    table = merged_table()
    check_placeholders(table)
    check_gender(table)
    check_quiz_bands(table)


    fonts = ('https://fonts.googleapis.com/css2'
             '?family=Heebo:wght@400;500;600;700;900'
             '&family=Secular+One'
             '&family=Inter:wght@400;600;700;800'
             '&family=Noto+Sans+Arabic:wght@400;600;700'
             '&display=swap')

    # Sets dir/lang and the theme before first paint: no RTL/LTR flash and no
    # flash of the wrong palette.
    early = ("(function(){try{var l=localStorage.getItem('proactive_lang');"
             "if(!l){var n=(navigator.language||'he').slice(0,2);"
             "l=['he','en','fr','ru','ar'].indexOf(n)>=0?n:'he';}"
             "var d=document.documentElement;d.lang=l;"
             "d.dir=(l==='he'||l==='ar')?'rtl':'ltr';"
             "var st=localStorage.getItem('proactive_theme');"
             "var th=(st==='dark'||st==='light')?st:'light';"
             "d.setAttribute('data-theme',th);"
             "var sa=localStorage.getItem('proactive_accent');"
             "d.setAttribute('data-accent',['sage','flame','bloom','mint'].indexOf(sa)>=0?sa:'sage');"
             "}catch(e){}})();")

    js = '\n'.join([i18n_js(table), JS_CORE, JS_QUIZ, JS_APP, JS_PRO, JS_DATA,
                    JS_AVATAR, JS_CHAIN, JS_MINI, JS_SELF, JS_RENDER])

    html = (
        '<!DOCTYPE html>\n'
        '<html lang="he" dir="rtl">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#FBF9F5">\n'
        '<meta name="color-scheme" content="dark light">\n'
        f'<title>{SEO_TITLE}</title>\n'
        + head_meta(table) + '\n'
        f'<script>{early}</script>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        # Preloaded so the fetch starts at once, but still render-blocking on
        # purpose: applying it after first paint restyled the whole page and
        # cost 0.19 of layout shift - a visible jump under the reader - to buy
        # 0.7s of paint. A page that does not move is worth more than a page
        # that appears sooner and then lurches.
        f'<link rel="preload" as="style" href="{fonts}">\n'
        f'<link rel="stylesheet" href="{fonts}">\n'
        '<link rel="icon" href="icon-192.png">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="Proacty">\n'
        f'<style>{CSS}</style>\n'
        '</head>\n<body>\n'
        + sprite() + '\n'
        + build_body('icon-192.png') + '\n'
        + '<script>' + js + '</script>\n'
        '</body>\n</html>\n'
    )

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    write_pwa(html)

    print(f'wrote {OUT}')
    gcounts, missing_ar = gender_report(table)
    print(f'  {len(table)} translation keys x {len(LANGS)} languages')
    print('  gendered strings: ' + ', '.join(f'{L}={gcounts[L]}' for L in LANGS))
    if missing_ar:
        print(f'  note: {len(missing_ar)} keys inflect in he but not yet in ar')
    print(f'  {len(html):,} bytes')


if __name__ == '__main__':
    main()
