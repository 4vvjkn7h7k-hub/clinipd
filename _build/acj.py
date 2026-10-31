import asyncio, http.server, socketserver, threading, functools
from playwright.async_api import async_playwright
ROOT="/home/claude/clinipd"; PORT=8971
PID="msk-shoulder-acromioclavicular-joint-injury"
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
            ctx=await b.new_context(viewport=vp)
            await ctx.route("**://fonts.g*/**", lambda r: asyncio.ensure_future(r.abort()))
            pg=await ctx.new_page()
            errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(f"http://127.0.0.1:{PORT}/p/{PID}.html", wait_until="domcontentloaded")
            await pg.wait_for_timeout(1200)

            live   = await pg.evaluate("document.querySelectorAll('.fld-live').length")
            left   = await pg.evaluate("document.querySelectorAll('.flds').length")
            tables = await pg.evaluate("document.querySelectorAll('.fld-live table.tpl').length")
            refs   = await pg.evaluate("document.querySelectorAll('.reflist li').length")
            dois   = await pg.evaluate("document.querySelectorAll('.reflist a[href^=\"https://doi.org/\"]').length")
            sups   = await pg.evaluate("document.querySelectorAll('.fld-live sup a[href^=\"#ref\"]').length")
            verify = await pg.evaluate("document.querySelectorAll('mark.verify').length")
            gloss  = await pg.evaluate("document.querySelectorAll('.fld-live .gl').length")
            chips  = await pg.evaluate("[...document.querySelectorAll('.chips .chip')].map(c=>c.textContent).join(' | ')")
            over   = await pg.evaluate("document.documentElement.scrollWidth-window.innerWidth")

            print(f"[{lab}] sections filled {live}/16 · placeholders left {left} · tables {tables}")
            print(f"[{lab}] refs {refs} ({dois} with DOI) · citation links {sups} · verify marks {verify} · glossary {gloss}")
            print(f"[{lab}] chips: {chips}")

            if live!=16: bad.append(f"[{lab}] only {live}/16 sections filled")
            if left:     bad.append(f"[{lab}] {left} placeholder blocks left behind")
            if refs!=10: bad.append(f"[{lab}] {refs} refs rendered, expected 10")
            if dois!=10: bad.append(f"[{lab}] {dois} DOI links, expected 10")
            if sups<20:  bad.append(f"[{lab}] only {sups} citation superscripts linked")
            if verify!=2:bad.append(f"[{lab}] {verify} verify marks, expected 2")
            if over>0:   bad.append(f"[{lab}] horizontal overflow {over}px")
            if errs:     bad.append(f"[{lab}] JS errors {errs[:2]}")

            # a citation link must actually land on its reference
            await pg.evaluate("document.querySelector('.fld-live sup a[href^=\"#ref\"]').click()")
            await pg.wait_for_timeout(500)
            tgt=await pg.evaluate("(document.querySelector('.reflist li:target')||{}).id || 'none'")
            if tgt=="none": bad.append(f"[{lab}] citation link did not jump to its reference")
            else: print(f"[{lab}] clicking a superscript lands on #{tgt}")

            if lab=="desktop":
                await pg.evaluate("window.scrollTo(0,1500)"); await pg.wait_for_timeout(500)
                await pg.screenshot(path="acj-body.png")
                await pg.evaluate("document.querySelector('.reflist').scrollIntoView()"); await pg.wait_for_timeout(500)
                await pg.screenshot(path="acj-refs.png")
            else:
                await pg.screenshot(path="acj-phone.png")
            await ctx.close()

        # a page with NO json must stay an honest skeleton
        ctx=await b.new_context(viewport={"width":1440,"height":950})
        await ctx.route("**://fonts.g*/**", lambda r: asyncio.ensure_future(r.abort()))
        pg=await ctx.new_page()
        e2=[]; pg.on("pageerror", lambda e: e2.append(str(e)))
        await pg.goto(f"http://127.0.0.1:{PORT}/p/msk-knee-knee-osteoarthritis.html", wait_until="domcontentloaded")
        await pg.wait_for_timeout(900)
        skel=await pg.evaluate("document.querySelectorAll('.flds').length")
        chip=await pg.evaluate("[...document.querySelectorAll('.chips .chip')].map(c=>c.textContent).join(' | ')")
        print(f"\n[unwritten page] placeholder blocks {skel} · chips: {chip}")
        if skel<10: bad.append("an unwritten page lost its placeholders")
        if e2: bad.append(f"[unwritten] JS errors {e2[:2]}")
        await b.close()
    print("\nPROBLEMS:",len(bad))
    for x in bad: print("  -",x)
asyncio.run(main())
