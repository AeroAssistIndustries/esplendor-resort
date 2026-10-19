/* Run-your-terms calculator: Path A seller financing and Path B 50/50 stake. */
(function(){
  var $=function(id){return document.getElementById(id)};
  if(!$('terms')) return;
  var M=function(v,d){d=d==null?2:d;return '$'+String(+(v/1e6).toFixed(d))+'M'};
  var K=function(v){return '$'+Math.round(v).toLocaleString('en-US')};

  /* tabs (roving tabindex, arrow keys) */
  var tabs=[$('tt-a'),$('tt-b')], panels=[$('tp-a'),$('tp-b')];
  function sel(i,focus){tabs.forEach(function(t,j){var on=i===j;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;panels[j].hidden=!on});if(focus)tabs[i].focus()}
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){sel(i)});
    t.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();sel(i===0?1:0,true)}});
  });

  /* Path A: seller financing */
  var ty='io';
  [].forEach.call(document.querySelectorAll('#tp-a [data-ty]'),function(b){b.addEventListener('click',function(){ty=b.dataset.ty;
    [].forEach.call(document.querySelectorAll('#tp-a [data-ty]'),function(x){x.setAttribute('aria-pressed',x===b)});calcA()})});
  var NOI_BASE=2.9e6;
  function calcA(){
    var px=+$('sa-px').value*1e6, dp=+$('sa-dp').value/100, r=+$('sa-rt').value/100, n=+$('sa-tm').value;
    $('sa-px-o').textContent=M(px,2); $('sa-dp-o').textContent=Math.round(dp*100)+'%';
    $('sa-rt-o').textContent=(r*100).toFixed(2).replace(/0$/,'')+'%'; $('sa-tm-o').textContent=n+(n===1?' year':' years');
    var cash=px*dp, loan=px-cash, i=r/12, mo, bal;
    if(ty==='io'){mo=loan*i; bal=loan}
    else{var N=300; mo=loan*i/(1-Math.pow(1+i,-N)); var k=n*12; bal=loan*Math.pow(1+i,k)-mo*(Math.pow(1+i,k)-1)/i}
    $('sa-cash').textContent=M(cash); $('sa-loan').textContent=M(loan);
    $('sa-loan-s').textContent=Math.round((1-dp)*100)+'% of the price';
    $('sa-mo').textContent=K(mo); $('sa-mo-s').textContent=K(mo*12)+' a year';
    $('sa-bal').textContent=M(Math.max(bal,0)); $('sa-bal-s').textContent='balloon after '+n+(n===1?' year':' years');
    $('sa-bar-a').style.width=(dp*100)+'%'; $('sa-bar-b').style.width=((1-dp)*100)+'%';
    $('sa-bar').setAttribute('aria-label','Your cash '+Math.round(dp*100)+'%, seller-financed '+Math.round((1-dp)*100)+'%');
    var cov=NOI_BASE/(mo*12);
    $('sa-cov').textContent='At the base-case stabilized NOI of about $2.9M a year, this payment would be covered '+cov.toFixed(2)+'×. That income only arrives after renovation and ramp-up, and before any renovation loan.';
  }
  ['sa-px','sa-dp','sa-rt','sa-tm'].forEach(function(id){$(id).addEventListener('input',calcA)});
  calcA();

  /* Path B: 50/50 stake. Values match the returns model (8.5% cap on forward NOI). */
  var SC={cons:{v:25.8e6,adr:150,occ:60},base:{v:37.7e6,adr:165,occ:66},up:{v:67.2e6,adr:195,occ:76}}, sc='base', INV=15e6, CAP=.085;
  [].forEach.call(document.querySelectorAll('#tp-b [data-sc]'),function(b){b.addEventListener('click',function(){sc=b.dataset.sc;
    [].forEach.call(document.querySelectorAll('#tp-b [data-sc]'),function(x){x.setAttribute('aria-pressed',x===b)});calcB()})});
  $('sb-refi').addEventListener('change',calcB);
  function calcB(){
    var s=SC[sc], half=s.v/2, noi=s.v*CAP/2, refi=$('sb-refi').checked;
    $('sb-desc').textContent='$'+s.adr+' average rate, '+s.occ+'% occupancy, valued at '+M(s.v,1)+' when stabilized.';
    $('sb-val').textContent=M(half,1); $('sb-val-s').textContent='of '+M(s.v,1)+' stabilized value';
    $('sb-mult').textContent=(half/INV).toFixed(2)+'×';
    $('sb-noi').textContent=M(noi,2); $('sb-noi-s').textContent=(noi/INV*100).toFixed(1)+'% a year on $15M, before debt';
    if(refi){var back=s.v*.65*.99/2; $('sb-refi-o').textContent=M(back,1); $('sb-refi-s').textContent=Math.round(back/INV*100)+'% of your capital, keeping your 50%'}
    else{$('sb-refi-o').textContent='—'; $('sb-refi-s').textContent='no refinance'}
    $('sb-bar-a').style.width='50%'; $('sb-bar-b').style.width='50%';
    $('sb-bar').setAttribute('aria-label','Investor 50%, current owner 50%');
  }
  calcB();
})();
