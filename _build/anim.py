import asyncio, http.server, socketserver, threading, functools
from playwright.async_api import async_playwright
ROOT="/home/claude/clinipd"; PORT=8947
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    class Q(socketserver.TCPServer): allow_reuse_address=True
    s=Q(("127.0.0.1",PORT),h); s.RequestHandlerClass.log_message=lambda *a:None
    threading.Thread(target=s.serve_forever,daemon=True).start()

async def main():
    serve(); bad=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        ctx=await b.new_context(viewport={"width":1440,"height":950}); pg=await ctx.new_page()
        errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto(f"http://127.0.0.1:{PORT}/index.html",wait_until="domcontentloaded")

        # hero stagger: children should still be partly transparent right after load
        await pg.wait_for_timeout(260)
        early=await pg.evaluate("[...document.querySelectorAll('.hero-in > *')].map(e=>+getComputedStyle(e).opacity.slice(0,4))")
        await pg.wait_for_timeout(1400)
        late=await pg.evaluate("[...document.querySelectorAll('.hero-in > *')].map(e=>+getComputedStyle(e).opacity.slice(0,4))")
        print("hero opacity @260ms:", early)
        print("hero opacity @1.6s :", late)
        if not any(v<0.9 for v in early): bad.append("hero did not stagger (all opaque at 260ms)")
        if any(v<0.99 for v in late):     bad.append("hero did not finish arriving")

        # parallax: the transform must change as you scroll
        t0=await pg.evaluate("getComputedStyle(document.querySelector('.hero-panel img')).transform")
        await pg.evaluate("window.scrollTo(0,500)"); await pg.wait_for_timeout(350)
        t1=await pg.evaluate("getComputedStyle(document.querySelector('.hero-panel img')).transform")
        print("hero transform before:", t0[:52]); print("hero transform after :", t1[:52])
        if t0==t1: bad.append("hero photo does not drift on scroll")

        # progress bar
        p0=await pg.evaluate("getComputedStyle(document.querySelector('#prog')).transform")
        await pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await pg.wait_for_timeout(500)
        p1=await pg.evaluate("getComputedStyle(document.querySelector('#prog')).transform")
        op=await pg.evaluate("getComputedStyle(document.querySelector('#prog')).opacity")
        print("prog scale top:",p0,"| bottom:",p1,"| opacity",op)
        if p0==p1: bad.append("progress bar does not fill")
        if float(op)<0.9: bad.append("progress bar invisible at the bottom of the page")

        # bands still animate
        await pg.evaluate("window.scrollTo(0,1900)"); await pg.wait_for_timeout(450)
        bo=await pg.evaluate("[...document.querySelectorAll('.band-img img')].map(i=>+getComputedStyle(i).opacity.slice(0,4))")
        print("band image opacities mid-scroll:", bo)

        over=await pg.evaluate("document.documentElement.scrollWidth-window.innerWidth")
        if over>0: bad.append(f"horizontal overflow {over}px")
        if errs: bad.append(f"JS errors {errs[:2]}")

        # reduced motion: everything must land in its final state
        ctx2=await b.new_context(viewport={"width":1440,"height":950},reduced_motion="reduce")
        pg2=await ctx2.new_page()
        await pg2.goto(f"http://127.0.0.1:{PORT}/index.html",wait_until="domcontentloaded")
        await pg2.wait_for_timeout(700)
        r=await pg2.evaluate("[...document.querySelectorAll('.hero-in > *,[data-rev]')].map(e=>+getComputedStyle(e).opacity.slice(0,4))")
        print("reduced-motion opacities:", sorted(set(r)))
        if any(v<0.99 for v in r): bad.append("reduced motion leaves content hidden")
        await b.close()
    print("\nPROBLEMS:",len(bad))
    for x in bad: print("  -",x)
asyncio.run(main())
