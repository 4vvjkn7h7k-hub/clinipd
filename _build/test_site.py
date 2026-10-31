import asyncio, os, re, sys, http.server, socketserver, threading, functools
from playwright.async_api import async_playwright

ROOT = "/home/claude/clinipd"
PORT = 8948
PAGES = ['anki.html', 'app.html', 'cardio.html', 'cases.html', 'clinics.html', 'collections.html', 'conditions.html', 'cpd.html', 'domains.html', 'evidence.html', 'exercises.html', 'foundations.html', 'geri.html', 'glossary.html', 'index.html', 'library.html', 'login.html', 'measures.html', 'msk.html', 'neuro.html', 'osce.html', 'paeds.html', 'pain.html', 'pelvic.html', 'placement.html', 'pricing.html', 'progress.html', 'qbank.html', 'questions.html', 'research.html', 'sports.html', 'studyplan.html', 'tests.html', 'universities.html', 'upload.html', 'videos.html']

def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), h)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

async def main():
    serve()
    problems = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for vp, label in [({"width":1440,"height":900},"desktop"), ({"width":400,"height":820},"phone")]:
            ctx = await b.new_context(viewport=vp)
            await ctx.route("**://fonts.googleapis.com/**", lambda r: asyncio.ensure_future(r.abort()))
            await ctx.route("**://fonts.gstatic.com/**", lambda r: asyncio.ensure_future(r.abort()))
            for page_name in PAGES:
                pg = await ctx.new_page()
                await pg.route('**fonts.g*', lambda r: asyncio.ensure_future(r.abort()))
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: errs.append("console:"+m.text) if (m.type=="error" and "fonts.g" not in m.text and "ERR_" not in m.text) else None)
                await pg.goto(f"http://127.0.0.1:{PORT}/{page_name}", wait_until="domcontentloaded")
                await pg.wait_for_timeout(500)
                # scroll through to fire reveals
                await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await pg.wait_for_timeout(600)
                over = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if over > 0:
                    problems.append(f"[{label}] {page_name}: horizontal overflow {over}px")
                if errs:
                    problems.append(f"[{label}] {page_name}: JS errors {errs[:3]}")
                # nav built?
                navcount = await pg.evaluate("document.querySelectorAll('#site-top .nav-a').length")
                footcount = await pg.evaluate("document.querySelectorAll('#site-foot a').length")
                SELF_SHELL = {'app.html'}   # the workspace keeps its own .cp-bar
                if navcount < 4 and page_name not in SELF_SHELL:
                    problems.append(f"[{label}] {page_name}: nav not built ({navcount} items)")
                if footcount < 10 and page_name not in SELF_SHELL:
                    problems.append(f"[{label}] {page_name}: footer not built ({footcount} links)")
                await pg.close()
            await ctx.close()

        # link integrity on desktop
        ctx = await b.new_context(viewport={"width":1440,"height":900})
        await ctx.route("**://fonts.googleapis.com/**", lambda r: asyncio.ensure_future(r.abort()))
        await ctx.route("**://fonts.gstatic.com/**", lambda r: asyncio.ensure_future(r.abort()))
        pg = await ctx.new_page()
        await pg.route('**fonts.g*', lambda r: asyncio.ensure_future(r.abort()))
        all_targets = set()
        for page_name in PAGES:
            await pg.goto(f"http://127.0.0.1:{PORT}/{page_name}", wait_until="domcontentloaded")
            await pg.wait_for_timeout(300)
            hrefs = await pg.evaluate("Array.from(document.querySelectorAll('a[href]')).map(a=>a.getAttribute('href'))")
            for h in hrefs:
                if not h or h.startswith(("#","mailto:","http://","https://")): continue
                all_targets.add((page_name, h.split("#")[0]))
        for src, t in sorted(all_targets):
            if not t: continue
            if not os.path.exists(os.path.join(ROOT, t)):
                problems.append(f"BROKEN LINK: {src} -> {t}")
        await ctx.close()

        # screenshots of home
        ctx = await b.new_context(viewport={"width":1440,"height":900}, device_scale_factor=1)
        await ctx.route("**://fonts.googleapis.com/**", lambda r: asyncio.ensure_future(r.abort()))
        await ctx.route("**://fonts.gstatic.com/**", lambda r: asyncio.ensure_future(r.abort()))
        pg = await ctx.new_page()
        await pg.route('**fonts.g*', lambda r: asyncio.ensure_future(r.abort()))
        await pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="domcontentloaded")
        await pg.wait_for_timeout(1600)
        await pg.screenshot(path="/home/claude/clinipd/_build/home-0.png")
        await pg.evaluate("window.scrollTo(0, 980)")
        await pg.wait_for_timeout(1100)
        await pg.screenshot(path="/home/claude/clinipd/_build/home-1.png")
        await pg.evaluate("window.scrollTo(0, 2500)")
        await pg.wait_for_timeout(1100)
        await pg.screenshot(path="/home/claude/clinipd/_build/home-2.png")
        await ctx.close()
        await b.close()

    print("PROBLEMS:", len(problems))
    for p in problems: print("  -", p)

asyncio.run(main())
