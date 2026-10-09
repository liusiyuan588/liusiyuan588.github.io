(function(){
  const toggle=document.querySelector('[data-mobile-toggle]');
  const nav=document.querySelector('[data-mobile-nav]');
  if(toggle&&nav){
    toggle.addEventListener('click',()=>{
      const open=nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded',String(open));
      toggle.textContent=open?'Close':'Menu';
    });
    nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded','false');
      toggle.textContent='Menu';
    }));
    document.addEventListener('keydown',e=>{
      if(e.key==='Escape'&&nav.classList.contains('open')){
        nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.textContent='Menu';toggle.focus();
      }
    });
  }
  const input=document.querySelector('[data-doc-search]');
  if(input){
    const links=Array.from(document.querySelectorAll('[data-search-item]'));
    const empty=document.querySelector('[data-search-empty]');
    input.addEventListener('input',()=>{
      const value=input.value.trim().toLowerCase();let count=0;
      links.forEach(x=>{
        const visible=x.textContent.toLowerCase().includes(value);
        x.hidden=!visible;if(visible)count++;
      });
      if(empty)empty.style.display=count?'none':'block';
    });
  }
})();
