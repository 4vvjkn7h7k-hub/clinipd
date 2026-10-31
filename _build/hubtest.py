import asyncio, os, http.server, socketserver, threading, functools
from playwright.async_api import async_playwright
ROOT="/home/claude/clinipd"; PORT=8942
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    class Q(socketserver.TCPServer): allow_reuse_address=True
    s=Q(("127.0.0.1",PORT),h); s.RequestHandlerClass.log_message=lambda *a:None
    threading.Thread(target=s.serve_forever,daemon=True).start()

async def main():
    serve(); bad=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        for vp,lab in [({"width":1440,"height":950},"desktop"),({"width":400,"height":860},"phone")]:
            ctx=await b.new_context(viewport=vp); pg=await ctx.new_page()
            errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
            await pg.goto(f"http://127.0.0.1:{PORT}/library.html",wait_until="domcontentloaded")
            await pg.wait_for_timeout(600)

            async def vis(sel): return await pg.evaluate(f"!document.querySelector('{sel}').hidden")
            # 1. default = hub
            if not await vis("#hub"): bad.append(f"[{lab}] hub not shown at load")
            cards=await pg.evaluate("document.querySelectorAll('.lib-card').length")
            if cards!=9: bad.append(f"[{lab}] expected 9 section cards, got {cards}")

            # 2. type a search -> results
            await pg.fill("#q","acl"); await pg.wait_for_timeout(300)
            if not await vis("#res"): bad.append(f"[{lab}] results not shown after typing")
            n=await pg.evaluate("document.querySelectorAll('#rlist .az-row').length")
            txt=await pg.inner_text("#rcount")
            marks=await pg.evaluate("document.querySelectorAll('#rlist mark').length")
            sects=await pg.evaluate("[...new Set([...document.querySelectorAll('#rlist .sec-tag')].map(e=>e.textContent))].join('/')")
            print(f"[{lab}] 'acl' -> {txt}, {n} rows, {marks} highlights, sections {sects}")
            if n<3: bad.append(f"[{lab}] too few results for 'acl'")   # 4 titles contain it
            if marks==0: bad.append(f"[{lab}] no search highlighting")

            # 3. every result href resolves
            hrefs=await pg.evaluate("[...document.querySelectorAll('#rlist a')].map(a=>a.getAttribute('href'))")
            miss=[h for h in hrefs if not os.path.exists(os.path.join(ROOT,h))]
            if miss: bad.append(f"[{lab}] broken result links: {miss[:3]}")

            # 4. scope with a pill
            await pg.click('#filters button[data-s="test"]'); await pg.wait_for_timeout(250)
            n2=await pg.evaluate("document.querySelectorAll('#rlist .az-row').length")
            only=await pg.evaluate("[...new Set([...document.querySelectorAll('#rlist .sec-tag')].map(e=>e.textContent))].join('/')")
            print(f"[{lab}] 'acl' in Special tests -> {n2} rows, sections {only}")
            if only not in ("TST",""): bad.append(f"[{lab}] pill did not scope results: {only}")

            # 5. clear the term -> that section's groups
            await pg.fill("#q",""); await pg.wait_for_timeout(300)
            if not await vis("#grp"): bad.append(f"[{lab}] group view not shown for an active pill")
            g=await pg.evaluate("document.querySelectorAll('#glist a').length")
            ghrefs=await pg.evaluate("[...document.querySelectorAll('#glist a')].map(a=>a.getAttribute('href'))")
            gmiss=[h for h in ghrefs if not os.path.exists(os.path.join(ROOT,h.split('?')[0]))]
            print(f"[{lab}] Special tests groups -> {g} rows")
            if g!=12: bad.append(f"[{lab}] expected 12 test groups, got {g}")
            if gmiss: bad.append(f"[{lab}] broken group links: {gmiss[:3]}")

            # 6. click the live pill again -> back to the hub
            await pg.click('#filters button[data-s="test"]'); await pg.wait_for_timeout(300)
            if not await vis("#hub"): bad.append(f"[{lab}] clicking the live pill did not return to the hub")

            # 7. deep link
            await pg.goto(f"http://127.0.0.1:{PORT}/library.html?q=berg",wait_until="domcontentloaded")
            await pg.wait_for_timeout(500)
            n3=await pg.evaluate("document.querySelectorAll('#rlist .az-row').length")
            print(f"[{lab}] ?q=berg -> {n3} rows")
            if n3<1: bad.append(f"[{lab}] ?q= deep link did not search")

            over=await pg.evaluate("document.documentElement.scrollWidth-window.innerWidth")
            if over>0: bad.append(f"[{lab}] horizontal overflow {over}px")
            if errs: bad.append(f"[{lab}] JS errors {errs[:2]}")
            await ctx.close()
        await b.close()
    print("\nPROBLEMS:",len(bad))
    for p in bad: print("  -",p)
asyncio.run(main())
