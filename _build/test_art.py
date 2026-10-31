import asyncio, http.server, socketserver, threading, functools, os, random, glob, re, io
from playwright.async_api import async_playwright
ROOT="/home/claude/clinipd"; PORT=9020
S="/home/claude/clinipd/_build/"
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
socketserver.TCPServer.allow_reuse_address=True
threading.Thread(target=socketserver.TCPServer(("127.0.0.1",PORT),h).serve_forever,daemon=True).start()

# 1. every p/ link from every root page must exist on disk
have={os.path.basename(f) for f in glob.glob(ROOT+"/p/*.html")}
missing=set()
for f in glob.glob(ROOT+"/*.html"):
    for m in re.findall(r'href="p/([a-z0-9-]+\.html)"', io.open(f,encoding='utf-8').read()):
        if m not in have: missing.add(m)
print("article pages on disk:", len(have))
print("broken p/ links from root pages:", len(missing), sorted(missing)[:5])

# 2. internal links inside article pages
missing2=set()
for f in glob.glob(ROOT+"/p/*.html"):
    src=io.open(f,encoding='utf-8').read()
    for m in re.findall(r'href="([a-z0-9-]+\.html)"', src):
        if m not in have: missing2.add((os.path.basename(f), m))
    for m in re.findall(r'href="\.\./([a-z0-9-]+\.html)"', src):
        if not os.path.exists(ROOT+"/"+m): missing2.add((os.path.basename(f), "../"+m))
print("broken links inside article pages:", len(missing2), sorted(missing2)[:5])

random.seed(4)
sample=random.sample(sorted(have), 14)
async def main():
    fails=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        for vp,lab in [({"width":1440,"height":950},"desktop"),({"width":390,"height":820},"phone")]:
            ctx=await b.new_context(viewport=vp)
            for f in sample:
                pg=await ctx.new_page()
                await ctx.route("**://fonts.g*/**", lambda r: asyncio.ensure_future(r.abort())); errs=[]
                pg.on("pageerror", lambda e: errs.append(str(e)))
                await pg.goto(f"http://127.0.0.1:{PORT}/p/{f}",wait_until="domcontentloaded")
                await pg.wait_for_timeout(500)
                r=await pg.evaluate("""() => ({
                  ov: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                  nav: document.querySelectorAll('#site-top .nav-a').length,
                  foot: document.querySelectorAll('#site-foot a').length,
                  h1: (document.querySelector('h1')||{}).textContent||'',
                  secs: document.querySelectorAll('.sec-a').length,
                  toc: document.querySelectorAll('.toc a').length,
                  brandHref: (document.querySelector('.brand')||{}).getAttribute ? document.querySelector('.brand').getAttribute('href') : ''
                })""")
                ok = r['ov']<=0 and r['nav']>=4 and r['foot']>=10 and r['h1'] and not errs
                if not ok: fails.append((lab,f,r,errs[:1]))
                await pg.close()
            await ctx.close()
        # brand link from an article must reach the home page
        ctx=await b.new_context(viewport={"width":1440,"height":950}); pg=await ctx.new_page()
        await ctx.route("**://fonts.g*/**", lambda r: asyncio.ensure_future(r.abort()))
        await pg.goto(f"http://127.0.0.1:{PORT}/p/{sample[0]}",wait_until="domcontentloaded")
        await pg.wait_for_timeout(600)
        await pg.click('.brand'); await pg.wait_for_timeout(900)
        print("brand click from article ->", pg.url.replace(f"http://127.0.0.1:{PORT}",""))
        if not pg.url.endswith("/index.html") and not pg.url.endswith("/"): fails.append(("nav","brand",pg.url,[]))
        await pg.goto(f"http://127.0.0.1:{PORT}/conditions.html",wait_until="domcontentloaded")
        await pg.wait_for_timeout(700)
        await pg.screenshot(path=S+"az.png")
        await pg.locator('.az-row').first.click(); await pg.wait_for_timeout(1000)
        print("first A-Z row click ->", pg.url.replace(f"http://127.0.0.1:{PORT}",""))
        if "/p/" not in pg.url: fails.append(("nav","az-row",pg.url,[]))
        await pg.screenshot(path=S+"art.png")
        await ctx.close(); await b.close()
    print("\nsampled", len(sample), "pages x2 viewports | FAILURES:", len(fails))
    for x in fails[:6]: print("   ", x)
asyncio.run(main())
