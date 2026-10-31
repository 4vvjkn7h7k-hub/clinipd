import asyncio, http.server, socketserver, threading, functools
from playwright.async_api import async_playwright
ROOT="/home/claude/clinipd"; PORT=9110
S="/home/claude/clinipd/_build/"
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
socketserver.TCPServer.allow_reuse_address=True
threading.Thread(target=socketserver.TCPServer(("127.0.0.1",PORT),h).serve_forever,daemon=True).start()
IDS=["","slate","warm","contrast","indigo","forest","plum","crimson","ocean","graphite"]
RATIO="""(a,b)=>{const L=c=>{const m=c.match(/[\\d.]+/g).map(Number).slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);});return .2126*m[0]+.7152*m[1]+.0722*m[2];};const l1=L(a),l2=L(b);return (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);}"""
async def main():
    fails=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        for mode in ["light","dark"]:
            for sc in IDS:
                ctx=await b.new_context(viewport={"width":1280,"height":900}); pg=await ctx.new_page()
                await ctx.route("**://fonts.g*/**", lambda r: __import__("asyncio").ensure_future(r.abort()))
                errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
                await pg.goto(f"http://127.0.0.1:{PORT}/index.html",wait_until="domcontentloaded")
                await pg.evaluate(f"localStorage.setItem('clinipd:scheme','{sc}');localStorage.setItem('clinipd:mode','{mode}')")
                await pg.reload(wait_until="domcontentloaded"); await pg.wait_for_timeout(700)
                r=await pg.evaluate("""(fn)=>{
                  const ratio=eval('('+fn+')');
                  const cs=getComputedStyle(document.body);
                  const bg=cs.backgroundColor;
                  const out={body:ratio(cs.color,bg)};
                  const m=document.querySelector('.dim,.lede');
                  if(m) out.lede=ratio(getComputedStyle(m).color,bg);
                  const btn=document.querySelector('.btn.pri');
                  if(btn){const bs=getComputedStyle(btn); out.btn=ratio(bs.color,bs.backgroundColor);}
                  const ov=document.documentElement.scrollWidth-document.documentElement.clientWidth;
                  return {out,ov};
                }""", RATIO)
                vals={k:round(v,2) for k,v in r['out'].items()}
                bad=[k for k,v in vals.items() if v<4.5]
                name=sc or "clinical"
                flag=""
                if bad: flag=" <-- "+",".join(bad); fails.append(f"{name}/{mode}: {bad}")
                if r['ov']>0: flag+=f" OVERFLOW {r['ov']}"; fails.append(f"{name}/{mode} overflow")
                if errs: flag+=" ERR"; fails.append(f"{name}/{mode} js")
                print(f"  {name:10} {mode:5} " + "  ".join(f"{k}={v}" for k,v in vals.items()) + flag)
                await ctx.close()
        await b.close()
    print("\nFAILURES:",len(fails))
    for f in fails[:10]: print("   -",f)
asyncio.run(main())
