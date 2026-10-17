#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-party-kit.

A single-purpose page for the seasonal "vision board party" intent (November to January):
invitation text, a timed 2-hour agenda, one printable A4 sheet with 12 prompt cards and a QR
code to the free phone maker, a supply list and FAQ.

Needs `segno` for the QR code (pip install segno). Run: python3 build.py
"""
import html as _html
import pathlib
from urllib.parse import urlencode

import segno

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-party-kit/"
SRC = "ghpages_party"
CAMPAIGN = "party_kit_2027"
PAYPAL_CID = "Ae-xjt-swINgDhNcLWajKo9dP2_1J9HPULAWafFQcmUmkZCZ6N1Kzy56GXo1YXIpUO4kjlsuSunMSTaQ"

SERIF = "Georgia, Times New Roman, serif"
SANS = "Helvetica Neue, Helvetica, Arial, sans-serif"
ACC = "#6D28D9"
MUTED = "#6B7280"
RULE = "#D4D4D8"

PROMPTS = [
    "What do I want more of in 2027?",
    "What am I done putting up with?",
    "If 2027 had one word, what would it be?",
    "What would make 31 December 2027 feel like a win?",
    "Who do I want to see more often?",
    "What would I try if nobody was watching?",
    "Where do I want to wake up?",
    "What does an ordinary Tuesday look like in my best 2027?",
    "What do I want people to ask me for advice about?",
    "What number do I want to see in my savings account?",
    "What is my body asking me for this year?",
    "What first step can I take before 1 January?",
]

# Printed QR goes to the phone maker; utm_medium=print keeps paper scans apart from page clicks.
QR_URL = ("https://visionboard.bemooore.com/free-vision-board-maker/?"
          + urlencode({"mode": "wallpaper", "utm_source": "party_qr", "utm_medium": "print", "utm_campaign": CAMPAIGN}))


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


TOOL = link("/free-vision-board-maker/", mode="wallpaper")
WALL_2027 = link("/2027-vision-board-wallpaper/")
HOME = link("/")

INVITE = """You're invited to a vision board party for 2027.

When: [day, date], [time] (about 2 hours)
Where: [address or video link]

Bring 2-3 old magazines if you have them, and one photo of something you want more of next year. I'll have scissors, glue, boards and snacks.

No magazines? Bring your phone. We'll also make a version you can keep as your lock screen.

You'll leave with a finished board and one first step you take before 1 January."""

AGENDA = [
    ("0:00", "Arrive, drinks, everyone writes 2027 in one word on a sticky note and keeps it hidden."),
    ("0:15", "Prompt round. Each guest draws two prompt cards and answers them out loud in one minute. Nobody comments."),
    ("0:35", "Hunt. Cut pictures and words that match your answers. Rule: no picture without a reason you can say in one sentence."),
    ("1:05", "Build. Glue the board. The one word goes in the middle, the first step goes in the bottom corner."),
    ("1:40", "Share. Two minutes each: the word, one picture, the first step and its date."),
    ("1:55", "Phones out. Photograph the board or scan the QR on the card sheet and save your goal as a lock screen."),
]

SUPPLIES = [
    "One board per guest: A3 card, cork tile or a 30x40 cm foam board",
    "15-20 old magazines for 8 guests, plus printed photos guests bring",
    "Scissors (one pair per two guests), glue sticks, washi tape",
    "Sticky notes and two markers per table",
    "The 12 prompt cards from this page, printed and cut (one sheet is enough for 6 guests, print two for 12)",
    "Snacks that do not leave grease on paper",
]

FAQ = [
    ("How do you host a vision board party?",
     "Invite 4 to 12 people, give everyone a board and magazines, and run it in four parts: two prompt cards answered out loud, "
     "30 minutes of cutting, 35 minutes of building, and a short round where each guest names one picture and one first step. "
     "The printable prompt cards and the 2-hour agenda on this page cover the whole evening."),
    ("What do you need for a vision board party?",
     "A board per guest, old magazines, scissors, glue sticks, sticky notes, markers and the printed prompt cards. "
     "Guests without magazines can make their board on their phone with the free maker linked from the QR code on the card sheet."),
    ("How long should a vision board party last?",
     "About two hours. Shorter and nobody finishes the board, longer and the sharing round drags."),
    ("When is the best time to host a 2027 vision board party?",
     "Between mid-November and mid-January. A party before New Year lets every guest take the first step before 1 January."),
    ("Can I host a virtual vision board party?",
     "Yes. Send the invitation with a video link, share the prompt cards on screen, and have guests build on their phones with the free maker. "
     "Each guest ends with a 1080x1920 lock-screen wallpaper instead of a paper board."),
    ("Is this party kit free?",
     "Yes. The prompt cards, agenda, invitation and supply list are free and MIT licensed. No signup, no e-mail."),
]


def wrap(text, width):
    lines, cur = [], ""
    for w in text.replace("31 December", "31\u00a0December").replace("1 January", "1\u00a0January").split(" "):
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def t(x, y, s, size, fill="#111827", family=SANS, anchor=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x:g}" y="{y:g}"{a} font-family="{family}" font-size="{size:g}" fill="{fill}"{extra}>'
            f'{_html.escape(s)}</text>')


def qr_svg(x, y, size):
    q = segno.make(QR_URL, error="m")
    m = q.matrix
    n = len(m) + 8  # 4-module quiet zone on each side
    cell = size / n
    parts = [f'<rect x="{x:g}" y="{y:g}" width="{size:g}" height="{size:g}" fill="#FFFFFF"/>']
    path = []
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if v:
                path.append(f"M{x + (c + 4) * cell:.3f} {y + (r + 4) * cell:.3f}h{cell:.3f}v{cell:.3f}h-{cell:.3f}z")
    parts.append(f'<path d="{"".join(path)}" fill="#111827"/>')
    return "".join(parts)


def sheet():
    o = ['<svg id="svg-cards" class="sheet" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg" role="img" '
         'aria-label="Vision board party prompt cards for 2027, 12 cards, printable">',
         '<rect width="210" height="297" fill="#FFFFFF"/>',
         t(12, 18, "Vision Board Party: 12 Prompt Cards for 2027", 9, family=SERIF),
         t(12, 24.5, "Cut along the dashed lines. Each guest draws two cards and answers out loud before cutting a single picture.", 3.7, MUTED)]
    x0, y0, cw, ch, gap = 12, 30, 62, 56, 0
    for i, p in enumerate(PROMPTS):
        col, row = i % 3, i // 3
        x, y = x0 + col * cw, y0 + row * ch
        o.append(f'<rect x="{x:g}" y="{y:g}" width="{cw:g}" height="{ch:g}" fill="none" stroke="{RULE}" '
                 f'stroke-width="0.35" stroke-dasharray="1.6 1.2"/>')
        o.append(t(x + 5, y + 8.5, f"{i + 1:02d}", 4, ACC, extra=' letter-spacing="0.5"'))
        lines = wrap(p, 21)
        ly = y + ch / 2 - (len(lines) - 1) * 3.4 + 1.5
        for j, ln in enumerate(lines):
            o.append(t(x + cw / 2, ly + j * 6.8, ln, 5.2, family=SERIF, anchor="middle"))
        o.append(t(x + cw / 2, y + ch - 5, "2027 vision board party", 2.9, "#A1A1AA", anchor="middle"))
    qy = y0 + 4 * ch + 4  # 258
    o.append(qr_svg(12, qy, 26))
    o.append(t(42, qy + 8, "NO MAGAZINES? MAKE IT ON YOUR PHONE", 3.7, ACC, extra=' letter-spacing="0.5"'))
    o.append(t(42, qy + 14, "Scan, type your goal and first step, save it as your lock screen.", 3.9))
    o.append(t(42, qy + 19.5, "Free, no signup, nothing uploaded.", 3.9, MUTED))
    o.append(f'<line x1="12" y1="288" x2="198" y2="288" stroke="{RULE}" stroke-width="0.3"/>')
    o.append(t(12, 292.5, "Vision Board Party Kit 2027 - free, MIT licensed - pittner.github.io/vision-board-party-kit", 3.4, MUTED))
    o.append(t(198, 292.5, "visionboard.bemooore.com", 3.4, MUTED, anchor="end"))
    o.append("</svg>")
    return "".join(o)


def e(s):
    return _html.escape(s, quote=True)


def build():
    agenda = "\n".join(f"      <li><b>{e(a)}</b> {e(b)}</li>" for a, b in AGENDA)
    supplies = "\n".join(f"    <li>{e(s)}</li>" for s in SUPPLIES)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    import json
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%SHEET%%": sheet(), "%%AGENDA%%": agenda, "%%SUPPLIES%%": supplies, "%%FAQ%%": faq_html,
        "%%LD%%": ld, "%%INVITE%%": e(INVITE), "%%TOOL%%": e(TOOL), "%%WALL%%": e(WALL_2027),
        "%%HOME%%": e(HOME), "%%URL%%": URL, "%%SRC%%": SRC, "%%CID%%": PAYPAL_CID,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vision Board Party Kit 2027: Free Printable Prompt Cards, Agenda &amp; Invitation</title>
<meta name="description" content="Host a 2-hour vision board party for 2027: free printable prompt cards, a timed agenda, invitation text, a supply list and a phone option for guests without magazines. No signup, MIT licensed.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Vision Board Party Kit 2027 - free printable host guide">
<meta property="og:description" content="12 printable prompt cards, a 2-hour agenda, invitation text and a supply list for a 2027 vision board party. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#6D28D9;--bg:#FBFAF9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#5B21B6;color:#fff}
.main{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px;align-items:start;padding:12px 0 36px}
@media (max-width:760px){.main{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--rule);border-radius:16px;overflow:hidden}
.preview{padding:16px}
.preview svg{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:6px}
.actions{padding:0 16px 16px;display:flex;gap:8px;flex-wrap:wrap}
.side h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.side ol{list-style:none;padding:0;margin:0 0 18px;color:#374151}
.side li{margin:0 0 10px}
.side li b{display:inline-block;min-width:3.2em;color:var(--acc);font-variant-numeric:tabular-nums}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}
section.block{padding:30px 0;border-top:1px solid var(--rule)}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
textarea.invite{width:100%;max-width:640px;min-height:250px;border:1px solid var(--rule);border-radius:12px;padding:14px 16px;font:15px/1.55 inherit;color:#374151;background:#fff;resize:vertical}
ul.sup{max-width:70ch;color:#374151;padding-left:20px}
ul.sup li{margin:6px 0}
.after{margin:0 16px 16px;padding:16px 18px;border:1px solid var(--rule);border-left:4px solid var(--acc);border-radius:12px;background:#FAF7FF;font-size:15px;color:#374151}
.after[hidden]{display:none}
.after p{margin:0 0 10px}
.after .lbl{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:14px 0 6px}
.tip-amts{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 10px}
.tip-amt.on{background:var(--acc);border-color:var(--acc);color:#fff}
#tip-go:disabled{opacity:.7;cursor:default}
#tip-msg{margin-top:8px;font-size:13px;color:var(--muted)}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
@media print{
  body{background:#fff}
  .wrap>*:not(.printzone){display:none!important}
  .printzone{display:block!important}
  .printzone svg{width:100%;height:auto;display:block;border:0}
}
@page{size:A4 portrait;margin:0}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Vision board party kit for 2027</h1>
  <p class="lede">Everything you need to host a two-hour vision board party before New Year: 12 printable prompt cards, a timed agenda, an invitation you can paste into a group chat, and a supply list. Guests without magazines scan the QR on the card sheet and make their board on their phone. Free, no signup, no e-mail.</p>
  <p class="meta">4 to 12 guests &middot; about 2 hours &middot; A4 and US Letter &middot; SVG and PNG download &middot; MIT licensed</p>
</header>

<div class="main">
  <article class="card" id="cards">
    <div class="preview">%%SHEET%%</div>
    <div class="actions">
      <button class="btn primary" data-print="cards">Print the prompt cards</button>
      <button class="btn" data-svg="cards">Download SVG</button>
      <button class="btn" data-png="cards">Download PNG</button>
    </div>
    <div class="after" id="afterDl" hidden>
      <p><strong>Saved.</strong> The QR at the bottom of the sheet opens the free maker, so guests without magazines can type their goal and first step and keep it as a 1080&times;1920 lock screen. You can try it first yourself.</p>
      <a class="btn primary" href="%%TOOL%%" data-cta="after_dl_tool">Try the phone version</a>
      <div class="lbl">Or just say thanks</div>
      <p>This kit is free and MIT licensed, and it stays that way. If it saved you an evening of preparation, you can send a one-off thank you. You get nothing extra for it.</p>
      <div class="tip-amts" role="group" aria-label="Amount">
        <button type="button" class="btn tip-amt" data-amt="3">&euro;3</button>
        <button type="button" class="btn tip-amt on" data-amt="5">&euro;5</button>
        <button type="button" class="btn tip-amt" data-amt="10">&euro;10</button>
      </div>
      <button type="button" class="btn" id="tip-go">Say thanks with PayPal</button>
      <div id="tip-pp" style="max-width:360px;margin-top:10px"></div>
      <div id="tip-msg">PayPal handles the payment. Nothing is loaded from PayPal until you press the button.</div>
    </div>
  </article>

  <div class="side">
    <h2>The 2-hour agenda</h2>
    <div class="bar">
      <button class="btn primary" id="pageA4" aria-pressed="true">Paper: A4</button>
      <button class="btn" id="pageLetter" aria-pressed="false">Paper: US Letter</button>
    </div>
    <ol>
%%AGENDA%%
    </ol>
    <p class="meta">Why the prompt round comes first: guests who answer two questions before touching a magazine cut pictures for a reason, and the board ends up being about them, not about the magazines you happened to have.</p>
  </div>
</div>

<section class="block">
  <h2>Invitation text</h2>
  <p>Paste it into a group chat or an e-mail and fill in the brackets.</p>
  <textarea class="invite" id="invite" readonly>%%INVITE%%</textarea>
  <p><button class="btn primary" id="copyInvite" type="button">Copy invitation</button> <span class="meta" id="copyMsg"></span></p>
</section>

<section class="block">
  <h2>What to buy for 8 guests</h2>
  <ul class="sup">
%%SUPPLIES%%
  </ul>
</section>

<section class="block">
  <h2>No magazines, or hosting on a video call?</h2>
  <p>Every guest opens the free maker on their phone, types the goal and the first step from their prompt cards, adds a photo if they want, and saves it as a 1080&times;1920 lock-screen wallpaper. It runs in the browser, nothing is uploaded and nobody has to sign up. The QR on the card sheet opens the same page.</p>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="section_phone_tool">Open the free phone maker</a>
     <a class="btn" href="%%WALL%%" data-cta="section_wallpaper_2027">20 ready 2027 goals as wallpapers</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-templates/">all 7 printable vision board templates</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">AI vision board prompts</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students (classroom kit)</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-party-kit">source</a>
</footer>

<div class="printzone" id="printzone" style="display:none"></div>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries the button and where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_content='+encodeURIComponent(a.getAttribute('data-cta'))+'&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  var ps=document.createElement('style'); document.head.appendChild(ps);
  function paper(size){
    ps.textContent='@page{size:'+size+' portrait;margin:'+(size==='A4'?'0':'6mm')+'}';
    document.getElementById('pageA4').classList.toggle('primary',size==='A4');
    document.getElementById('pageLetter').classList.toggle('primary',size!=='A4');
    document.getElementById('pageA4').setAttribute('aria-pressed',String(size==='A4'));
    document.getElementById('pageLetter').setAttribute('aria-pressed',String(size!=='A4'));
  }
  paper('A4');
  document.getElementById('pageA4').onclick=function(){paper('A4');beacon('cta_click','paper_a4');};
  document.getElementById('pageLetter').onclick=function(){paper('Letter');beacon('cta_click','paper_letter');};

  var cm=document.getElementById('copyMsg');
  document.getElementById('copyInvite').onclick=function(){
    var ta=document.getElementById('invite');
    beacon('cta_click','copy_invite');
    function done(){ cm.textContent='Copied. Paste it into your group chat.'; }
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(ta.value).then(done,function(){ ta.select(); document.execCommand('copy'); done(); });
    } else { ta.select(); document.execCommand('copy'); done(); }
  };

  var after=document.getElementById('afterDl');
  function showAfter(){ after.hidden=false; }

  // Voluntary thank-you, same flow as T-095/T-105/T-107: PayPal SDK loads only on click.
  var amt='5',tipLoading=false,amts=document.querySelector('.tip-amts'),go=document.getElementById('tip-go'),msg=document.getElementById('tip-msg');
  amts.addEventListener('click',function(e){
    var b=e.target.closest('.tip-amt'); if(!b)return;
    amt=b.getAttribute('data-amt');
    Array.prototype.forEach.call(amts.querySelectorAll('.tip-amt'),function(x){x.classList.toggle('on',x===b);});
  });
  go.addEventListener('click',function(){
    if(tipLoading)return; tipLoading=true; go.disabled=true; go.textContent='Loading PayPal...';
    beacon('cta_click','tip_open_'+amt);
    var s=document.createElement('script');
    s.src='https://www.paypal.com/sdk/js?client-id=%%CID%%&currency=EUR&intent=capture&components=buttons';
    s.onerror=function(){ tipLoading=false; go.disabled=false; go.textContent='Say thanks with PayPal'; msg.textContent='PayPal could not be loaded. Please try again in a moment.'; };
    s.onload=function(){
      go.style.display='none';
      window.paypal.Buttons({
        style:{layout:'vertical',label:'paypal'},
        createOrder:function(d,actions){
          return actions.order.create({
            purchase_units:[{amount:{value:amt,currency_code:'EUR'},custom_id:'tip-vb-party',description:'Vision board party kit 2027, voluntary thank you'}],
            application_context:{brand_name:'VisionBoard',user_action:'PAY_NOW',shipping_preference:'NO_SHIPPING'}
          });
        },
        onApprove:function(d,actions){
          return actions.order.capture().then(function(){
            beacon('cta_click','tip_paid_'+amt);
            document.getElementById('tip-pp').innerHTML='<p><strong>Thank you.</strong> The payment went through.</p>';
            msg.textContent='PayPal has emailed you the receipt.';
          });
        },
        onError:function(){ msg.textContent='Something went wrong at PayPal and no money was taken. You can try again.'; }
      }).render('#tip-pp');
    };
    document.head.appendChild(s);
  });

  function svgEl(){ return document.getElementById('svg-cards'); }
  function serialize(){
    var s=svgEl().cloneNode(true); s.removeAttribute('class'); s.removeAttribute('id');
    s.setAttribute('xmlns','http://www.w3.org/2000/svg');
    s.setAttribute('width','210mm'); s.setAttribute('height','297mm');
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+new XMLSerializer().serializeToString(s);
  }
  function save(blob,name){
    var u=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=u;a.download=name;document.body.appendChild(a);a.click();
    setTimeout(function(){URL.revokeObjectURL(u);a.remove();},1500);
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b)return;
    if(b.hasAttribute('data-print')){
      var z=document.getElementById('printzone');
      z.innerHTML=''; z.appendChild(svgEl().cloneNode(true)); z.style.display='block';
      beacon('template_print','party-cards');
      window.print();
      setTimeout(function(){z.style.display='none';z.innerHTML='';showAfter();},800);
    } else if(b.hasAttribute('data-svg')){
      save(new Blob([serialize()],{type:'image/svg+xml'}),'vision-board-party-prompt-cards-2027.svg');
      beacon('template_download','party-cards|svg');
      showAfter();
    } else if(b.hasAttribute('data-png')){
      var img=new Image(), src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(serialize())));
      img.onload=function(){
        var c=document.createElement('canvas'); c.width=1654; c.height=2339; // A4 @ 200dpi
        var x=c.getContext('2d'); x.fillStyle='#fff'; x.fillRect(0,0,c.width,c.height);
        x.drawImage(img,0,0,c.width,c.height);
        c.toBlob(function(bl){ save(bl,'vision-board-party-prompt-cards-2027.png'); },'image/png');
      };
      img.src=src;
      beacon('template_download','party-cards|png');
      showAfter();
    }
  });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
