(function(){
  // mobile menu
  var mb=document.getElementById('menu-btn'),mn=document.getElementById('m-nav');
  if(mb&&mn){var set=function(o){mb.setAttribute('aria-expanded',o);mb.setAttribute('aria-label',o?'Close menu':'Open menu');mn.hidden=!o};mb.addEventListener('click',function(){set(mn.hidden)});mn.addEventListener('click',function(e){if(e.target.tagName==='A')set(false)});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!mn.hidden){set(false);mb.focus()}})}
  // zone hover sync + flash the idea card on jump
  var links=[].slice.call(document.querySelectorAll('.zones a,.zlist a'));
  function sync(h,on){links.forEach(function(l){if(l.getAttribute('href')===h)l.classList.toggle('on',on)})}
  links.forEach(function(l){var h=l.getAttribute('href');l.addEventListener('mouseenter',function(){sync(h,true)});l.addEventListener('mouseleave',function(){sync(h,false)});l.addEventListener('focus',function(){sync(h,true)});l.addEventListener('blur',function(){sync(h,false)});
    l.addEventListener('click',function(){var c=document.querySelector(h);if(c){c.classList.add('flash');setTimeout(function(){c.classList.remove('flash')},1600)}})});
  // income sketch
  var G=[
    {id:'st',name:'Extended-stay suites',cat:'lodging',f:[['u','Suites',30,0,60,2,''],['r','Nightly rate',95,60,180,5,'$'],['o','Occupancy',75,30,95,1,'%']],calc:function(v){return v.u*v.r*v.o/100*365}},
    {id:'ca',name:'View casitas',cat:'lodging',f:[['u','Casitas',12,0,20,1,''],['r','Nightly rate',225,100,450,5,'$'],['o','Occupancy',55,20,90,1,'%']],calc:function(v){return v.u*v.r*v.o/100*365}},
    {id:'ev',name:'Events on the lawn',cat:'events',f:[['n','Events per year',36,0,120,2,''],['r','Venue fee per event',8000,1000,20000,500,'$']],calc:function(v){return v.n*v.r}},
    {id:'gl',name:'Glamping tents',cat:'flex',f:[['u','Tents',10,0,20,1,''],['r','Nightly rate',90,40,250,5,'$'],['o','Occupancy',45,15,85,1,'%']],calc:function(v){return v.u*v.r*v.o/100*365}}
  ];
  var C=document.getElementById('ctrls'),B=document.getElementById('c-bars'),T=document.getElementById('c-total'),vals={};
  function fmt(n){return '$'+Math.round(n).toLocaleString('en-US')}
  function fv(k,u,v){return u==='$'?'$'+(+v).toLocaleString('en-US'):u==='%'?v+'%':v}
  G.forEach(function(g){vals[g.id]={};var d=document.createElement('div');d.className='cgrp';d.style.setProperty('--c','var(--z-'+g.cat+')');d.innerHTML='<h3>'+g.name+'</h3>';
    g.f.forEach(function(f){vals[g.id][f[0]]=f[2];var l=document.createElement('label');var id='c-'+g.id+'-'+f[0];l.innerHTML='<span>'+f[1]+'</span><output for="'+id+'">'+fv(f[0],f[6],f[2])+'</output><input type="range" id="'+id+'" min="'+f[3]+'" max="'+f[4]+'" step="'+f[5]+'" value="'+f[2]+'">';
      var inp=l.querySelector('input'),out=l.querySelector('output');inp.addEventListener('input',function(){vals[g.id][f[0]]=+inp.value;out.textContent=fv(f[0],f[6],inp.value);draw()});d.appendChild(l)});C.appendChild(d)});
  function draw(){var rows=G.map(function(g){return{n:g.name,c:g.cat,v:g.calc(vals[g.id])}}),tot=rows.reduce(function(a,r){return a+r.v},0),mx=Math.max.apply(null,rows.map(function(r){return r.v}).concat([1]));
    T.textContent=fmt(tot);B.innerHTML=rows.map(function(r){return '<div class="bar" style="--c:var(--z-'+r.c+')"><div class="bl"><span>'+r.n+'</span><b>'+fmt(r.v)+'</b></div><div class="track"><div class="fill" style="width:'+(r.v/mx*100).toFixed(1)+'%"></div></div></div>'}).join('');
    B.setAttribute('aria-label','Gross revenue by add-on: '+rows.map(function(r){return r.n+' '+fmt(r.v)}).join(', ')+'. Total '+fmt(tot)+'.')}
  draw();
})();
