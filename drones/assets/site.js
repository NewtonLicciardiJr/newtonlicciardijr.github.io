'use strict';
const search=document.querySelector('#model-search');
if(search){let sector='Todos';const cards=[...document.querySelectorAll('.model-card')],buttons=[...document.querySelectorAll('[data-filter]')];const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();function filter(){let n=0;const q=normalize(search.value.trim());for(const c of cards){const show=(sector==='Todos'||c.dataset.sector===sector)&&normalize(c.dataset.search).includes(q);c.hidden=!show;if(show)n++;}document.querySelector('#model-count').textContent=`${n} ${n===1?'modelo':'modelos'}`;document.querySelector('#model-empty').hidden=n!==0;}search.addEventListener('input',filter);for(const b of buttons)b.addEventListener('click',()=>{sector=b.dataset.filter;buttons.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));filter();});}

// The authored display:block rules override the browser's [hidden] default.
// Reveal the frame before setting src so the user click can start playback.
for(const button of document.querySelectorAll('.youtube-launch')){
 button.addEventListener('click',()=>{
  const player=button.closest('.youtube-preview').querySelector('iframe');
  const url=new URL(player.dataset.youtubeSrc,window.location.href);
  url.searchParams.set('autoplay','1');
  url.searchParams.set('playsinline','1');
  button.hidden=true;
  button.style.display='none';
  player.hidden=false;
  player.style.display='block';
  player.loading='eager';
  player.src=url.toString();
 });
}

for(const video of document.querySelectorAll('[data-review-video]')){
 const wrap=video.closest('.video-section');
 const end=wrap.querySelector('.end-links');
 const start=wrap.querySelector('.resume-play');
 const sync=()=>{end.hidden=!(Number.isFinite(video.duration)&&video.duration-video.currentTime<=20);};
 video.addEventListener('timeupdate',sync);video.addEventListener('loadedmetadata',sync);video.addEventListener('seeked',sync);video.addEventListener('ended',sync);
 const play=()=>{video.muted=false;const result=video.play();if(result&&result.then)result.then(()=>{start.hidden=true;}).catch(()=>{start.hidden=false;});};
 start.addEventListener('click',play);
 if(new URLSearchParams(window.location.search).get('autoplay')==='1')play();
}
