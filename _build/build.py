# -*- coding: utf-8 -*-
"""產生整個網站的 HTML。用法：在 site 資料夾執行  python3 _build/build.py"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from content import *  # noqa

MANIFEST = json.load(open(os.path.join(ROOT, "assets/img/manifest.json"), encoding="utf-8"))
DIMS = {i["src"]: (i["w"], i["h"]) for v in MANIFEST.values() for i in v}
CAT = {k: (zh, en) for k, zh, en in CATEGORIES}
BY_SLUG = {p["slug"]: p for p in PROJECTS}
e = html.escape

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@500;600;700&family=Noto+Sans+TC:wght@400;500;600&display=swap" rel="stylesheet">'


def img(slug, name, alt, pre, cls="", eager=False):
    src = f"assets/img/{slug}/{name}.jpg"
    w, h = DIMS.get(f"{slug}/{name}.jpg", (1600, 1000))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{pre}{src}" width="{w}" height="{h}" alt="{e(alt)}" {load}{c}>'


def cover_name(p):
    return p.get("cover", "cover")


def head(title, desc, pre):
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#04060a">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{pre}assets/css/style.css">
</head>
<body>
<div class="glow" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
"""


ICON_MAIL = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>'
ICON_IN = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.75h4v11H3v-11Zm6.5 0h3.8v1.5h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1v5.46h-4v-4.84c0-1.16-.02-2.64-1.61-2.64-1.61 0-1.86 1.26-1.86 2.56v4.92h-4v-11Z"/></svg>'
RESUME_BTN = f'<a class="btn btn--solid btn--resume" href="{RESUME}" target="_blank" rel="noopener">Download Resume <span class="arr" aria-hidden="true">↓</span></a>'

ICO = {
 "strategy": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor"/>',
 "flow": '<rect x="3" y="3.5" width="6" height="5" rx="1.2"/><rect x="15" y="3.5" width="6" height="5" rx="1.2"/><rect x="9" y="15.5" width="6" height="5" rx="1.2"/><path d="M6 8.5v3.5h12V8.5M12 12v3.5"/>',
 "research": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5.5 5.5M8 10.5h5"/>',
 "product": '<rect x="2.5" y="4" width="14" height="10" rx="1.5"/><path d="M6.5 18h6M9.5 14v4"/><rect x="16" y="9" width="5.5" height="11" rx="1.2"/>',
 "interaction": '<path d="m5 4 12.5 6.2-5.3 1.4-2.2 5.2z"/><path d="M17 15.5v5M14.5 18h5"/>',
 "responsive": '<rect x="3" y="3" width="12.5" height="17" rx="1.6"/><rect x="12.5" y="9" width="8.5" height="12" rx="1.4"/><path d="M8 17h2.5"/>',
 "system": '<rect x="3.5" y="3.5" width="7" height="7" rx="1"/><rect x="13.5" y="3.5" width="7" height="7" rx="1"/><rect x="3.5" y="13.5" width="7" height="7" rx="1"/><rect x="13.5" y="13.5" width="7" height="7" rx="3.5"/>',
 "component": '<path d="m12 2.8 3.2 3.2L12 9.2 8.8 6zM12 14.8l3.2 3.2-3.2 3.2-3.2-3.2zM6 8.8 9.2 12 6 15.2 2.8 12zM18 8.8l3.2 3.2-3.2 3.2-3.2-3.2z"/>',
 "guide": '<path d="M5 4.5h10.5a3 3 0 0 1 3 3v12H8a3 3 0 0 1-3-3z"/><path d="M5 16.5a3 3 0 0 1 3-3h10.5M9 8.5h6"/>',
 "collab": '<circle cx="8.5" cy="8.5" r="3"/><circle cx="16.5" cy="9.5" r="2.5"/><path d="M3 19.5c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5M14.5 14.6c.6-.2 1.3-.3 2-.3 2.3 0 4 1.5 4.5 4.7"/>',
 "lead": '<path d="M6 21V3.5"/><path d="M6 4h11.5l-2.5 4 2.5 4H6"/>',
}
def icon(k):
    return f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICO[k]}</svg>'


def header(pre, current):
    def nl(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a class="nav-link" href="{pre}{href}"{cur}>{label}</a>'
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{pre}index.html" aria-label="Harvey Huang 首頁"><img src="{pre}assets/img/logo.png" width="1200" height="537" alt="Harvey Design"><span class="brand-hint" aria-hidden="true">← Back to Home</span></a>
    <button class="menu-btn" aria-label="選單" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="主要導覽">
      {nl('about.html', 'ABOUT', 'about')}
      {nl('projects.html', 'WORKS', 'projects')}
      <a class="nav-link" href="#contact">CONTACT</a>
      {RESUME_BTN}
    </nav>
  </div>
</header>
<main>
"""


def contact(pre):
    return f"""<section class="section contact" id="contact">
  <div class="wrap">
    <h2 class="blur-type" data-focus aria-label="Let's talk"><span class="ln" aria-hidden="true">Let’s</span><span class="ln" aria-hidden="true">Talk</span></h2>
    <div class="contact-info reveal">
      <p class="zh-lead">任何專案想法或合作機會，<br>歡迎與我聯絡。</p>
      <div class="contact-actions">
        <a class="btn btn--solid" href="{RESUME}" target="_blank" rel="noopener">Download Resume <span class="arr" aria-hidden="true">↓</span></a>
        <a class="icon-btn" href="mailto:{EMAIL}" aria-label="Email：{EMAIL}" title="{EMAIL}">{ICON_MAIL}<span>Email</span></a>
        <a class="icon-btn" href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn">{ICON_IN}<span>LinkedIn</span></a>
      </div>
    </div>
  </div>
</section>
"""


def footer(pre):
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <span class="label label--muted">© 2026 Harvey Huang. All Rights Reserved.</span>
  </div>
</footer>
<script src="{pre}assets/js/main.js" defer></script>
</body>
</html>
"""


def card(p, i, pre, eager=False):
    zh_cat, en_cat = CAT[p["cat"]]
    return f"""<a class="card reveal" href="{pre}projects/{p['slug']}.html" data-cat="{p['cat']}" data-scramble-trigger>
  <div class="card-media">
    <span class="card-num num">{i:02d}</span>
    {img(p['slug'], cover_name(p), p['zh'], pre, eager=eager)}
  </div>
  <div class="card-body">
    <h3 class="card-title" data-scramble>{e(p['title'])}</h3>
    <p class="card-zh">{e(p['zh'])}</p>
    <p class="card-tags">{e(' / '.join(p['tags'][:3]))}</p>
    <span class="card-arr" aria-hidden="true">→</span>
  </div>
</a>"""


def write(path, s):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)
    print("wrote", path)


# ---------------------------------------------------------------- home
def build_home():
    pre = ""
    feat = [BY_SLUG[s] for s in ORDER_FEATURED]
    cards = "\n".join(card(p, i + 1, pre) for i, p in enumerate(feat))
    s = head("Harvey Huang｜UX / UI Designer", "Harvey Huang 黃威霖，資深 UX / UI 設計師，7+ 年數位產品與體驗設計經驗。", pre)
    s += header(pre, "home")
    s += f"""<section class="hero">
  <a class="scroll-cue" href="#works" aria-label="往下捲動"><span class="label label--muted">Scroll</span><i></i></a>
  <div class="wrap">
    <h1 class="blur-type" data-focus aria-label="Harvey — Experience, Design, Visual">
      <span class="ln" aria-hidden="true">Harvey</span>
      <span class="ln" aria-hidden="true">Experience</span>
      <span class="ln" aria-hidden="true">Design</span>
      <span class="ln" aria-hidden="true">Visual</span>
    </h1>
  </div>
</section>

<section class="section" id="works">
  <div class="wrap">
    <div class="section-head">
      <h2 class="label">精選作品｜Featured Works</h2>
      <a class="link-arrow" href="projects.html">View all <span class="arr" aria-hidden="true">→</span></a>
    </div>
    <div class="works-grid">
{cards}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2 class="label">專業領域｜Expertise</h2></div>
    <ul class="index-list">
      <li class="reveal"><span class="num">(01)</span><h3>Product Design<small>產品設計</small></h3><p>UI / UX · App &amp; LINE Mini App · Dashboard · Design System</p></li>
      <li class="reveal"><span class="num">(02)</span><h3>Web Experience<small>網站體驗</small></h3><p>Brand Website · Campaign Site · RWD · Interaction</p></li>
      <li class="reveal"><span class="num">(03)</span><h3>Visual Design<small>視覺設計</small></h3><p>Key Visual · Visual Identity · Illustration</p></li>
      <li class="reveal"><span class="num">(04)</span><h3>AI × Design<small>AI 共創設計</small></h3><p>AI-assisted Workflow · Rapid Prototyping · Vibe Coding</p></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <h2 class="label" style="margin:0 0 28px">設計方法｜Approach</h2>
        <p class="zh-lead" style="margin:0">從問題出發，<br>創造兼具美感與價值的體驗設計。</p>
      </div>
      <div class="prose reveal">
        <p>從需求、體驗到視覺與互動，我在意每個決定背後的原因，也會從<strong>商業目標、使用者需求與技術條件</strong>出發，找到兼顧體驗與視覺表現的設計解法。</p>
        <ol class="process" aria-label="設計流程"><li><span class="st-num">01</span><span class="st-dot" aria-hidden="true"></span><b>理解</b><small>Understand</small></li><li><span class="st-num">02</span><span class="st-dot" aria-hidden="true"></span><b>定義</b><small>Define</small></li><li><span class="st-num">03</span><span class="st-dot" aria-hidden="true"></span><b>探索</b><small>Explore</small></li><li><span class="st-num">04</span><span class="st-dot" aria-hidden="true"></span><b>設計</b><small>Design</small></li><li><span class="st-num">05</span><span class="st-dot" aria-hidden="true"></span><b>驗證</b><small>Validate</small></li><li><span class="st-num">06</span><span class="st-dot" aria-hidden="true"></span><b>迭代</b><small>Iterate</small></li></ol>
      </div>
    </div>
    <div class="stats reveal">
      <div class="stat"><b data-scramble data-glyphs="0123456789">7+</b><span>年數位產品與體驗設計經驗</span></div>
      <div class="stat"><b data-scramble data-glyphs="0123456789">10+</b><span>企業與品牌客戶</span></div>
      <div class="stat"><b data-scramble data-glyphs="0123456789">10+</b><span>大型網站設計規劃</span></div>
      <div class="stat"><b data-scramble data-glyphs="0123456789">2</b><span>DSA 數位奇點獎項</span></div>
    </div>
  </div>
</section>
"""
    s += contact(pre) + footer(pre)
    write("index.html", s)


# ---------------------------------------------------------------- projects index
def build_projects():
    pre = ""
    cards = "\n".join(card(p, i + 1, pre, eager=i < 2) for i, p in enumerate(PROJECTS))
    filters = f'<button class="pill" data-filter="all" aria-pressed="true">全部 All ({len(PROJECTS)})</button>' + "".join(
        f'<button class="pill" data-filter="{k}" aria-pressed="false">{zh} {en}</button>' for k, zh, en in CATEGORIES)
    s = head("Works｜Harvey Huang", "Harvey Huang 的作品集：數位產品、互動體驗與品牌體驗設計。", pre)
    s += header(pre, "projects")
    s += f"""<section class="page-hero page-hero--cue page-hero--works page-hero--full">
  <a class="scroll-cue" href="#all-works" aria-label="往下捲動"><span class="label label--muted">Scroll</span><i></i></a>
  <div class="wrap">
    <h1 class="blur-type" data-focus aria-label="All Works"><span class="ln" aria-hidden="true">All</span><span class="ln" aria-hidden="true">Works</span></h1>
    <p class="works-intro">多年來參與汽車、零售百貨、精品與酒類、消費電子與時尚媒體等產業的數位產品及體驗設計。</p>
  </div>
</section>
<section class="section" id="all-works" style="padding-top:0">
  <div class="wrap">
    <div class="filters" role="group" aria-label="作品分類">{filters}</div>
    <div class="works-grid works-grid--2">
{cards}
    </div>
  </div>
</section>
"""
    s += contact(pre) + footer(pre)
    write("projects.html", s)


# ---------------------------------------------------------------- about
def build_about():
    pre = ""
    s = head("About｜Harvey Huang", "Harvey Huang 黃威霖，資深 UX / UI 設計師。工作經歷、專業能力與獲獎紀錄。", pre)
    s += header(pre, "about")
    skills = [
        ("使用者體驗｜UX Design", [("strategy", "使用者體驗策略", "從商業目標與使用者需求出發，釐清問題並制定具體且可執行的體驗策略。"),
                       ("flow", "User Flow & Information Architecture", "將複雜的資訊與操作流程重新組織，建立清晰且直覺的使用者旅程。"),
                       ("research", "User Research & Testing", "透過質化與量化洞察及使用者測試，驗證設計方向並持續改善產品體驗。")]),
        ("介面設計｜UI Design", [("product", "Digital Product Design", "設計網站、App 與數位產品的完整介面體驗，兼顧使用性、視覺表現與品牌特色。"),
                       ("interaction", "Visual & Interaction Design", "結合視覺系統、互動模式與動態體驗，創造具吸引力且易於理解的數位介面。"),
                       ("responsive", "Responsive Design", "規劃不同裝置與螢幕尺寸下的體驗，維持一致且流暢的使用感受。")]),
        ("設計系統｜Design System", [("system", "Design System", "建立與維護可擴充的 Design System，提升產品體驗的一致性與設計效率。"),
                           ("component", "Component Design", "設計可重複使用的 UI Components 與 Patterns，提升設計與開發效率。"),
                           ("guide", "Design Guidelines", "建立設計原則與規範，維持跨產品、跨平台的設計一致性。")]),
        ("團隊協作｜Collaboration", [("collab", "跨部門協作", "與 PM、RD、編輯及其他利害關係人合作，確保設計從概念順利落地。"),
                           ("lead", "Design Leadership", "擔任 UI Lead，負責設計方向、任務分配、設計品質把關與團隊協作。")]),
    ]
    skill_html = "".join(
        f'<div class="skill-col reveal"><h3 class="label">{g}</h3>' + "".join(
            f'<div class="skill"><span class="sk-ico">{icon(k)}</span><div><h4>{e(t)}</h4><p>{e(d)}</p></div></div>' for k, t, d in items) + "</div>"
        for g, items in skills)
    steps = [("理解", "Understand"), ("定義", "Define"), ("探索", "Explore"), ("設計", "Design"), ("驗證", "Validate"), ("迭代", "Iterate")]
    proc = "".join(f'<li><span class="st-num">{i + 1:02d}</span><span class="st-dot" aria-hidden="true"></span><b>{zh}</b><small>{en}</small></li>' for i, (zh, en) in enumerate(steps))
    inds = ["消費電子", "汽車", "精品與酒類", "零售與百貨", "消費品牌", "娛樂", "數位行銷 Campaign", "互動體驗"]
    s += f"""<section class="page-hero page-hero--cue page-hero--full">
  <a class="scroll-cue" href="#about-intro" aria-label="往下捲動"><span class="label label--muted">Scroll</span><i></i></a>
  <div class="wrap">
    <h1 class="blur-type" data-focus aria-label="Hi, I'm Harvey"><span class="ln" aria-hidden="true">Hi, I’m</span><span class="ln" aria-hidden="true">Harvey</span></h1>
  </div>
</section>

<section class="section" id="about-intro" style="padding-top:clamp(40px,5vw,72px)">
  <div class="wrap">
    <div class="intro">
      <aside class="intro-side">
        <figure class="portrait reveal">
          <img src="assets/img/portrait.jpg" width="896" height="1200" alt="Harvey Huang 黃威霖" loading="lazy">
          <figcaption><span>Harvey 黃威霖</span><span>Taipei, TW</span></figcaption>
        </figure>
        <dl class="intro-facts reveal" style="--d:.1s">
          <dt>現職</dt><dd>Ogilvy Taiwan<br>Senior Consultant, UX &amp; UI</dd>
          <dt>經歷</dt><dd>Ogilvy Taiwan<br>Condé Nast Taiwan</dd>
          <dt>專長</dt><dd>Product Design · Web Experience<br>Visual Design · AI × Design</dd>
        </dl>
      </aside>
      <div class="intro-main">
        <span class="label reveal">關於我｜About</span>
        <p class="intro-quote reveal" style="--d:.08s">在未知的世界裡，<br>一起探索設計的更多可能！</p>
        <div class="intro-body">
          <p class="intro-lead reveal" style="--d:.12s">我是 Harvey 黃威霖，擁有 7+ 年經驗的設計師，擅長將複雜需求轉化為清晰、直覺且具視覺吸引力的數位體驗。</p>
          <div class="intro-cols">
            <p class="reveal" style="--d:.16s">以 UI Design 與 Design System 為核心，並以 UX 思維支撐設計決策，作品橫跨數位產品、互動體驗與品牌 Campaign。</p>
            <p class="reveal" style="--d:.2s">與 PM、RD 及跨部門團隊緊密合作，從需求釐清、介面設計到產品落地，完整參與設計流程。</p>
          </div>
        </div>
      </div>
    </div>
    <div class="stats reveal">
      <div class="stat"><b data-scramble data-glyphs="0123456789">7+</b><span>年數位產品與體驗設計經驗</span></div>
      <div class="stat"><b data-scramble data-glyphs="0123456789">10+</b><span>企業與品牌客戶</span></div>
      <div class="stat"><b data-scramble data-glyphs="0123456789">10+</b><span>大型網站設計規劃</span></div>
      <div class="stat"><b data-scramble data-glyphs="0123456789">2</b><span>DSA 數位奇點獎項</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2 class="label">工作經歷｜Experience</h2></div>
    <ol class="timeline">
      <li class="tl-org reveal">
        <div><h3 class="org-logo"><img src="assets/img/logos/ogilvy-white.png" width="800" height="310" alt="奧美 Ogilvy" style="height:52px"></h3><div class="meta">2020 — 至今 · 台北，台灣</div></div>
        <div class="role-track">
          <div class="tl-role">
            <h4>Senior Consultant, UX &amp; UI Consulting</h4><span class="when">2024.08 — 至今</span>
            <p>負責數位產品與品牌體驗設計，從 UX Strategy、產品架構到 UI Design 與 Design System，協助企業將商業需求轉化為具體且可落地的數位體驗。同時擔任 UI Lead，參與設計團隊的專案規劃、設計方向、品質把關與跨部門協作。</p>
            <div class="focus">UX Strategy · Product Design · UI Design · Design System · Team Leadership</div>
          </div>
          <div class="tl-role">
            <h4>Consultant, UX &amp; UI Consulting</h4><span class="when">2023.01 — 2024.08</span>
            <p>參與企業數位產品與服務體驗規劃，將商業需求與使用者需求轉化為具體的 UX/UI 解決方案。與 PM、RD 及跨職能團隊合作，從前期需求釐清到設計執行與開發落地，完整參與產品設計流程。</p>
            <div class="focus">UX Design · UI Design · Prototyping · User Research · Cross-functional Collaboration</div>
          </div>
          <div class="tl-role">
            <h4>Experience, UI Designer</h4><span class="when">2020.11 — 2023.01</span>
            <p>負責網站、App、Campaign 與互動數位產品的 UI/UX 設計，參與從概念發想到實際落地的完整設計流程。服務台灣在地品牌及國際企業客戶，累積跨產業、多平台的數位產品與品牌體驗設計經驗。</p>
            <div class="focus">UI Design · Interaction Design · Digital Experience · Visual Design · Figma</div>
          </div>
        </div>
      </li>
      <li class="tl-org reveal">
        <div><h3 class="org-logo"><img src="assets/img/logos/conde-nast-white.png" width="1000" height="147" alt="Condé Nast Taiwan" style="height:26px"></h3><ul class="brand-row" aria-label="旗下品牌">
            <li><img src="assets/img/logos/vogue-white.png" width="800" height="205" alt="VOGUE Taiwan" loading="lazy" class="b-vogue"></li>
            <li><img src="assets/img/logos/gq-white.png" width="800" height="422" alt="GQ Taiwan" loading="lazy" class="b-gq"></li>
          </ul>
          <div class="meta">2019.02 — 2020.07 · 台北，台灣</div></div>
        <div>
          <div class="tl-role">
            <h4>Assistant Product Designer</h4><span class="when">2019.02 — 2020.07</span>
            <p>參與數位活動與品牌體驗設計，曾執行 4 場大型 Campaign Website 的 Key Visual 與網站體驗規劃。與時尚編輯及團隊合作，從品牌特色與活動概念出發，將視覺創意轉化為符合 RWD 規範且具吸引力的數位體驗。</p>
            <div class="focus">Campaign Website · Visual Design · RWD · Art Direction · Editorial Collaboration</div>
          </div>
        </div>
      </li>
    </ol>
  </div>
</section>

<section class="section section--follow">
  <div class="wrap">
    <div class="section-head"><h2 class="label">教育背景｜Education</h2></div>
    <ol class="timeline">
      <li class="tl-org reveal">
        <div><h3>元智大學</h3><div class="meta">桃園，台灣</div></div>
        <div>
          <div class="tl-role">
            <h4>資訊傳播學系 設計組</h4><span class="when">2014 — 2018</span>
          </div>
        </div>
      </li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2 class="label">專業能力｜Capabilities</h2></div>
    <div class="skills">{skill_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2 class="label">榮譽與獎項｜Awards</h2></div>
    <div class="awards">
      <article class="award reveal">
        <div class="award-top">
          <img class="award-logo" src="assets/img/logos/dsa-gold.png" width="480" height="407" alt="DSA 數位奇點獎" loading="lazy">
          <div class="award-badge medal-gold"><b>金獎</b><span>Gold</span></div>
        </div>
        <span class="label">DSA 數位奇點獎 · 2024.11</span>
        <h3 class="medal">最佳顧客旅程介面設計商務行銷獎</h3>
        <dl>
          <dt>Project</dt><dd>My Volkswagen App</dd>
          <dt>Client</dt><dd>Volkswagen Taiwan</dd>
          <dt>Role</dt><dd>UI Lead Design · UX Research</dd>
        </dl>
        <p class="award-desc">參與 Volkswagen 數位體驗專案，負責 UI Lead Design，並參與 UX Research，與 UX、PM、Martech 及開發團隊共同完成產品設計與落地。</p>
        <a class="link-arrow" href="https://www.youtube.com/watch?v=mvJdcn54BvY" target="_blank" rel="noopener">觀看作品影片 <span class="arr" aria-hidden="true">↗</span></a>
      </article>
      <article class="award reveal">
        <div class="award-top">
          <img class="award-logo" src="assets/img/logos/dsa-gold.png" width="480" height="407" alt="DSA 數位奇點獎" loading="lazy">
          <div class="award-badge medal-silver"><b>銀獎</b><span>Silver</span></div>
        </div>
        <span class="label">DSA 數位奇點獎 · 2022.11</span>
        <h3 class="medal">最佳顧客旅程及介面設計獎</h3>
        <dl>
          <dt>Project</dt><dd>全聯小時達｜不用等到最後的晚餐</dd>
          <dt>Client</dt><dd>全聯福利中心</dd>
          <dt>Role</dt><dd>User Flow · Wireframe · UI Design</dd>
        </dl>
        <p class="award-desc">參與全聯小時達數位體驗設計，負責 User Flow、Wireframe 與 UI Design，從使用者旅程與操作流程出發，規劃完整的數位體驗。</p>
        <a class="link-arrow" href="https://www.youtube.com/watch?v=vFGlAPMyJc0" target="_blank" rel="noopener">觀看作品影片 <span class="arr" aria-hidden="true">↗</span></a>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="facts">
      <div class="reveal">
        <h3 class="label">產業經驗｜Industries</h3>
        <ul class="pills pills--hover">{''.join(f'<li class="pill">{x}</li>' for x in inds)}</ul>
      </div>
      <div class="reveal">
        <h3 class="label">設計工具｜Tools</h3>
        <dl>
          <dt>Design</dt><dd>Figma · FigJam · Adobe Creative Suite</dd>
          <dt>Prototyping</dt><dd>Wireframe · High-fidelity · Interactive Prototype</dd>
          <dt>AI &amp; Emerging</dt><dd>Figma Make · AI-assisted Design · Vibe Coding</dd>
        </dl>
      </div>
    </div>
  </div>
</section>
"""
    s += contact(pre) + footer(pre)
    write("about.html", s)


# ---------------------------------------------------------------- project detail
def build_project(idx):
    p = PROJECTS[idx]
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    pre = "../"
    slug = p["slug"]
    zh_cat, en_cat = CAT[p["cat"]]
    tags = "".join(f'<li class="pill">{e(t)}</li>' for t in p["tags"])
    role = p.get("role")
    meta3 = (f'<div><h3 class="label label--muted">擔任角色｜Role</h3><p>{"<br>".join(e(r) for r in role) if isinstance(role, list) else e(role)}</p></div>' if role
             else f'<div><h3 class="label label--muted">作品分類｜Category</h3><p>{zh_cat} · {en_cat}</p></div>')
    award = f'<p class="p-award">{e(p["award"])}</p>' if p.get("award") else ""
    secs = "".join(f'<div class="p-sec reveal"><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in p["sections"])
    secs_html = f'<div class="p-sections">{secs}</div>' if secs else ""

    items = []
    for g in p["gallery"]:
        if isinstance(g, str):
            items.append(f'<figure class="reveal">{img(slug, g, p["zh"], pre)}</figure>')
        elif g[0] == "text":
            items.append(f'<div class="g-text reveal"><h3>{e(g[1])}</h3><p>{e(g[2])}</p></div>')
        elif g[0] == "join":
            items.append('<figure class="reveal g-join">' + "".join(img(slug, n, p["zh"], pre) for n in g[1:]) + '</figure>')
        elif g[0] == "loop":
            items.append(f'<figure class="reveal"><video src="{pre}assets/video/{g[1]}" autoplay muted loop playsinline preload="auto" aria-label="{e(p["zh"])} 介面操作影片"></video></figure>')
        elif g[0] == "video":
            items.append(f'<figure class="reveal"><video src="{pre}assets/video/{g[1]}" controls playsinline preload="metadata" poster="{pre}assets/img/{slug}/{cover_name(p)}.jpg"></video></figure>')
        elif g[0] == "youtube":
            items.append(f'<figure class="reveal"><div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/{g[1]}" title="{e(g[2])}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div><figcaption>{e(g[2])}</figcaption></figure>')
    layout = p.get("layout", "wide")
    gcls = {"wide": "gallery", "tall": "gallery gallery--tall", "grid3": "gallery gallery--grid3"}[layout]
    links = "".join(f'<a class="btn" href="{u}" target="_blank" rel="noopener">{e(t)} <span class="arr" aria-hidden="true">↗</span></a>' for t, u in p.get("links", []))
    links_html = f'<div class="p-links">{links}</div>' if links else ""

    if p.get("hero_video"):
        hv = p["hero_video"]; hv = hv if isinstance(hv, list) else [hv]
        hp = p.get("hero_poster", cover_name(p)); hp = hp if isinstance(hp, list) else [hp] * len(hv)
        hero_media = "".join(f'<video class="p-hero-video" src="{pre}assets/video/{v}" autoplay muted loop playsinline controls preload="auto" poster="{pre}assets/img/{slug}/{hp[i]}.jpg" aria-label="{e(p["zh"])} 影片"></video>' for i, v in enumerate(hv))
    else:
        hero_media = img(slug, cover_name(p), p['zh'], pre, eager=True)
    s = head(f"{p['title']}｜Harvey Huang", p["lead"][:110], pre)
    s += header(pre, "projects")
    s += f"""<article>
<section class="p-hero">
  <div class="wrap">
    <a class="link-arrow p-back" href="{pre}projects.html"><span aria-hidden="true">←</span> All works</a>
    <div class="p-kicker"><span class="num">{idx + 1:02d} / {len(PROJECTS):02d}</span><span class="rule"></span><span class="label">{zh_cat}｜{en_cat}</span></div>
    <h1 class="p-title">{e(p['title'])}</h1>
    <p class="p-zh">{e(p['zh'])}</p>
    {award}
    <div class="p-meta">
      <div><h3 class="label label--muted">客戶｜Client</h3><p>{e(p['client'])}</p></div>
      {meta3}
      <div><h3 class="label label--muted">專案範疇｜Scope</h3><ul class="pills">{tags}</ul></div>
    </div>
  </div>
</section>
<div class="wrap p-cover">{hero_media}</div>
<section class="section">
  <div class="wrap">
    <div class="p-intro reveal">
      <span class="label">專案概述｜Overview</span>
      <p class="zh-lead">{e(p['lead'])}</p>
    </div>
    {secs_html}
    {links_html}
  </div>
</section>
<section class="section" style="padding-top:0;border-top:0">
  <div class="wrap">
    <div class="{gcls}">
      {''.join(items)}
    </div>
  </div>
</section>
<a class="next wrap" href="{pre}projects/{nxt['slug']}.html" style="display:block">
  <span class="label">下一個作品｜Next Project →</span>
  <span class="blur-type"><span class="ln">{e(nxt['title'])}</span></span>
  <p class="next-zh">{e(nxt['zh'])}</p>
</a>
</article>
"""
    s += contact(pre) + footer(pre)
    write(f"projects/{slug}.html", s)


if __name__ == "__main__":
    build_home()
    build_projects()
    build_about()
    for i in range(len(PROJECTS)):
        build_project(i)
