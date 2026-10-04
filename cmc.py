#  This file is part of lceta modules
#  Copyright (c) 2026 lceta
#  This software is released under the MIT License.
#  https://opensource.org/licenses/MIT

# meta developer: @lceta
# meta tags: statistics, chat, messages, media, lurkers, analytics, report, automation
# meta banner: https://raw.githubusercontent.com/lcetaa/CMC-heroku-bot/refs/heads/main/meta_banner.png
# meta pic: https://raw.githubusercontent.com/lcetaa/CMC-heroku-bot/refs/heads/main/meta_pic.png

__version__ = (4, 0, 2)

# ░█░░░█▀▀░█▀▀░▀█▀░█▀█
# ░█░░░█░░░█▀▀░░█░░█▀█
# ░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀

import asyncio
import logging
import base64
import hashlib
import io
import json
import re
import time
import html as _html
from urllib.parse import quote as _quote
from datetime import datetime, timezone

import aiohttp
from .. import loader, utils

UPDATE_URL = "https://raw.githubusercontent.com/lcetaa/CMC-heroku-bot/refs/heads/main/cmc.py"
UPDATE_LOCK_WAIT = 15
MUSIC_EXT = (".mp3", ".ogg", ".opus", ".m4a", ".aac", ".wav")
MUSIC_TTL = 60
UPDATE_INSTALL_TIMEOUT = 60
logger = logging.getLogger(__name__)
try:
    import herokutl as hikkatl
    from herokutl.errors import FloodWaitError
except ImportError:
    import hikkatl
    from hikkatl.errors import FloodWaitError


def _emoji(i, c):
    return f"<emoji document_id={i}>{c}</emoji>"


EMO = {
    "total_messages": _emoji(5886436057091673541, "💬"),
    "total_media": _emoji(5931472654660800739, "📊"),
    "stickers": _emoji(6030466823290360017, "🖼"),
    "gifs": _emoji(5944777041709633960, "🎞"),
    "photos": _emoji(6048390817033228573, "📷"),
    "videos": _emoji(5944753741512052670, "📷"),
    "voice": _emoji(6030722571412967168, "🎤"),
    "documents": _emoji(6039630677182254664, "📂"),
    "photo_video": _emoji(6048390817033228573, "📷"),
    "total_members": _emoji(5942877472163892475, "👥"),
    "admins": _emoji(5778423822940114949, "🛡"),
    "deleted_accounts": _emoji(5872829476143894491, "🚫"),
}
E_USER = _emoji(5886412370347036129, "👤")
E_MSG = EMO["total_messages"]
E_NOTE = _emoji(5881845358008763202, "📝")

MEDIA = (("sticker", "stickers"), ("gif", "gifs"), ("photo", "photos"),
         ("video", "videos"), ("voice", "voice"), ("document", "documents"))
USER_KEYS = ("total_messages", "total_media", "stickers", "gifs", "photos", "videos", "voice", "documents")


def _svg(body):
    return f'<svg class="ic" viewBox="0 0 24 24">{body}</svg>'


MUSIC_JS = r"""
(function(){
var $=function(i){return document.getElementById(i)};
var b=$('mu'),pl=$('mpl'),pp=$('mpp'),cl=$('mpx');if(!b||!pl)return;
var urls=(typeof MU!=='undefined'&&MU.length)?MU.slice():[];
for(var k=urls.length-1;k>0;k--){var j=Math.floor(Math.random()*(k+1)),t0=urls[k];urls[k]=urls[j];urls[j]=t0}
if(!urls.length){b.style.display='none';return}
var lst=$('mls'),lop=false,mt=$('mpt'),ms=$('mps'),bw=$('mpb'),br=$('mpr'),bf=$('mpf'),ta=$('mpa'),td=$('mpd'),pv=$('mpv'),nx=$('mpn');
var on=false,au,ai=0,fails=0;
var AC=window.AudioContext||window.webkitAudioContext,ac=null,an=null,fd=null,fxCors=!!AC,cok=false,raf=0,lb=0,ltk=0,gmx=-40,tL=null,tC=null,tb=null,cr=0,lv=0,wu=0,DL=mkd(4),DC=mkd(6);
var fx=window.CMCFX={bass:0,beat:0,b:[0,0,0,0]},eq=pl.querySelectorAll('.mpe i');
function title(u){
  try{u=decodeURIComponent(u.split('?')[0].split('/').pop())}catch(e){u=u.split('/').pop()}
  return u.replace(/\.[a-z0-9]+$/i,'').replace(/[-_+]+/g,' ').trim()||'Track'}
function fmt(s){if(!isFinite(s))return'0:00';s=Math.floor(s);return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
function buildList(){
  var h='',i;for(i=0;i<urls.length;i++)
    h+='<button data-i="'+i+'"'+(i===ai?' class="cur"':'')+'><span class="n">'+(i+1)+'</span><span class="t"></span><svg class="e" viewBox="0 0 24 24"><path d="M7 4v16l13-8z"/></svg></button>';
  lst.innerHTML=h;
  var bs=lst.children;for(i=0;i<bs.length;i++)bs[i].children[1].textContent=title(urls[i])}
function placeList(){
  if(!lop)return;
  var r=pl.getBoundingClientRect(),t=r.bottom+6;
  lst.style.left=r.left+'px';lst.style.width=r.width+'px';lst.style.top=t+'px';
  lst.style.maxHeight=Math.max(120,Math.min(window.innerHeight*.55,window.innerHeight-t-10))+'px';
  requestAnimationFrame(placeList)}
function closeList(){lop=false;lst.classList.remove('open');pl.classList.remove('lo')}
function toggleList(){
  if(lop){closeList();return}
  lop=true;buildList();lst.classList.add('open');pl.classList.add('lo');placeList();
  var c=lst.querySelector('.cur');if(c)lst.scrollTop=Math.max(0,c.offsetTop-lst.clientHeight/2+c.offsetHeight/2)}
lst.addEventListener('click',function(e){
  var bt=e.target.closest('button');if(!bt)return;
  ai=+bt.getAttribute('data-i');load();closeList();if(on)playFile();else start()});
document.addEventListener('pointerdown',function(e){
  if(lop&&!lst.contains(e.target)&&!pl.contains(e.target))closeList()});
function info(){
  if(lop)buildList();
  mt.textContent=title(urls[ai]);
  ms.textContent=L.m_of.replace('{0}',ai+1).replace('{1}',urls.length);
  pv.disabled=nx.disabled=urls.length<2;
  if('mediaSession' in navigator&&window.MediaMetadata)
    navigator.mediaSession.metadata=new MediaMetadata({title:mt.textContent,artist:'CMC'})}
function prog(){
  var d=au&&au.duration;
  bf.style.width=(d&&isFinite(d)?au.currentTime/d*100:0)+'%';
  ta.textContent=fmt(au?au.currentTime:0);td.textContent=fmt(d)}
function mk(c){
  var a=new Audio();a.preload='none';if(c)a.crossOrigin='anonymous';
  a.addEventListener('timeupdate',function(){if(a===au)prog()});
  a.addEventListener('loadedmetadata',function(){if(a===au)prog()});
  a.addEventListener('ended',function(){if(a!==au)return;
    if(urls.length>1)go(1);else{a.currentTime=0;a.play().catch(halt)}});
  a.addEventListener('playing',function(){if(a===au){fails=0;cok=true}});
  a.addEventListener('error',function(){if(a===au)onErr()});
  return a}
function getAu(){if(au)return au;au=mk(fxCors);return au}
function fxInit(){
  if(ac||!fxCors||!AC)return;
  try{var a=getAu(),c=new AC(),s=c.createMediaElementSource(a),n=c.createAnalyser();
    n.fftSize=2048;n.smoothingTimeConstant=0;s.connect(n);n.connect(c.destination);
    tL=chain(c,s,35,150);tC=chain(c,s,130,400);tb=new Float32Array(2048);
    ac=c;an=n;fd=new Float32Array(n.frequencyBinCount)}catch(e){ac=null;an=null;tL=tC=null}}
function chain(c,s,lo,hi){
  var h=c.createBiquadFilter(),l=c.createBiquadFilter(),n=c.createAnalyser(),g=c.createGain();
  h.type='highpass';h.frequency.value=lo;h.Q.value=-3.01;l.type='lowpass';l.frequency.value=hi;l.Q.value=-3.01;
  n.fftSize=2048;n.smoothingTimeConstant=0;g.gain.value=0;
  s.connect(h);h.connect(l);l.connect(n);n.connect(g);g.connect(c.destination);return n}
function fxOff(){
  fxCors=false;var o=au;au=null;
  if(o){try{o.pause();o.removeAttribute('src');o.load()}catch(e){}}
  if(ac){try{ac.close()}catch(e){}}
  ac=null;an=null;fd=null;tL=tC=tb=null;
  au=mk(false);load();if(on)playFile()}
function bdb(lo,hi){
  var bh=ac.sampleRate/an.fftSize,a=Math.max(1,Math.round(lo/bh)),b=Math.max(a+1,Math.round(hi/bh)),t=0;
  for(var k=a;k<b&&k<fd.length;k++){var v=fd[k];if(!(v>-140))v=-140;t+=Math.pow(10,v/10)}
  return 10*Math.log10(t/(b-a)+1e-14)}
function mkd(m){return{h:[],pk:m*2,last:-1e9,m:m}}
function bst(o,L,t,dk){
  var h=o.h,i,mn=1e9,r,k;h.push([t,L]);
  while(h.length&&t-h[0][0]>140)h.shift();
  for(i=0;i<h.length;i++)if(h[i][1]<mn)mn=h[i][1];
  r=L-mn;k=o.pk*dk;o.pk=r>0?Math.max(k,r):k;
  if(r>Math.max(o.m,.5*o.pk)&&h.length>3&&L-h[h.length-4][1]>=1&&t-o.last>110){o.last=t;return r/Math.max(o.pk,1e-6)}
  return 0}
function msq(a,e){var s=0,i;for(i=e-1024;i<e;i++)s+=a[i]*a[i];return 10*Math.log10(s/1024+1e-10)}
function tick(now){
  raf=0;var live=!!(on&&an&&ac&&ac.state==='running'),bl=[0,0,0,0],i,dt=Math.min(Math.max((now-ltk)/1000,.001),.1);ltk=now;
  if(live){
    an.getFloatFrequencyData(fd);
    var Lb=bdb(40,130),vb=0;
    fx.bass*=Math.exp(-dt/.15);
    if(tL&&tC){
      var sr=ac.sampleRate,B=256,dk=Math.exp(-B/sr/2.5),na,nb,j,xs=[],ys=[],ts,v;
      cr+=dt*sr;na=Math.floor(cr/B);cr-=na*B;nb=Math.min(4,na);
      tL.getFloatTimeDomainData(tb);for(j=0;j<nb;j++)xs.push(msq(tb,2048-(nb-1-j)*B));
      tC.getFloatTimeDomainData(tb);for(j=0;j<nb;j++)ys.push(msq(tb,2048-(nb-1-j)*B));
      for(j=0;j<nb;j++){ts=now-(nb-1-j)*B/sr*1000;
        v=Math.max(bst(DL,xs[j],ts,dk),.9*bst(DC,ys[j],ts,dk));
        if(v>0&&ts-wu>250&&ts-lb>110&&(ts-lb>260||v>.7*lv)){lb=ts;lv=v;vb=Math.max(vb,v)}}
      if(vb>0){fx.beat=1;fx.bass=Math.max(fx.bass,.45+.55*Math.min(1,(vb-.5)*2))}}
    var bd=[Lb,bdb(130,500),bdb(500,2500),bdb(2500,9000)];
    gmx=Math.max(bd[0],bd[1],bd[2],bd[3],gmx-dt*3);
    for(i=0;i<4;i++)bl[i]=Math.pow(Math.max(0,Math.min(1,(bd[i]-(gmx-30))/30)),1.5);
  }else fx.bass*=Math.exp(-dt/.15);
  fx.beat*=Math.exp(-dt/.1);
  for(i=0;i<4;i++){fx.b[i]+=(bl[i]-fx.b[i])*.35;
    if(eq[i])eq[i].style.height=(12+88*Math.pow(Math.min(fx.b[i],1),2.2)).toFixed(0)+'%'}
  pl.classList.toggle('fx',live);
  document.documentElement.style.setProperty('--bs',fx.bass.toFixed(3));
  if(on||fx.bass>.01||fx.beat>.01)raf=requestAnimationFrame(tick);
  else{fx.bass=fx.beat=0;document.documentElement.style.setProperty('--bs','0');
    for(i=0;i<4;i++)if(eq[i])eq[i].style.height=''}}
function fxRun(){
  if(ac&&ac.state==='suspended'){try{ac.resume()}catch(e){}}
  if(ac)setTimeout(function(){if(on&&ac&&ac.state!=='running')fxOff()},1500);
  if(!raf)raf=requestAnimationFrame(tick)}
function load(){
  var a=getAu();a.src=urls[ai];wu=performance.now();lv=0;DL=mkd(4);DC=mkd(6);
  bf.style.width='0%';ta.textContent='0:00';td.textContent='0:00';info()}
function playFile(){
  var a=getAu();if(!a.src)load();
  var p=a.play();if(p&&p.catch)p.catch(halt)}
function go(d){
  if(urls.length<2)return;
  ai=(ai+d+urls.length)%urls.length;load();if(on)playFile()}
function halt(){on=false;pl.classList.remove('on')}
function onErr(){if(fxCors&&!cok){fxOff();return}fails++;if(urls.length>1&&fails<urls.length)go(1);else halt()}
function start(){on=true;pl.classList.add('show','on');b.classList.add('on');fxInit();playFile();fxRun()}
function pause(){on=false;pl.classList.remove('on');if(au)au.pause()}
function shut(){pause();closeList();pl.classList.remove('show');b.classList.remove('on')}
b.addEventListener('click',function(){pl.classList.contains('show')?shut():start()});
pp.addEventListener('click',function(){on?pause():start()});
cl.addEventListener('click',shut);
pv.addEventListener('click',function(){go(-1)});
nx.addEventListener('click',function(){go(1)});
br.addEventListener('click',function(e){
  if(!au||!isFinite(au.duration))return;
  var r=br.getBoundingClientRect();
  au.currentTime=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width))*au.duration});
if('mediaSession' in navigator){
  [['play',start],['pause',pause],['previoustrack',function(){go(-1)}],['nexttrack',function(){go(1)}]]
  .forEach(function(h){try{navigator.mediaSession.setActionHandler(h[0],h[1])}catch(e){}})}
(function(){
var dr=null,mv=false;
function home(){pl.classList.remove('drag');pl.classList.add('rel');pl.style.setProperty('--dx','0px');pl.style.setProperty('--dy','0px')}
pl.addEventListener('pointerdown',function(e){
  if(e.button>0||e.target.closest('button,#mpr'))return;
  var r=pl.getBoundingClientRect(),cx=r.left+r.width/2-pl.offsetLeft,cy=r.top-pl.offsetTop;
  dr={id:e.pointerId,x:e.clientX,y:e.clientY,cx:cx,cy:cy,r:r,t:e.target};mv=false;
  pl.classList.remove('rel');pl.classList.add('drag');
  pl.style.setProperty('--dx',cx+'px');pl.style.setProperty('--dy',cy+'px');
  try{pl.setPointerCapture(e.pointerId)}catch(x){}
  e.preventDefault()});
pl.addEventListener('pointermove',function(e){
  if(!dr||e.pointerId!==dr.id)return;
  if(!mv&&Math.abs(e.clientX-dr.x)+Math.abs(e.clientY-dr.y)<8)return;mv=true;
  var dx=dr.cx+e.clientX-dr.x,dy=dr.cy+e.clientY-dr.y;
  pl.style.setProperty('--dx',dx+'px');pl.style.setProperty('--dy',dy+'px')});
function end(e){
  if(!dr||e.pointerId!==dr.id)return;var d0=dr;dr=null;
  if(mv)home();else{pl.classList.remove('drag');
    if(e.type==='pointerup'&&d0.t&&d0.t.closest&&d0.t.closest('.mpi'))toggleList()}}
pl.addEventListener('pointerup',end);
pl.addEventListener('pointercancel',end);
pl.addEventListener('transitionend',function(e){if(e.propertyName==='transform'&&!dr)pl.classList.remove('rel')});
})();
info();
})();
"""

IC = {
    "users": _svg('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
    "moon": _svg('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'),
    "all": _svg('<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>'),
    "new": _svg('<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>'),
    "prem": _svg('<path d="m2 4 3 12h14l3-12-6 7-4-7-4 7-6-7zm3 16h14"/>'),
    "sel": _svg('<rect width="18" height="18" x="3" y="3" rx="2"/><path d="m9 12 2 2 4-4"/>'),
    "copy": _svg('<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>'),
    "music": _svg('<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'),
    "csv": _svg('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>'),
}

CSS = r""":root{--card:rgba(22,18,44,.72);--tx:#ecebff;--mt:#a9a5c9;--bd:rgba(160,140,255,.22);--bar:#4f6df0;--ac:#8fa6ff;--g-bg:#1f3310;--g-tx:#97C459;--a-bg:#3d2a0c;--a-tx:#FAC775;--r-bg:#3f1a1a;--r-tx:#F09595}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%;margin:0;padding:0;overflow:hidden}
body{color:var(--tx);font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:radial-gradient(ellipse 90% 60% at 18% -5%,#1b1250 0%,transparent 65%),radial-gradient(ellipse 80% 55% at 100% 100%,#36104d 0%,transparent 65%),radial-gradient(ellipse 60% 40% at 0% 100%,#08294d 0%,transparent 70%),#02030c;background-attachment:fixed}
#bg{position:fixed;top:0;left:0;right:0;bottom:0;z-index:0;pointer-events:none;overflow:hidden}
#stars{position:absolute;left:0;top:0;width:100%;height:100%}
.o{position:absolute;display:block;left:0;top:0;width:560px;height:560px;margin:-280px 0 0 -280px;border-radius:50%;will-change:transform,opacity}
.o1{background:radial-gradient(circle,rgba(100,72,225,.50),transparent 68%)}
.o2{background:radial-gradient(circle,rgba(30,150,205,.34),transparent 68%)}
.o3{background:radial-gradient(circle,rgba(205,62,165,.32),transparent 68%)}
.pl{position:absolute;right:-70px;top:96px;width:190px;height:190px;border-radius:50%;background:radial-gradient(circle at 30% 26%,#a9b9ff 0%,#5b4fd0 34%,#231a6b 68%,#070620 100%);box-shadow:inset -30px -22px 55px rgba(0,0,0,.7),0 0 calc(70px + var(--bs,0)*90px) rgba(120,140,255,calc(.28 + var(--bs,0)*.45));filter:brightness(calc(1 + var(--bs,0)*.4));opacity:.6;animation:plf 9s ease-in-out infinite alternate}
.pl::after{content:'';position:absolute;left:-45%;top:38%;width:190%;height:24%;border-radius:50%;border:3px solid rgba(200,210,255,.38);transform:rotate(-16deg);box-shadow:0 0 14px rgba(160,180,255,.25)}
#app{position:fixed;top:0;left:0;right:0;bottom:0;z-index:1;overflow-y:auto;overflow-x:hidden;padding:16px 34px 48px 16px;scrollbar-width:none;-ms-overflow-style:none;overscroll-behavior:contain}
#app::-webkit-scrollbar{display:none;width:0;height:0}
.w{max-width:640px;margin:0 auto}
.hero{display:flex;align-items:center;gap:14px;margin:4px 0 12px;will-change:transform,opacity}
.hi{width:60px;height:60px;border-radius:19px;display:flex;align-items:center;justify-content:center;font-size:31px;flex:none;background:linear-gradient(145deg,rgba(110,140,255,.32),rgba(255,255,255,.04));border:1px solid var(--bd);box-shadow:0 8px 28px rgba(79,109,240,.38),inset 0 1px 0 rgba(255,255,255,.14);animation:hf 4s ease-in-out infinite}
.ov{font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ac)}
h1{display:block;font-size:36px;line-height:1.05;margin:3px 0 0;font-weight:800;letter-spacing:-.02em;color:var(--tx)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 18px}
.chips span{font-size:12px;padding:4px 11px;border-radius:999px;border:1px solid var(--bd);background:rgba(255,255,255,.04);color:var(--mt);max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chips span:first-child{color:var(--tx)}
.st{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:18px}
.st div,.list,.pill,.btn,input[type=text]{-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.st div{display:block;border:1px solid var(--bd);border-radius:18px;padding:14px 16px;background:linear-gradient(145deg,rgba(110,140,255,.14),transparent 70%),var(--card);box-shadow:0 2px 10px rgba(0,0,0,.08);animation:up .5s both;transition:transform .2s}
.st div:nth-child(2){animation-delay:.08s}
.st div:hover{transform:translateY(-3px)}
.st small{display:flex;align-items:flex-start;gap:6px;min-height:2.6em;color:var(--mt);font-size:12px}
.st small .ic{width:15px;height:15px;color:var(--ac)}
.st b{display:inline-block;font-size:32px;font-weight:700;line-height:1.2}
.st div:first-child b{color:var(--ac)}
.st i{font-style:normal;color:var(--mt);font-size:13px;margin-left:6px}
.chh{display:flex;justify-content:space-between;color:var(--mt);font-size:13px;margin:6px 0 4px}
.bars{display:flex;align-items:flex-end;gap:8px;height:90px;padding-top:18px}
.bar{flex:1;min-width:6px;position:relative;background:linear-gradient(180deg,var(--ac),var(--bar));border-radius:8px 8px 0 0;transform-origin:bottom;animation:gr .8s cubic-bezier(.2,.8,.2,1) both}
.bar:nth-child(2){animation-delay:.08s}
.bar:nth-child(3){animation-delay:.16s}
.bar:nth-child(4){animation-delay:.24s}
.bar span{position:absolute;top:-16px;left:0;right:0;text-align:center;font-size:11px;color:var(--mt)}
.ax{display:flex;justify-content:space-between;color:var(--mt);font-size:12px;margin:4px 0 12px}
.ax.c{gap:8px}
.ax.c span{flex:1;text-align:center}
.pills,.tb{display:flex;flex-wrap:wrap;gap:8px}
.pills{margin:14px 0}
.tb{margin-bottom:10px}
.pill,.btn{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--bd);background:var(--card);color:var(--tx);font-weight:500;cursor:pointer}
.pill{border-radius:20px;padding:8px 16px;font-size:14px;transition:all .15s}
.btn{border-radius:12px;padding:10px 14px;font-size:13px}
.btn.on{border-color:var(--ac);color:var(--ac);box-shadow:0 0 14px rgba(143,166,255,.35)}
.mpl{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 8px);width:min(94vw,520px);z-index:60;display:flex;align-items:center;gap:10px;background:rgba(30,24,64,.28);border:1px solid rgba(190,175,255,.28);border-radius:18px;padding:10px 12px;box-shadow:0 8px 28px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.12),0 0 calc(var(--bs,0)*30px) rgba(143,166,255,calc(var(--bs,0)*.75));backdrop-filter:blur(18px) saturate(140%);-webkit-backdrop-filter:blur(18px) saturate(140%);text-shadow:0 1px 6px rgba(0,0,0,.55);transform:translate(calc(-50% + var(--dx,0px)),calc(-160% + var(--dy,0px)));opacity:0;pointer-events:none;transition:transform .35s ease,opacity .35s ease;touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none}
.mpl.show{transform:translate(calc(-50% + var(--dx,0px)),var(--dy,0px));opacity:1;pointer-events:auto}
.mpl.drag{transition:none;cursor:grabbing}
.mpl.on.fx .mpe i{animation:none;opacity:1;transition:height .06s linear}
.mpl.rel{transition:transform .7s cubic-bezier(.22,1,.36,1),opacity .35s ease}
.mpe{display:flex;align-items:flex-end;gap:3px;height:30px;width:28px;flex:none}
.mpe i{flex:1;height:25%;background:var(--ac);border-radius:2px;opacity:.45}
.mpl.on .mpe i{opacity:1;animation:mpq 1s ease-in-out infinite}
.mpe i:nth-child(2){animation-delay:.25s}.mpe i:nth-child(3){animation-delay:.5s}.mpe i:nth-child(4){animation-delay:.75s}
@keyframes mpq{0%,100%{height:25%}50%{height:100%}}
.mpi{flex:1;min-width:0}
.mpi b{display:block;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mpi small{display:block;color:var(--mt);font-size:11px;margin-top:1px}
.mpi{cursor:pointer}.mpi small::after{content:' \25BE';opacity:.8}.mpl.lo .mpi small::after{content:' \25B4'}
.mls{position:fixed;z-index:59;display:none;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;touch-action:pan-y;padding:6px;border-radius:16px;background:rgba(30,24,64,.66);border:1px solid rgba(190,175,255,.28);box-shadow:0 8px 28px rgba(0,0,0,.35);backdrop-filter:blur(18px) saturate(140%);-webkit-backdrop-filter:blur(18px) saturate(140%)}
.mls.open{display:block}
.mls button{display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:none;border:0;border-radius:10px;padding:11px 10px;color:var(--tx);font:inherit;font-size:13px;cursor:pointer}
.mls button.cur{background:rgba(143,166,255,.2);color:var(--ac)}
.mls .n{flex:none;width:22px;color:var(--mt);font-size:11px;font-variant-numeric:tabular-nums}
.mls .t{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mls .e{flex:none;width:14px;height:14px;fill:var(--ac);opacity:0}.mls .cur .e{opacity:1}
.mpb{display:flex;align-items:center;gap:6px;margin-top:7px;font-size:10px;color:var(--mt);font-variant-numeric:tabular-nums}
.mpr{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,.22);cursor:pointer;position:relative}
.mpr i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:3px;background:var(--ac)}
.mpk{display:flex;align-items:center;gap:6px;flex:none}
.mb{width:36px;height:36px;border-radius:50%;border:1px solid rgba(190,175,255,.3);background:rgba(255,255,255,.08);color:var(--tx);display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.mb svg{width:17px;height:17px;fill:currentColor}
.mb.big{width:44px;height:44px;border-color:var(--ac);color:var(--ac)}
.mb:disabled{opacity:.3;cursor:default}
.mb.sm{width:28px;height:28px;border-color:transparent;background:none;color:var(--mt)}
.mb.sm svg{width:15px;height:15px;fill:none}
.mpl.on .mb.big{box-shadow:0 0 14px rgba(143,166,255,.4)}
.mb .ia{display:none}.mpl.on .mb .ia{display:block}.mpl.on .mb .ip{display:none}
@media(max-width:420px){.mpe{display:none}}
.pill.on{background:var(--ac);border-color:var(--ac);color:#fff}
#cp{background:var(--ac);border-color:var(--ac);color:#fff}
.btn:active,.pill:active{transform:scale(.96)}
.pill:hover,.btn:hover{transform:translateY(-1px);border-color:var(--ac)}
input[type=text]{width:100%;padding:13px 16px;border-radius:14px;border:1px solid var(--bd);background:var(--card);color:var(--tx);font-size:15px;margin-bottom:10px;outline:none;transition:all .15s}
input[type=text]:focus{border-color:var(--ac);box-shadow:0 0 0 3px rgba(110,140,255,.28)}
.list{background:var(--card);border:1px solid var(--bd);border-radius:20px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.06)}
.row{display:flex;align-items:center;gap:8px;padding:12px 14px;border-bottom:1px solid rgba(160,140,255,.14);transition:background .15s}
.row:last-child{border-bottom:0}
.row:active{background:rgba(127,127,127,.14)}
.row:has(.cb:checked){background:rgba(110,140,255,.14)}
.row:hover{background:rgba(110,140,255,.08)}
.row.rv{opacity:0;transform:translateY(18px)}
.row.rv.in{opacity:1;transform:none;transition:opacity .5s ease,transform .55s cubic-bezier(.2,.8,.2,1),background .15s}
.cb{-webkit-appearance:none;appearance:none;flex:none;width:22px;height:22px;border-radius:7px;border:2px solid var(--bd);background:transparent;cursor:pointer;position:relative;accent-color:var(--ac);transition:all .15s}
.cb:checked{background:var(--ac);border-color:var(--ac)}
.cb:checked::after{content:'';position:absolute;left:6px;top:2px;width:5px;height:11px;border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
.who{display:flex;align-items:center;gap:10px;flex:1;min-width:0;text-decoration:none;color:inherit}
.av{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:500;flex:none;overflow:hidden;box-shadow:0 0 0 2px var(--card),0 0 0 3px rgba(127,127,127,.35);transition:transform .2s}
.row:hover .av{transform:scale(1.08)}
.av img{width:100%;height:100%;object-fit:cover;display:block}
.blue{background:#B5D4F4;color:#0C447C}
.green{background:#C0DD97;color:#27500A}
.amber{background:#FAC775;color:#633806}
.red{background:#F7C1C1;color:#791F1F}
.purple{background:#CECBF6;color:#3C3489}
.info{flex:1;min-width:0}
.info b{display:block;font-size:15px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.info small{display:block;color:var(--mt);font-size:12px;line-height:1.5;white-space:normal;overflow-wrap:anywhere}
.bd{font-size:11px;font-weight:600;padding:3px 9px;border-radius:12px;white-space:nowrap;flex:none}
.bd.g{position:relative;background:var(--g-bg);color:var(--g-tx)}
.bd.a{background:var(--a-bg);color:var(--a-tx)}
.bd.r{background:var(--r-bg);color:var(--r-tx)}
.bd.g::before{content:'';display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;margin-right:5px;vertical-align:middle;animation:pl 1.8s ease-in-out infinite}
.empty{display:none;text-align:center;color:var(--mt);padding:20px}
.note{color:var(--mt);font-size:12px;margin-top:12px}
.ic{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
#sb{position:fixed;right:0;top:70px;bottom:70px;width:36px;z-index:9;touch-action:none;display:none}
#th{position:absolute;right:7px;top:0;width:5px;height:56px;border-radius:3px;background:var(--bar);opacity:.55}
#sb.act #th{width:9px;right:5px;opacity:.9}
.wm{position:fixed;left:0;right:0;bottom:10px;z-index:3;text-align:center;pointer-events:none}
.wm a{pointer-events:auto;display:inline-block;font-size:11px;letter-spacing:.06em;color:var(--mt);text-decoration:none;padding:4px 12px;border-radius:999px;border:1px solid var(--bd);background:rgba(10,8,30,.55);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);opacity:.75}
.wm a b{color:var(--ac);font-weight:600}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes gr{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pl{50%{opacity:.25;transform:scale(.7)}}
@keyframes hf{50%{transform:translateY(-3px) rotate(-5deg)}}
@keyframes plf{to{transform:translateY(14px) rotate(3deg)}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
"""

JS = r"""
var $=function(s){return document.querySelector(s)},
$$=function(s){return[].slice.call(document.querySelectorAll(s))},
app=$('#app'),q=$('#q'),e=$('#e'),cp=$('#cp'),cpt=cp.querySelector('span'),sat=$('#sa span'),
sb=$('#sb'),th=$('#th'),hero=$('.hero'),chips=$('.chips'),o=$$('.o'),rs=$$('.row'),pills=$$('.pill'),
cv=$('#stars'),cx=cv.getContext('2d'),f='all',drag=0,sp=0,tp=0,last=0,vel=0,sy=0,W=0,H=0,on=0,nm=0,S=[],M=[],
t0=performance.now(),rm=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches,
P=[[.12,.08,.88,.78],[.92,.92,.08,.30],[.5,.5,.85,.12]],
COL=['255,255,255','190,210,255','255,228,200','210,190,255'],LR=[.45,.8,1.3],PX=[.015,.04,.09];
function show(r){return r.style.display!=='none'}
function cb(r){return r.querySelector('.cb')}
function chk(){return rs.filter(function(r){return cb(r).checked})}
function upd(){cpt.textContent=L.copy+' ('+chk().length+')';var v=rs.filter(show);
sat.textContent=v.length&&v.every(function(r){return cb(r).checked})?L.unsel:L.sel}
function apply(){var v=q.value.toLowerCase().trim(),n=0;
rs.forEach(function(r){var ok=(!v||r.dataset.s.indexOf(v)>-1)&&(f==='all'||r.dataset[f]==='1');
r.style.display=ok?'':'none';if(ok)n++});
e.style.display=n?'none':'block';upd()}
function flash(t){cpt.textContent=t;setTimeout(upd,1500)}
function copy(t,done){var fb=function(){var a=document.createElement('textarea');a.value=t;a.style.cssText='position:fixed;opacity:0';
document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(x){}document.body.removeChild(a)};
navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(t).then(done,fb):fb()}
function cq(s){return'"'+String(s).replace(/"/g,'""')+'"'}
q.addEventListener('input',apply);
pills.forEach(function(p){p.addEventListener('click',function(){
f=p.dataset.f;pills.forEach(function(x){x.classList.toggle('on',x===p)});apply()})});
document.addEventListener('change',function(ev){if(ev.target.classList.contains('cb'))upd()});
$('#sa').addEventListener('click',function(){var v=rs.filter(show),all=v.every(function(r){return cb(r).checked});
v.forEach(function(r){cb(r).checked=!all});upd()});
cp.addEventListener('click',function(){var c=chk();if(!c.length)return flash(L.pick);
copy(c.map(function(r){return r.dataset.u?'@'+r.dataset.u:r.dataset.id}).join('\n'),function(){flash(L.done+': '+c.length)})});
$('#csv').addEventListener('click',function(){
var out=[[L.c_name,L.c_user,L.c_id,L.c_joined,L.c_seen,L.c_prem].map(cq).join(',')];
rs.filter(show).forEach(function(r){var d=r.dataset;
out.push([d.n,d.u?'@'+d.u:'',d.id,d.j,d.l,d.pr==='1'?L.yes:''].map(cq).join(','))});
var a=document.createElement('a');
a.href=URL.createObjectURL(new Blob(['\ufeff'+out.join('\r\n')],{type:'text/csv;charset=utf-8'}));
a.download='silent_users.csv';document.body.appendChild(a);a.click();document.body.removeChild(a)});
function mx(){return app.scrollHeight-app.clientHeight}
function pos(){var m=mx();sb.style.display=m>app.clientHeight*.5?'block':'none';
th.style.top=(m>0?Math.min(app.scrollTop/m,1)*(sb.clientHeight-th.offsetHeight):0)+'px'}
function mv(y){var r=sb.getBoundingClientRect();
app.scrollTop=Math.min(Math.max((y-r.top-th.offsetHeight/2)/(r.height-th.offsetHeight),0),1)*mx()}
function end(){drag=0;sb.classList.remove('act')}
sb.addEventListener('pointerdown',function(ev){drag=1;sb.setPointerCapture(ev.pointerId);sb.classList.add('act');mv(ev.clientY);ev.preventDefault()});
sb.addEventListener('pointermove',function(ev){if(drag){mv(ev.clientY);ev.preventDefault()}});
sb.addEventListener('pointerup',end);sb.addEventListener('pointercancel',end);
app.addEventListener('scroll',function(){var s=app.scrollTop;vel+=Math.abs(s-last);last=s;tp=s/Math.max(mx(),1);sy=rm?0:s;
hero.style.transform='translateY('+(s*.28).toFixed(1)+'px)';hero.style.opacity=Math.max(1-s/260,0).toFixed(2);
chips.style.opacity=Math.max(1-s/200,0).toFixed(2);pos()},{passive:true});
if(window.ResizeObserver)new ResizeObserver(pos).observe(app.firstElementChild);
function init(){var d=Math.min(window.devicePixelRatio||1,2);W=innerWidth;H=innerHeight;
cv.width=W*d;cv.height=H*d;cx.setTransform(d,0,0,d,0,0);S=[];
for(var i=0,n=Math.min(Math.round(W*H/2400),900);i<n;i++){var r=Math.random(),l=r<.62?0:r<.9?1:2;
S.push({x:Math.random()*W,y:Math.random()*H,l:l,r:LR[l]*(.65+Math.random()*.7),ph:Math.random()*6.28,sp:.4+Math.random()*1.6,c:COL[Math.random()*4|0]})}}
function go(){if(!on&&!document.hidden){on=1;requestAnimationFrame(fr)}}
var pb=0,CM=[],CC=[['120,170,255','200,225,255'],['255,130,212','255,220,240'],['170,140,255','230,215,255']];
function fr(now){on=0;var t=rm?0:(now-t0)/1000;
sp+=(tp-sp)*.07;vel*=.9;var k=Math.min(vel/45,1),F=window.CMCFX,bs=F?F.bass:0,bt=F?F.beat:0;
o.forEach(function(el,i){var a=P[i],
x=(a[0]+(a[2]-a[0])*sp)*W+Math.sin(t*.35+i*2.1)*55,y=(a[1]+(a[3]-a[1])*sp)*H+Math.cos(t*.28+i*1.7)*55,
sc=1+.12*Math.sin(t*.5+i)+k*.35+bs*.45,op=i===0?1-.55*sp:i===2?.35+.65*sp:.8;
el.style.transform='translate3d('+x.toFixed(1)+'px,'+y.toFixed(1)+'px,0) scale('+sc.toFixed(3)+')';
el.style.opacity=Math.min(op+k*.2+bs*.3,1).toFixed(2)});
cx.clearRect(0,0,W,H);
S.forEach(function(s){var y=((s.y-sy*PX[s.l])%H+H)%H,a=(.35+.65*(.5+.5*Math.sin(t*s.sp+s.ph)))*(s.l?1:.7)*(1+bs*.6);
cx.fillStyle='rgba('+s.c+','+Math.min(a,1).toFixed(2)+')';cx.beginPath();cx.arc(s.x,y,s.r*(1+bs*.5),0,6.283);cx.fill();
if(s.l>1){cx.fillStyle='rgba('+s.c+','+(a*.16).toFixed(2)+')';cx.beginPath();cx.arc(s.x,y,s.r*4,0,6.283);cx.fill()}});
if(!rm){
if(bt>pb+.5&&CM.length<16){var c0=1+(bs>.85?2:bs>.65?1:0);
for(var q=0;q<c0;q++){var cc=CC[Math.random()*3|0];
CM.push({x:W*(.3+Math.random()),y:-40+Math.random()*H*.5,t:now+q*90,v:520+Math.random()*420,L:110+Math.random()*130+bs*90,w:1.6+Math.random()*1.8,a:cc[0],h:cc[1]})}}
pb=bt;
CM=CM.filter(function(c){var u=(now-c.t)/1000;if(u<0)return 1;if(u>2||c.x-c.v*.87*u<-300||c.y+c.v*.5*u>H+300)return 0;
var hx=c.x-c.v*.87*u,hy=c.y+c.v*.5*u,tx=hx+.87*c.L,ty=hy-.5*c.L,fd=Math.min(u/.15,1)*Math.min((2-u)/.4,1);
var g=cx.createLinearGradient(hx,hy,tx,ty);g.addColorStop(0,'rgba('+c.h+','+(fd*.95).toFixed(2)+')');
g.addColorStop(.25,'rgba('+c.a+','+(fd*.55).toFixed(2)+')');g.addColorStop(1,'rgba('+c.a+',0)');
cx.strokeStyle=g;cx.lineCap='round';cx.lineWidth=c.w;cx.beginPath();cx.moveTo(hx,hy);cx.lineTo(tx,ty);cx.stroke();
var rg=cx.createRadialGradient(hx,hy,0,hx,hy,c.w*5);rg.addColorStop(0,'rgba('+c.h+','+fd.toFixed(2)+')');
rg.addColorStop(.35,'rgba('+c.a+','+(fd*.45).toFixed(2)+')');rg.addColorStop(1,'rgba('+c.a+',0)');
cx.fillStyle=rg;cx.beginPath();cx.arc(hx,hy,c.w*5,0,6.283);cx.fill();return 1})}
if(!rm){if(now>nm){M.push({x:Math.random()*W*.9+W*.1,y:Math.random()*H*.4,t:now});nm=now+4000+Math.random()*6000}
M=M.filter(function(m){var p=(now-m.t)/900;if(p>=1)return 0;
var x=m.x-p*320,y=m.y+p*180,g=cx.createLinearGradient(x,y,x+130,y-73);
g.addColorStop(0,'rgba(255,255,255,'+(1-p).toFixed(2)+')');g.addColorStop(1,'rgba(255,255,255,0)');
cx.strokeStyle=g;cx.lineWidth=1.6;cx.beginPath();cx.moveTo(x,y);cx.lineTo(x+130,y-73);cx.stroke();return 1})}
go()}
$$('.st b').forEach(function(b){var n=parseInt(b.textContent,10),s0=null;if(!n||n>1e6)return;
function step(ts){if(s0===null)s0=ts;var p=Math.min((ts-s0)/900,1);b.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(step)}
b.textContent='0';requestAnimationFrame(step)});
if('IntersectionObserver'in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){
if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{root:app,rootMargin:'0px 0px -5% 0px',threshold:.05});
rs.forEach(function(r){r.classList.add('rv');io.observe(r)})}
window.addEventListener('resize',function(){init();pos()});
document.addEventListener('visibilitychange',go);
init();pos();go();
"""


_FONT_PATHS = (
    "DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "Roboto-Regular.ttf", "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", "NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf", "arial.ttf", "Arial.ttf",
    "/system/fonts/Roboto-Regular.ttf", "/system/fonts/DroidSans.ttf",
)
_FONT_PATHS_BOLD = (
    "DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "Roboto-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/system/fonts/Roboto-Bold.ttf", "arialbd.ttf",
)
_TONES = {"g": (151, 196, 89), "a": (250, 199, 117), "r": (240, 149, 149)}
_PALETTE = ((79, 109, 240), (91, 79, 208), (140, 90, 220), (60, 140, 200), (170, 80, 190))


def _shrink_photo(raw):
    """Avatar -> 64x64 JPEG, quality 55 (about 2 KB instead of ~10 KB); original bytes if Pillow fails"""
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        img.thumbnail((64, 64))
        out = io.BytesIO()
        img.save(out, "JPEG", quality=55)
        return out.getvalue()
    except Exception:
        return raw


def _load_font(paths, size):
    from PIL import ImageFont
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def _clean(text):
    return "".join(c for c in text if ord(c) <= 0xFFFF and not 0x2600 <= ord(c) <= 0x27BF).strip()


def _render_image(title, silent, total, T):
    """One galaxy card as a PNG: every dot is a member, glowing pink dots are the lurkers"""
    import math
    import random
    from PIL import Image, ImageDraw, ImageFilter

    W, H, PAD = 1000, 1200, 44
    count = len(silent)
    percent = count / total * 100 if total else 0
    stale = sum(1 for u in silent if u["stale"])
    new = sum(1 for u in silent if u["new"])
    prem = sum(1 for u in silent if u["premium"])

    f_title, f_sub = _load_font(_FONT_PATHS_BOLD, 38), _load_font(_FONT_PATHS, 22)
    f_big, f_pct = _load_font(_FONT_PATHS_BOLD, 128), _load_font(_FONT_PATHS_BOLD, 50)
    f_lab, f_verd = _load_font(_FONT_PATHS_BOLD, 20), _load_font(_FONT_PATHS_BOLD, 25)
    f_mid, f_small = _load_font(_FONT_PATHS_BOLD, 42), _load_font(_FONT_PATHS, 19)
    PINK, BLUE, MUTED, AMBER = (255, 130, 212), (150, 185, 255), (169, 165, 201), (250, 199, 117)

    base = Image.new("RGBA", (W, H))
    px = ImageDraw.Draw(base)
    for y in range(H):
        k = y / H
        px.line([(0, y), (W, y)], fill=(int(5 + 16 * k), int(5 + 4 * k), int(22 + 30 * k), 255))

    neb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(neb)
    for (nx, ny, nr, col) in ((190, 250, 250, (70, 50, 200, 110)), (830, 560, 280, (170, 40, 160, 85)),
                              (480, 470, 300, (40, 90, 210, 80)), (260, 800, 220, (30, 140, 170, 55))):
        nd.ellipse([nx - nr, ny - nr, nx + nr, ny + nr], fill=col)
    base = Image.alpha_composite(base, neb.filter(ImageFilter.GaussianBlur(95)))

    rnd = random.Random(count * 31 + total)
    draw = ImageDraw.Draw(base, "RGBA")
    for _ in range(300):
        x, y, r = rnd.randrange(W), rnd.randrange(H), rnd.choice((1, 1, 1, 2))
        c = rnd.randrange(110, 235)
        draw.ellipse([x, y, x + r, y + r], fill=(c, c, 255, rnd.randrange(110, 255)))

    flares = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flares)
    for _ in range(9):
        x, y, L = rnd.randrange(40, W - 40), rnd.randrange(130, 820), rnd.randrange(10, 22)
        fd.line([(x - L, y), (x + L, y)], fill=(210, 220, 255, 230), width=2)
        fd.line([(x, y - L), (x, y + L)], fill=(210, 220, 255, 230), width=2)
        fd.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 255, 255, 255))
    base = Image.alpha_composite(base, flares.filter(ImageFilter.GaussianBlur(1.2)))

    gcx, gcy, R, tilt, ang, arms = W // 2, 470, 420, 0.72, math.radians(-28), 3

    def place(rr, th):
        x0, y0 = rr * math.cos(th), rr * math.sin(th) * tilt
        return gcx + x0 * math.cos(ang) - y0 * math.sin(ang), gcy + x0 * math.sin(ang) + y0 * math.cos(ang)

    def spiral(n, spread):
        rr = R * (rnd.random() ** 0.8)
        th = (n % arms) * 2 * math.pi / arms + 4.6 * rr / R + rnd.gauss(0, spread * (0.35 + 0.65 * rr / R))
        return place(rr, th)

    orbit = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(orbit)
    for scale in (0.55, 0.8, 1.04):
        ring = [place(R * scale, a * math.pi / 90) for a in range(181)]
        od.line(ring, fill=(170, 150, 255, 38), width=2)
    base = Image.alpha_composite(base, orbit)

    core = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    cd.ellipse([gcx - 150, gcy - 95, gcx + 150, gcy + 95], fill=(150, 170, 255, 130))
    cd.ellipse([gcx - 55, gcy - 38, gcx + 55, gcy + 38], fill=(255, 235, 220, 150))
    base = Image.alpha_composite(base, core.filter(ImageFilter.GaussianBlur(45)))

    draw = ImageDraw.Draw(base, "RGBA")
    for n in range(800):
        x, y = spiral(n, 0.26)
        draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(150, 170, 255, rnd.randrange(60, 150)))

    dots = min(max(total, 1), 520)
    lurk_n = round(dots * count / total) if total else 0
    if count and not lurk_n:
        lurk_n = 1
    flags = [True] * lurk_n + [False] * (dots - lurk_n)
    rnd.shuffle(flags)
    pts = [spiral(n, 0.20) + (flag,) for n, flag in enumerate(flags)]

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for x, y, lk in pts:
        r = 9 if lk else 6
        gd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 70, 190, 210) if lk else (90, 130, 255, 130))
    base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(6)))

    draw = ImageDraw.Draw(base, "RGBA")
    for x, y, lk in pts:
        if lk:
            draw.ellipse([x - 4.2, y - 4.2, x + 4.2, y + 4.2], fill=PINK + (255,))
            draw.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=(255, 255, 255, 255))
        else:
            draw.ellipse([x - 3.6, y - 3.6, x + 3.6, y + 3.6], fill=BLUE + (255,))
            draw.ellipse([x - 1.4, y - 1.4, x + 1.4, y + 1.4], fill=(235, 242, 255, 255))

    def fit(text, font, width):
        if draw.textlength(text, font=font) <= width:
            return text
        while text and draw.textlength(text + "...", font=font) > width:
            text = text[:-1]
        return text + "..."

    draw.text((PAD, 34), fit(_clean(title) or "-", f_title, W - PAD * 2 - 170), font=f_title, fill=(236, 235, 255, 255))
    draw.text((PAD, 88), f"{T['checked'].format(total)}  ·  {T['date']}", font=f_sub, fill=MUTED + (255,))
    draw.text((W - PAD, 54), "@lceta", font=f_sub, fill=(143, 166, 255, 255), anchor="rm")

    ly = 836
    items = ((T["active"], BLUE), (T["lurkers"], PINK))
    widths = [draw.textlength(t, font=f_small) + 22 for t, _ in items]
    lx = (W - sum(widths) - 36) // 2
    for (t, c), w in zip(items, widths):
        draw.ellipse([lx, ly - 6, lx + 12, ly + 6], fill=c + (255,))
        draw.text((lx + 22, ly), t, font=f_small, fill=MUTED + (255,), anchor="lm")
        lx += w + 36

    box = (PAD, 872, W - PAD, 1160)
    pw_, ph_ = box[2] - box[0], box[3] - box[1]
    glass = base.crop(box).filter(ImageFilter.GaussianBlur(18))
    gm = Image.new("L", (pw_, ph_), 0)
    ImageDraw.Draw(gm).rounded_rectangle([0, 0, pw_ - 1, ph_ - 1], radius=30, fill=255)
    base.paste(glass, (box[0], box[1]), gm)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=30, fill=(18, 14, 46, 175), outline=(175, 155, 255, 95), width=2)
    base = Image.alpha_composite(base, ov).convert("RGB")
    draw = ImageDraw.Draw(base, "RGBA")

    lx0 = box[0] + 36
    draw.text((lx0, 902), T["lurkers"].upper(), font=f_lab, fill=PINK + (255,))
    num, pct = str(count), f"{percent:.1f}%"
    draw.text((lx0 - 4, 1034), num, font=f_big, fill=(255, 255, 255, 255), anchor="ls")
    draw.text((lx0 + draw.textlength(num, font=f_big) + 22, 1034), pct, font=f_pct, fill=(143, 166, 255, 255), anchor="ls")

    bx0, bx1, by = lx0, lx0 + 470, 1062
    draw.rounded_rectangle([bx0, by, bx1, by + 12], radius=6, fill=(255, 255, 255, 32))
    if count:
        fill_w = max(12, int((bx1 - bx0) * min(percent, 100) / 100))
        bar = Image.new("RGBA", (fill_w, 12), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bar)
        for x in range(fill_w):
            t = x / max(1, fill_w - 1)
            bd.line([(x, 0), (x, 12)], fill=(int(79 + 176 * t), int(109 + 1 * t), int(240 - 28 * t), 255))
        bm = Image.new("L", (fill_w, 12), 0)
        ImageDraw.Draw(bm).rounded_rectangle([0, 0, fill_w - 1, 11], radius=6, fill=255)
        base.paste(bar.convert("RGB"), (bx0, by), bm)
        draw = ImageDraw.Draw(base, "RGBA")

    vw = draw.textlength(T["verdict"], font=f_verd) + 44
    draw.rounded_rectangle([lx0, 1094, lx0 + vw, 1136], radius=21, fill=AMBER + (34,), outline=AMBER + (170,), width=2)
    draw.text((lx0 + vw / 2, 1115), T["verdict"], font=f_verd, fill=AMBER + (255,), anchor="mm")

    sx = box[0] + 560
    draw.line([(sx - 30, 902), (sx - 30, 1130)], fill=(175, 155, 255, 70), width=2)
    rows = ((T["stale"], stale, _TONES["r"]), (T["new"], new, _TONES["g"]), (T["premium"], prem, _TONES["a"]))
    for k, (label, value, col) in enumerate(rows):
        y = 898 + k * 76
        draw.ellipse([sx, y + 6, sx + 12, y + 18], fill=col + (255,))
        draw.text((sx + 24, y + 12), fit(label, f_small, 300), font=f_small, fill=MUTED + (255,), anchor="lm")
        draw.text((sx, y + 26), str(value), font=f_mid, fill=col + (255,))
        share = f"{value / count * 100:.0f}%" if count else "0%"
        draw.text((sx + draw.textlength(str(value), font=f_mid) + 14, y + 62), share, font=f_small, fill=MUTED + (255,), anchor="lm")

    buf = io.BytesIO()
    base.convert("RGB").save(buf, "JPEG", quality=80)
    buf.name = "silent_users.jpg"
    buf.seek(0)
    return buf


@loader.tds
class CMCMod(loader.Module):
    """Message, media and user statistics for chats"""

    strings = {
        "name": "CMC",
        "_cls_doc": "Count messages, media and user stats in a chat",
        "upd_checking": "Checking for updates...",
        "upd_downloading": "Updating CMC...",
        "upd_done": "CMC updated successfully!",
        "upd_none": "You already have the latest version.",
        "upd_none_force": "You already have the latest version. Update anyway?",
        "upd_force_btn": "↻ Update anyway",
        "upd_cancel_btn": "✖ Cancel",
        "upd_fail": "Update failed. Check the logs.",
        "upd_fetch_fail": "Could not reach the update source. Try again later.",
        "upd_busy": "An update check/install is already running. Try again in a bit.",
        "busy": "Already working in this chat, please wait for the current command to finish.",
        "cfg_chat": "Group ID (e.g. -1001234567890) to send a copy of the .silent file to",
        "cfg_topic": "Topic ID in that group (General = 1)",
        "cfg_photos": "Embed avatars into the .silent HTML report (the file gets heavier)",
        "cfg_music_folder": "GitHub folder with tracks (github.com/user/repo/tree/branch/folder): every audio file in it is picked up automatically",
        "cfg_music": "Backup direct mp3 links (used if the folder is empty or unreachable); if there are no tracks at all, the music button is hidden",
        "this_chat": "this chat",
        "this_channel": "this channel",
        "my_wait": "Counting your messages...\nThis may take a while.",
        "my_head": "Your stats in <u>'{}'</u>:",
        "user_wait": "Counting messages of {}...",
        "user_head": "Stats of {} in <u>'{}'</u>:",
        "user_nf": "User not found. Check the @username or ID.",
        "user_args": "Specify a @username or ID, or reply to the user's message.",
        "all_wait": "Counting messages of all users in <u>'{}'</u>...\nThis may take a while.",
        "all_head": "Message stats in <u>'{}'</u>:",
        "all_unit": "messages",
        "no_part": "Could not get the chat members.",
        "chat_wait": "Collecting stats of <u>'{}'</u>...",
        "chat_head": "Chat stats of <u>'{}'</u>:",
        "l_total_messages": "Total messages",
        "l_total_media": "Total media",
        "l_stickers": "Stickers",
        "l_gifs": "GIF",
        "l_photos": "Photos",
        "l_videos": "Videos",
        "l_voice": "Voice messages",
        "l_documents": "Files",
        "l_photo_video": "Photos/videos",
        "l_total_members": "Members",
        "l_admins": "Admins",
        "l_deleted_accounts": "Deleted accounts",
        "silent_wait": "Looking for lurkers in <u>'{}'</u>...",
        "silent_prog": "Looking for lurkers in <u>'{}'</u>...\nChecked: {}/{}, found: {}",
        "silent_none": "No lurkers in <u>'{}'</u>!",
        "silent_photos": "Found lurkers: {}. Loading avatars...",
        "cap_head": "Lurkers in <u>'{}'</u>",
        "cap_total": "Total lurkers: <b>{}</b> (checked: {})",
        "copy_err": "CMC: failed to send a copy of the file to the group: {}",
        "file_fb_group": "Files can't be sent to this chat. The report was sent to the configured group.",
        "file_fb_me": "Files can't be sent to this chat. The report was sent to your Saved Messages.",
        "file_fb_fail": "Files can't be sent to this chat and the report could not be delivered elsewhere: {}",
        "img_v1": "A lively chat",
        "img_v2": "A quiet harbor",
        "img_v3": "Cosmic silence",
        "img_v4": "A black hole",
        "img_active": "Active",
        "no_name": "No name",
        "s_online": "online",
        "s_long": "long ago",
        "s_today": "today",
        "s_yday": "yesterday",
        "s_days": "{} d. ago",
        "s_weeks": "{} w. ago",
        "s_months": "{} mo. ago",
        "s_years": "{} y. ago",
        "s_recent": "recently",
        "s_week": "last week",
        "s_month": "last month",
        "lang": "en",
        "r_title": "Lurkers — {}",
        "r_over": "Lurkers report",
        "r_h1": "Lurkers",
        "r_checked": "checked {}",
        "r_lurkers": "Lurkers",
        "r_stale": "Inactive 30+ days",
        "r_chart": "By join date",
        "r_chart_unit": "lurkers",
        "r_joined": "joined {}",
        "r_search": "Search by name or @username",
        "r_empty": "Nothing found",
        "r_note": "“Newcomers” joined within the last 30 days. If a person hides their last seen time, "
                  "“recently”, “last week” or “last month” is shown instead of a date.",
        "r_sig": "Design by",
        "f_all": "All",
        "f_old": "Long inactive",
        "f_nw": "Newcomers",
        "f_pr": "Premium",
        "b_sel": "Select visible",
        "b_unsel": "Deselect",
        "b_copy": "Copy usernames",
        "b_csv": "Download CSV",
        "b_music": "Music",
        "m_of": "Track {0} of {1}",
        "b_pick": "Select people first",
        "b_done": "Copied",
        "c_name": "Name",
        "c_user": "Username",
        "c_id": "ID",
        "c_joined": "Joined",
        "c_seen": "Last seen",
        "c_prem": "Premium",
        "c_yes": "yes",
    }

    strings_ru = {
        "_cls_doc": "Подсчет сообщений, медиа и статистики пользователей в чате",
        "upd_checking": "Проверяю обновления...",
        "upd_downloading": "Обновляю CMC...",
        "upd_done": "CMC успешно обновлён!",
        "upd_none": "У вас уже последняя версия.",
        "upd_none_force": "У вас уже последняя версия. Всё равно обновить?",
        "upd_force_btn": "↻ Обновить всё равно",
        "upd_cancel_btn": "✖ Отмена",
        "upd_fail": "Не удалось обновить. Проверьте логи.",
        "upd_fetch_fail": "Не удалось связаться с источником обновлений. Попробуйте позже.",
        "upd_busy": "Проверка или установка обновления уже идёт. Попробуйте чуть позже.",
        "busy": "В этом чате уже идёт подсчёт, дождитесь завершения текущей команды.",
        "cfg_chat": "ID группы (например -1001234567890), куда дублировать файл .silent",
        "cfg_topic": "ID топика в этой группе (General = 1)",
        "cfg_photos": "Вставлять аватарки в HTML-отчёт .silent (файл станет тяжелее)",
        "cfg_music_folder": "Папка на GitHub с треками (github.com/user/repo/tree/ветка/папка): все аудиофайлы из неё подхватываются сами",
        "cfg_music": "Запасные прямые ссылки на mp3 (если папка пуста или недоступна); если треков нет совсем, кнопка музыки скрывается",
        "this_chat": "этот чат",
        "this_channel": "этот канал",
        "my_wait": "Начинаю подсчет ваших сообщений...\nЭто может занять некоторое время.",
        "my_head": "Ваша статистика в <u>'{}'</u>:",
        "user_wait": "Начинаю подсчет сообщений пользователя {}...",
        "user_head": "Статистика {} в <u>'{}'</u>:",
        "user_nf": "Не удалось найти пользователя. Убедитесь, что вы ввели правильный @username или ID.",
        "user_args": "Пожалуйста, укажите @username, ID или сделайте реплай на сообщение пользователя.",
        "all_wait": "Начинаю подсчет сообщений всех пользователей в <u>'{}'</u>...\nЭто может занять некоторое время.",
        "all_head": "Статистика сообщений в <u>'{}'</u>:",
        "all_unit": "сообщений",
        "no_part": "Не удалось получить участников чата.",
        "chat_wait": "Собираю статистику чата <u>'{}'</u>...",
        "chat_head": "Статистика чата <u>'{}'</u>:",
        "l_total_messages": "Всего сообщений",
        "l_total_media": "Всего медиаконтента",
        "l_stickers": "Стикеров",
        "l_gifs": "GIF",
        "l_photos": "Фото",
        "l_videos": "Видео",
        "l_voice": "Голосовых",
        "l_documents": "Файлов",
        "l_photo_video": "Фото/видео",
        "l_total_members": "Участников",
        "l_admins": "Администраторов",
        "l_deleted_accounts": "Удаленных аккаунтов",
        "silent_wait": "Ищу молчунов в <u>'{}'</u>...",
        "silent_prog": "Ищу молчунов в <u>'{}'</u>...\nПроверено: {}/{}, найдено: {}",
        "silent_none": "Нет молчунов в <u>'{}'</u>!",
        "silent_photos": "Нашёл молчунов: {}. Загружаю аватарки...",
        "cap_head": "Молчуны в <u>'{}'</u>",
        "cap_total": "Всего молчунов: <b>{}</b> (проверено: {})",
        "copy_err": "CMC: не удалось продублировать файл в General: {}",
        "file_fb_group": "В этот чат нельзя отправлять файлы. Отчёт отправлен в указанную группу.",
        "file_fb_me": "В этот чат нельзя отправлять файлы. Отчёт отправлен в Избранное.",
        "file_fb_fail": "В этот чат нельзя отправлять файлы, и отчёт не удалось доставить в другое место: {}",
        "img_v1": "Живой чат",
        "img_v2": "Тихая гавань",
        "img_v3": "Космическая тишина",
        "img_v4": "Чёрная дыра",
        "img_active": "Активные",
        "no_name": "Без имени",
        "s_online": "в сети",
        "s_long": "давно",
        "s_today": "сегодня",
        "s_yday": "вчера",
        "s_days": "{} дн. назад",
        "s_weeks": "{} нед. назад",
        "s_months": "{} мес. назад",
        "s_years": "{} г. назад",
        "s_recent": "недавно",
        "s_week": "на этой неделе",
        "s_month": "в этом месяце",
        "lang": "ru",
        "r_title": "Молчуны — {}",
        "r_over": "Отчёт о молчунах",
        "r_h1": "Молчуны",
        "r_checked": "проверено {}",
        "r_lurkers": "Молчунов",
        "r_stale": "Не заходили 30+ дн.",
        "r_chart": "По времени вступления",
        "r_chart_unit": "молчуны",
        "r_joined": "вступил {}",
        "r_search": "Поиск по имени или @username",
        "r_empty": "Ничего не найдено",
        "r_note": "«Новички» — вступили за последние 30 дней. Если человек скрыл время захода, "
                  "вместо даты показывается «недавно», «на этой неделе» или «в этом месяце».",
        "r_sig": "Автор дизайна",
        "f_all": "Все",
        "f_old": "Давно не заходили",
        "f_nw": "Новички",
        "f_pr": "Premium",
        "b_sel": "Выбрать видимых",
        "b_unsel": "Снять выбор",
        "b_copy": "Скопировать ники",
        "b_csv": "Скачать CSV",
        "b_music": "Музыка",
        "m_of": "Трек {0} из {1}",
        "b_pick": "Сначала отметьте людей",
        "b_done": "Скопировано",
        "c_name": "Имя",
        "c_user": "Username",
        "c_id": "ID",
        "c_joined": "Вступил",
        "c_seen": "Был(а) в сети",
        "c_prem": "Premium",
        "c_yes": "да",
    }

    def __init__(self):
        self._silent_cache = {}
        self._tracks_cache = None
        self._busy = set()
        self._update_lock = asyncio.Lock()
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "report_chat", None, lambda: self.strings("cfg_chat"),
                validator=loader.validators.Union(
                    loader.validators.Integer(),
                    loader.validators.String(),
                    loader.validators.NoneType(),
                ),
            ),
            loader.ConfigValue(
                "report_topic", 1, lambda: self.strings("cfg_topic"),
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "report_photos", True, lambda: self.strings("cfg_photos"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "music_folder",
                "https://github.com/lcetaa/CMC-heroku-bot/tree/main/music",
                lambda: self.strings("cfg_music_folder"),
                validator=loader.validators.Union(
                    loader.validators.Link(),
                    loader.validators.NoneType(),
                ),
            ),
            loader.ConfigValue(
                "music_urls",
                [
                    "https://lcetaa.github.io/CMC-heroku-bot/music/SM-HARDTEKK-SLOWED.mp3",
                    "https://lcetaa.github.io/CMC-heroku-bot/music/MAMA-MA-Sped-Up.mp3",
                ],
                lambda: self.strings("cfg_music"),
                validator=loader.validators.Series(validator=loader.validators.Link()),
            ),
        )

    async def client_ready(self, client, db):
        self._client = client
        self._me = await client.get_me()

    async def on_unload(self):
        self._silent_cache.clear()
        self._busy.clear()

    async def _get_tracks(self):
        """All audio files from the GitHub folder (cached), else the manual links"""
        manual = [str(u) for u in (self.config["music_urls"] or [])]
        folder = self.config["music_folder"]
        if not folder:
            return manual
        folder = str(folder)
        cached = self._tracks_cache
        if cached and cached[2] == folder and time.time() - cached[0] < MUSIC_TTL:
            return cached[1]
        m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+?)/?$", folder)
        if not m:
            return manual
        owner, repo, branch, path = m.groups()
        api = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
        base = f"https://{owner}.github.io/{repo}/{path}/"
        tracks = []
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=8),
                headers={"Accept": "application/vnd.github+json", "User-Agent": "CMC-module"},
            ) as ses:
                async with ses.get(api) as r:
                    if r.status != 200:
                        logger.warning("music folder: GitHub API answered %s", r.status)
                    if r.status == 200:
                        data = await r.json()
                        tracks = [
                            base + _quote(f["name"])
                            for f in data
                            if f.get("type") == "file" and f["name"].lower().endswith(MUSIC_EXT)
                        ]
        except Exception as e:
            logger.warning("music folder fetch failed: %s", e)
        if tracks:
            self._tracks_cache = (time.time(), tracks, folder)
            return tracks
        if cached and cached[2] == folder:
            return cached[1]
        return manual

    async def _guard(self, message, run):
        """One heavy command per chat at a time"""
        key = utils.get_chat_id(message)
        if key in self._busy:
            return await utils.answer(message, self.strings("busy"))
        self._busy.add(key)
        try:
            await run(message)
        finally:
            self._busy.discard(key)


    async def _ctx(self, message):
        """(chat_id, is_private, title) of the chat the command was sent in"""
        chat_id = message.peer_id
        chat = await self._client.get_entity(chat_id)
        private = chat_id == self._me.id or getattr(chat, "first_name", None) is not None
        title = getattr(chat, "title", None) or self.strings("this_chat" if private else "this_channel")
        return chat_id, private, title

    async def _search(self, chat_id, flt=None, from_id=None, limit=0, offset_id=0):
        return await self._client(hikkatl.functions.messages.SearchRequest(
            peer=chat_id, q="", filter=flt or hikkatl.types.InputMessagesFilterEmpty(),
            min_date=None, max_date=None, offset_id=offset_id, add_offset=0, limit=limit,
            max_id=0, min_id=0, from_id=from_id, hash=0,
        ))

    async def _count(self, chat_id, flt):
        return getattr(await self._search(chat_id, flt), "count", 0) or 0

    @staticmethod
    def _mention(user):
        return f"@{user.username}" if user.username else f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    def _lines(self, stats, keys, nested=()):
        return "\n".join(
            f"{'└ ' if k in nested else ''}{EMO[k]} {self.strings('l_' + k)}: <b>{stats[k]}</b>" for k in keys
        )

    async def get_chat_participants(self, chat_id):
        """All chat members (aggressive mode bypasses the 10k limit)"""
        try:
            return await self._client.get_participants(chat_id, limit=None, aggressive=True)
        except Exception:
            return await self._client.get_participants(chat_id)

    async def get_message_stats(self, chat_id, user_id, is_private=False):
        """Messages and media count of a user (chats and DMs)"""
        stats = dict.fromkeys(USER_KEYS, 0)
        try:
            total = (await self._search(chat_id, from_id=user_id)).count
        except Exception:
            total = 0

        offset_id = collected = 0
        while collected < total:
            if is_private:
                messages = (await self._client(hikkatl.functions.messages.GetHistoryRequest(
                    peer=chat_id, offset_id=offset_id, offset_date=None, add_offset=0,
                    limit=100, max_id=0, min_id=0, hash=0,
                ))).messages
            else:
                messages = (await self._search(chat_id, from_id=user_id, limit=100, offset_id=offset_id)).messages
            if not messages:
                break
            for msg in messages:
                if getattr(msg.from_id, "user_id", msg.from_id) == user_id:
                    collected += 1
                    for attr, key in MEDIA:
                        if getattr(msg, attr, None):
                            stats[key] += 1
                            stats["total_media"] += 1
                            break
            offset_id = messages[-1].id

        stats["total_messages"] = total
        return stats

    async def get_chat_total_stats(self, chat_id):
        """Whole-chat statistics"""
        parts = await self.get_chat_participants(chat_id)
        stats = {
            "total_members": len(parts),
            "deleted_accounts": sum(1 for u in parts if getattr(u, "deleted", False)),
        }
        try:
            full = await self._client(hikkatl.functions.channels.GetFullChannelRequest(chat_id))
            stats["total_members"] = getattr(full.full_chat, "participants_count", None) or stats["total_members"]
        except Exception:
            pass
        try:
            stats["admins"] = len(await self._client.get_participants(
                chat_id, filter=hikkatl.types.ChannelParticipantsAdmins()))
        except Exception:
            stats["admins"] = sum(
                1 for u in parts if u.participant and getattr(u.participant, "admin_rights", None))

        T = hikkatl.types
        for key, flt in (
            ("total_messages", T.InputMessagesFilterEmpty()),
            ("photo_video", T.InputMessagesFilterPhotoVideo()),
            ("gifs", T.InputMessagesFilterGif()),
            ("voice", T.InputMessagesFilterVoice()),
            ("documents", T.InputMessagesFilterDocument()),
        ):
            stats[key] = await self._count(chat_id, flt)
        return stats

    @loader.command(ru_doc="- ваши сообщения и медиа", en_doc="- your messages and media")
    @loader.unrestricted
    async def mymsg(self, message):
        await self._guard(message, self._mymsg_run)

    async def _mymsg_run(self, message):
        """- your messages and media"""
        chat_id, private, title = await self._ctx(message)
        await utils.answer(message, self.strings("my_wait"))
        stats = await self.get_message_stats(chat_id, self._me.id, private)
        await utils.answer(
            message,
            f"{E_USER} {self.strings('my_head').format(title)}\n\n"
            + self._lines(stats, USER_KEYS, USER_KEYS[2:]),
        )

    @loader.command(ru_doc="- сообщения юзера (реплай или @username)", en_doc="- user's messages (reply or @username)")
    @loader.unrestricted
    async def usermsg(self, message):
        await self._guard(message, self._usermsg_run)

    async def _usermsg_run(self, message):
        """- user's messages (reply or @username)"""
        args = utils.get_args_raw(message)
        chat_id, private, title = await self._ctx(message)

        if message.is_reply:
            user = await self._client.get_entity((await message.get_reply_message()).sender_id)
        elif args:
            try:
                user = await self._client.get_entity(args)
            except Exception:
                return await utils.answer(message, self.strings("user_nf"))
        else:
            return await utils.answer(message, self.strings("user_args"))

        name = self._mention(user)
        await utils.answer(message, self.strings("user_wait").format(name))
        stats = await self.get_message_stats(chat_id, user.id, private)
        await utils.answer(
            message,
            f"{E_USER} {self.strings('user_head').format(name, title)}\n\n"
            + self._lines(stats, USER_KEYS, USER_KEYS[2:]),
        )

    @loader.command(ru_doc="- сообщения всех участников", en_doc="- messages of all members")
    @loader.unrestricted
    async def allmsg(self, message):
        await self._guard(message, self._allmsg_run)

    async def _allmsg_run(self, message):
        """- messages of all members"""
        chat_id, _, title = await self._ctx(message)
        await utils.answer(message, self.strings("all_wait").format(title))

        participants = await self.get_chat_participants(chat_id)
        if not participants:
            return await utils.answer(message, self.strings("no_part"))

        counts = []
        for user in participants:
            if user.deleted:
                continue
            try:
                n = (await self._search(chat_id, from_id=user.id)).count
            except Exception:
                n = 0
            if n > 0:
                counts.append((self._mention(user), n))
        counts.sort(key=lambda x: x[1], reverse=True)

        unit = self.strings("all_unit")
        await utils.answer(
            message,
            self.strings("all_head").format(title) + "\n\n"
            + "".join(f"{E_USER} {name}: {E_MSG}<b>{n}</b> {unit}\n" for name, n in counts),
        )

    @loader.command(ru_doc="- статистика чата", en_doc="- chat statistics")
    @loader.unrestricted
    async def chatstats(self, message):
        await self._guard(message, self._chatstats_run)

    async def _chatstats_run(self, message):
        """- chat statistics"""
        chat_id, _, title = await self._ctx(message)
        await utils.answer(message, self.strings("chat_wait").format(title))
        s = await self.get_chat_total_stats(chat_id)
        await utils.answer(
            message,
            f"{EMO['total_media']} {self.strings('chat_head').format(title)}\n\n"
            + self._lines(s, ("total_members", "admins", "deleted_accounts"), ("admins", "deleted_accounts"))
            + "\n\n"
            + self._lines(s, ("total_messages", "photo_video", "gifs", "voice", "documents"),
                          ("photo_video", "gifs", "voice", "documents")),
        )

    @loader.command(ru_doc="- молчуны + HTML-отчёт", en_doc="- lurkers + HTML report")
    @loader.unrestricted
    async def silent(self, message):
        await self._guard(message, self._silent_run)

    async def _silent_run(self, message):
        """- lurkers + HTML report"""
        S = self.strings
        chat_id, _, title = await self._ctx(message)

        key = (str(chat_id), bool(self.config["report_photos"]))
        cached = self._silent_cache.get(key)
        if cached and time.monotonic() - cached[0] < 900:
            silent, total = cached[1], cached[2]
        else:
            await utils.answer(message, S("silent_wait").format(title))
            participants = [
                u for u in await self.get_chat_participants(chat_id)
                if not getattr(u, "deleted", False) and not getattr(u, "bot", False)
            ]
            total = len(participants)
            silent, now_utc = [], datetime.now(timezone.utc)

            for checked, user in enumerate(participants, 1):
                while True:
                    try:
                        if (await self._search(chat_id, from_id=user.id, limit=1)).count == 0:
                            silent.append(self._silent_info(user, now_utc))
                        break
                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds + 1)
                    except Exception:
                        break
                if checked % 300 == 0:
                    try:
                        await utils.answer(message, S("silent_prog").format(title, checked, total, len(silent)))
                    except Exception:
                        pass
                await asyncio.sleep(0.05)

            if silent and self.config["report_photos"]:
                try:
                    await utils.answer(message, S("silent_photos").format(len(silent)))
                except Exception:
                    pass
                await self._load_photos({u.id: u for u in participants}, silent)

            now = time.monotonic()
            self._silent_cache = {k: v for k, v in self._silent_cache.items() if now - v[0] < 900}
            self._silent_cache[key] = (now, silent, total)

        if not silent:
            return await utils.answer(message, f"{E_NOTE} {S('silent_none').format(title)}")

        tracks = await self._get_tracks()
        data = io.BytesIO(self._build_silent_report(title, silent, total, tracks).encode("utf-8"))
        data.name = "silent_users.html"
        caption = (
            f"{EMO['total_members']} {S('cap_head').format(title)}\n"
            f"{E_NOTE} {S('cap_total').format(len(silent), total)}"
        )
        try:
            await self._client.send_file(
                chat_id, data, caption=caption, parse_mode="html",
                reply_to=self._topic(message), force_document=True,
            )
        except Exception:
            if await self._send_images(message, chat_id, title, silent, total, caption):
                await self._send_copy(data, caption)
                return
            if await self._send_copy(data, caption):
                note = S("file_fb_group")
            else:
                try:
                    data.seek(0)
                    await self._client.send_file("me", data, caption=caption, parse_mode="html")
                    note = S("file_fb_me")
                except Exception as e:
                    note = S("file_fb_fail").format(_html.escape(str(e)))
            return await utils.answer(message, f"{E_NOTE} {note}")
        try:
            await message.delete()
        except Exception:
            pass
        await self._send_copy(data, caption)

    async def _get_local_source(self):
        """Source code of the currently loaded module (via loader or inspect)"""
        import inspect
        import sys
        mod = sys.modules.get(self.__class__.__module__)
        ldr_obj = getattr(mod, "__loader__", None)
        if ldr_obj and hasattr(ldr_obj, "get_source"):
            try:
                src = ldr_obj.get_source(self.__class__.__module__)
                if src:
                    return src
            except Exception as e:
                logger.debug("Failed to get the source via __loader__.get_source(): %s", e)
        if mod:
            try:
                return inspect.getsource(mod)
            except Exception as e:
                logger.debug("Failed to get the source via inspect.getsource(): %s", e)
        return None

    async def _fetch_remote_source(self):
        """Download the latest module code from GitHub (raw). Bytes or None on error"""
        try:
            headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
                async with session.get(f"{UPDATE_URL}?_={int(time.time())}", headers=headers) as resp:
                    if resp.status != 200:
                        logger.warning("Update: server returned status %s", resp.status)
                        return None
                    return await resp.read()
        except Exception as e:
            logger.warning("Update: failed to download the source: %s", e)
            return None

    async def _check_update_hashes(self):
        """(differs: bool | None, remote_ok: bool)"""
        remote = await self._fetch_remote_source()
        if not remote:
            return None, False
        local = await self._get_local_source()
        if not local:
            logger.warning("Update: no local source hash, assuming they differ")
            return True, True
        return hashlib.sha256(remote).hexdigest() != hashlib.sha256(local.encode("utf-8")).hexdigest(), True

    async def _safe_install_update(self):
        """Install the fresh module version via the Loader"""
        ldr = self.lookup("Loader")
        if not ldr or not hasattr(ldr, "download_and_install"):
            logger.error("Update: the Loader module is unavailable")
            return False
        try:
            res = await asyncio.wait_for(ldr.download_and_install(UPDATE_URL), timeout=UPDATE_INSTALL_TIMEOUT)
            if getattr(ldr, "fully_loaded", False):
                ldr.update_modules_in_db()
            return res == 1
        except asyncio.TimeoutError:
            logger.warning("Update: install timed out (%s sec)", UPDATE_INSTALL_TIMEOUT)
            return False
        except Exception as e:
            logger.warning("Update: install failed: %s", e)
            return False

    async def _upd_force_cb(self, call):
        S = self.strings
        try:
            await call.answer()
            await call.edit(f"🔄 <b>{S('upd_downloading')}</b>")
        except Exception as e:
            logger.debug("Update form: %s", e)
        ok = await self._safe_install_update()
        try:
            await call.edit(f"✅ <b>{S('upd_done')}</b>" if ok else f"❌ <b>{S('upd_fail')}</b>")
        except Exception as e:
            logger.debug("Update form: %s", e)

    async def _upd_cancel_cb(self, call):
        try:
            await call.delete()
        except Exception as e:
            logger.debug("Update form: %s", e)

    @loader.command(
        ru_doc="[-f|--force] - проверить и установить обновление модуля",
        en_doc="[-f|--force] - check for and install a module update",
    )
    async def cmcupdate(self, message):
        S = self.strings
        args = utils.get_args_raw(message)
        force = "-f" in args or "--force" in args
        m = await utils.answer(message, f"🔄 <b>{S('upd_downloading') if force else S('upd_checking')}</b>")
        try:
            await asyncio.wait_for(self._update_lock.acquire(), timeout=UPDATE_LOCK_WAIT)
        except asyncio.TimeoutError:
            return await m.edit(f"❌ <b>{S('upd_busy')}</b>")
        try:
            if force:
                ok = await self._safe_install_update()
                return await m.edit(f"✅ <b>{S('upd_done')}</b>" if ok else f"❌ <b>{S('upd_fail')}</b>")
            differs, remote_ok = await self._check_update_hashes()
            if not remote_ok:
                return await m.edit(f"❌ <b>{S('upd_fetch_fail')}</b>")
            if not differs:
                try:
                    await self.inline.form(
                        text=f"✅ <b>{S('upd_none_force')}</b>", message=m,
                        reply_markup=[[
                            {"text": S("upd_force_btn"), "callback": self._upd_force_cb},
                            {"text": S("upd_cancel_btn"), "callback": self._upd_cancel_cb},
                        ]],
                    )
                except Exception:
                    await m.edit(f"✅ <b>{S('upd_none')}</b>")
                return
            await m.edit(f"🔄 <b>{S('upd_downloading')}</b>")
            ok = await self._safe_install_update()
            await m.edit(f"✅ <b>{S('upd_done')}</b>" if ok else f"❌ <b>{S('upd_fail')}</b>")
        finally:
            self._update_lock.release()

    @staticmethod
    def _topic(message):
        """Forum topic id of the command message, or None"""
        rt = getattr(message, "reply_to", None)
        if getattr(rt, "forum_topic", False):
            return getattr(rt, "reply_to_top_id", None) or getattr(rt, "reply_to_msg_id", None)
        return None


    async def _load_photos(self, users_by_id, silent_users):
        """Download tiny low-quality avatars of the lurkers in parallel and embed them as base64"""
        loop = asyncio.get_running_loop()
        sem = asyncio.Semaphore(10)

        async def load(info):
            user = users_by_id.get(info["id"])
            if user is None or not getattr(user, "photo", None):
                return
            async with sem:
                for _ in range(3):
                    try:
                        raw = await self._client.download_profile_photo(user, file=bytes, download_big=False)
                        if raw:
                            raw = await loop.run_in_executor(None, _shrink_photo, raw)
                            info["photo"] = base64.b64encode(raw).decode()
                        return
                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds + 1)
                    except Exception:
                        return

        await asyncio.gather(*(load(info) for info in silent_users))

    async def _send_images(self, message, chat_id, title, silent, total, caption):
        """Fallback when files are forbidden: send a summary card as one photo"""
        S = self.strings
        pct = len(silent) / total * 100 if total else 0
        try:
            texts = {
                "checked": S("r_checked"), "lurkers": S("r_lurkers"), "stale": S("r_stale"),
                "new": S("f_nw"), "premium": S("f_pr"), "active": S("img_active"),
                "date": datetime.now().strftime("%d.%m.%Y"),
                "verdict": S("img_v%d" % (1 if pct < 15 else 2 if pct < 35 else 3 if pct < 60 else 4)),
            }
            image = await asyncio.get_running_loop().run_in_executor(
                None, _render_image, title, silent, total, texts,
            )
            await self._client.send_file(
                chat_id, image, caption=caption, parse_mode="html",
                reply_to=self._topic(message), force_document=False,
            )
        except Exception:
            return False
        try:
            await message.delete()
        except Exception:
            pass
        return True

    async def _send_copy(self, data, caption):
        """Send a copy of the report to the General topic of the configured group"""
        target = self.config["report_chat"]
        if not target:
            return False
        try:
            if isinstance(target, str) and target.lstrip("-").isdigit():
                target = int(target)
            data.seek(0)
            topic = self.config["report_topic"] or None
            await self._client.send_file(
                target, data, caption=caption,
                reply_to=topic if topic and topic > 1 else None, parse_mode="html",
            )
            return True
        except Exception as e:
            await self._client.send_message("me", self.strings("copy_err").format(_html.escape(str(e))))
            return False

    def _seen_info(self, user, now):
        """(label, colour, inactive 30+ days) from the user's last-seen status"""
        S = self.strings
        status = getattr(user, "status", None)
        st = type(status).__name__
        if st == "UserStatusOnline":
            return S("s_online"), "g", False
        if st == "UserStatusOffline":
            was = getattr(status, "was_online", None)
            if was is None:
                return S("s_long"), "r", True
            if was.tzinfo is None:
                was = was.replace(tzinfo=timezone.utc)
            days = max((now - was).days, 0)
            if days == 0:
                return S("s_today"), "g", False
            if days == 1:
                return S("s_yday"), "g", False
            if days < 7:
                return S("s_days").format(days), "g", False
            if days < 30:
                return S("s_weeks").format(days // 7), "a", False
            if days < 365:
                return S("s_months").format(days // 30), "r", True
            return S("s_years").format(days // 365), "r", True
        if st == "UserStatusRecently":
            return S("s_recent"), "g", False
        if st == "UserStatusLastWeek":
            return S("s_week"), "a", False
        if st == "UserStatusLastMonth":
            return S("s_month"), "a", False
        return S("s_long"), "r", True

    def _silent_info(self, user, now):
        """Lurker data taken from the already fetched member list (no extra requests)"""
        joined = getattr(getattr(user, "participant", None), "date", None)
        if joined is not None and joined.tzinfo is None:
            joined = joined.replace(tzinfo=timezone.utc)
        seen, tone, stale = self._seen_info(user, now)
        return {
            "username": user.username,
            "name": user.first_name or self.strings("no_name"),
            "id": user.id,
            "joined": joined,
            "seen": seen,
            "tone": tone,
            "stale": stale,
            "new": bool(joined and (now - joined).days <= 30),
            "premium": bool(getattr(user, "premium", False)),
        }

    def _build_silent_report(self, chat_title, silent_users, total, tracks=None):
        """HTML report: search, filters, selection, username copy, CSV"""
        S, esc = self.strings, _html.escape
        count = len(silent_users)
        percent = (count / total * 100) if total else 0
        stale_count = sum(1 for u in silent_users if u["stale"])
        palette = ["blue", "green", "amber", "red", "purple"]

        rows = []
        for i, u in enumerate(silent_users, 1):
            name, username, uid = u["name"], u["username"], u["id"]
            chars = re.findall(r"[^\W_]", name) or re.findall(r"[^\W_]", username or "")
            initials = esc("".join(chars[:2]).upper() or "?")
            sub = [f"@{esc(username)}" if username else f"ID {uid}"]
            joined = u["joined"].strftime("%m.%Y") if u["joined"] else ""
            if joined:
                sub.append(S("r_joined").format(joined))
            if u["premium"]:
                sub.append("Premium")
            subhtml = sub[0] + ("<br>" + " · ".join(sub[1:]) if len(sub) > 1 else "")
            link = f"https://t.me/{esc(username)}" if username else f"tg://user?id={uid}"
            search = esc(f"{name} {username or ''} {uid}".lower())
            if u.get("photo"):
                av = f'<span class="av"><img alt="" src="data:image/jpeg;base64,{u["photo"]}"></span>'
            else:
                av = f'<span class="av {palette[i % len(palette)]}">{initials}</span>'
            rows.append(
                f'<div class="row" data-s="{search}" data-old="{int(u["stale"])}" '
                f'data-nw="{int(u["new"])}" data-pr="{int(u["premium"])}" '
                f'data-n="{esc(name)}" data-u="{esc(username or "")}" data-id="{uid}" '
                f'data-j="{joined}" data-l="{esc(u["seen"])}">'
                f'<input type="checkbox" class="cb"><a class="who" href="{link}">{av}'
                f'<span class="info"><b>{esc(name)}</b><small>{subhtml}</small></span></a>'
                f'<span class="bd {u["tone"]}">{esc(u["seen"])}</span></div>'
            )

        chart = ""
        dates = [u["joined"] for u in silent_users if u["joined"]]
        if dates:
            by_year = len({d.year for d in dates}) > 1
            cnt = {}
            for d in dates:
                k = (d.year, 0) if by_year else (d.year, d.month)
                cnt[k] = cnt.get(k, 0) + 1
            if by_year:
                for y in range(min(d.year for d in dates), max(d.year for d in dates) + 1):
                    cnt.setdefault((y, 0), 0)
            keys = sorted(cnt)
            lab = (lambda k: str(k[0])) if by_year else (lambda k: f"{k[1]:02d}.{k[0]}")
            mx = max(cnt.values())
            bars = "".join(
                f'<div class="bar" style="height:{max(4, round(cnt[k] / mx * 70))}px" '
                f'title="{lab(k)}: {cnt[k]}"><span>{cnt[k]}</span></div>'
                for k in keys
            )
            if 2 < len(keys) <= 6:
                axis, ax_cls = "".join(f"<span>{lab(k)}</span>" for k in keys), "ax c"
            else:
                axis = f"<span>{lab(keys[0])}</span>" + (f"<span>{lab(keys[-1])}</span>" if len(keys) > 1 else "")
                ax_cls = "ax"
            chart = (
                f'<div class="chh"><span>{S("r_chart")}</span><span>{S("r_chart_unit")}</span></div>'
                f'<div class="bars">{bars}</div><div class="{ax_cls}">{axis}</div>'
            )

        pills = "".join(
            f'<button class="pill{" on" if k == "all" else ""}" data-f="{k}">{IC[ic]}{S("f_" + k)}</button>'
            for k, ic in (("all", "all"), ("old", "moon"), ("nw", "new"), ("pr", "prem"))
        )
        L = {
            "copy": S("b_copy"), "sel": S("b_sel"), "unsel": S("b_unsel"), "pick": S("b_pick"), "done": S("b_done"),
            "c_name": S("c_name"), "c_user": S("c_user"), "c_id": S("c_id"), "c_joined": S("c_joined"),
            "c_seen": S("c_seen"), "c_prem": S("c_prem"), "yes": S("c_yes"),
            "m_of": S("m_of"),
        }
        title = esc(chat_title)
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        music = json.dumps([str(u) for u in (tracks if tracks is not None else (self.config["music_urls"] or []))]).replace("</", "<\\/")
        return (
            f'<!DOCTYPE html><html lang="{S("lang")}"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{esc(S('r_title').format(chat_title))}</title><style>{CSS}</style></head>"
            '<body><div id="bg"><canvas id="stars"></canvas><i class="pl"></i>'
            '<i class="o o1"></i><i class="o o2"></i><i class="o o3"></i></div>'
            '<div id="app"><div class="w"><div class="hero"><span class="hi">🤫</span>'
            f'<div><div class="ov">{S("r_over")}</div><h1>{S("r_h1")}</h1></div></div>'
            f'<div class="chips"><span>{title}</span><span>{now}</span><span>{S("r_checked").format(total)}</span></div>'
            f'<div class="st"><div><small>{IC["users"]}{S("r_lurkers")}</small><b>{count}</b><i>{percent:.1f}%</i></div>'
            f'<div><small>{IC["moon"]}{S("r_stale")}</small><b>{stale_count}</b></div></div>'
            f'{chart}<div class="pills">{pills}</div>'
            f'<input id="q" type="text" placeholder="{S("r_search")}">'
            f'<div class="tb"><button class="btn" id="sa">{IC["sel"]}<span>{S("b_sel")}</span></button>'
            f'<button class="btn" id="cp">{IC["copy"]}<span>{S("b_copy")} (0)</span></button>'
            f'<button class="btn" id="csv">{IC["csv"]}<span>{S("b_csv")}</span></button>'
            f'<button class="btn" id="mu">{IC["music"]}<span>{S("b_music")}</span></button></div>'
            f'<div class="list">{"".join(rows)}</div>'
            f'<div class="empty" id="e">{S("r_empty")}</div><p class="note">{S("r_note")}</p></div></div>'
            f'<div class="wm"><a href="https://t.me/lceta">{S("r_sig")} · <b>@lceta</b></a></div>'
            '<div class="mpl" id="mpl"><div class="mpe"><i></i><i></i><i></i><i></i></div>'
            '<div class="mpi"><b id="mpt"></b><small id="mps"></small>'
            '<div class="mpb" id="mpb"><span id="mpa">0:00</span><div class="mpr" id="mpr"><i id="mpf"></i></div><span id="mpd">0:00</span></div></div>'
            '<div class="mpk"><button class="mb" id="mpv" aria-label="prev"><svg viewBox="0 0 24 24"><path d="M6 5h2v14H6zM20 5v14L9 12z"/></svg></button>'
            '<button class="mb big" id="mpp" aria-label="play/pause"><svg class="ip" viewBox="0 0 24 24"><path d="M7 4v16l13-8z"/></svg><svg class="ia" viewBox="0 0 24 24"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg></button>'
            '<button class="mb" id="mpn" aria-label="next"><svg viewBox="0 0 24 24"><path d="M16 5h2v14h-2zM4 5v14l11-7z"/></svg></button>'
            '<button class="mb sm" id="mpx" aria-label="close"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg></button></div></div>'
            '<div class="mls" id="mls"></div><div id="sb"><div id="th"></div></div>'
            f"<script>var L={json.dumps(L, ensure_ascii=False)};var MU={music};{JS}{MUSIC_JS}</script></body></html>"
        )
