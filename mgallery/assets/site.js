// 신불당아트센터 M갤러리 — 작품 크게 넘겨 보기(PKM식)와 작품 문의 창
(function () {
  var PHONE = '1533-8771';
  var TALK = 'https://talk.naver.com/w4maya';          // 네이버 톡톡 (공식 홈페이지와 같은 창구)
  var KAKAO = 'https://pf.kakao.com/_vaDxeX/chat';      // 카카오톡 채널 「신불당M갤러리」

  var LANG = (document.documentElement.lang || 'ko').slice(0, 2);
  var TX = {
    ko: { title: '작품 문의', kakao: '카카오톡으로 문의', tel: '전화로 문의 ', talk: '네이버 톡톡으로 문의', sms: '문자로 문의', tip: '카톡·톡톡을 누르면 작품 이름이 복사돼요. 채팅창에 붙여 넣어 주세요.', close: '닫기 ✕', ask: '이 작품 문의', general: '작품 구입·대여·선물용 그림 상담 (예산과 걸 공간을 알려 주시면 골라 드려요)', msgW: function (w) { return '[M갤러리 작품 문의] ' + w + ' — 이 작품 문의드려요.'; }, msgG: '[M갤러리 작품 문의] 작품 구입 상담 부탁드려요.' },
    en: { title: 'Inquire', kakao: 'Message on KakaoTalk', tel: 'Call +82 ', talk: 'Message on Naver TalkTalk', sms: 'Send a text', tip: 'Tapping KakaoTalk or TalkTalk copies the work title. Paste it into the chat. We reply in Korean or English.', close: 'Close ✕', ask: 'Inquire about this work', general: 'Buying, renting or gifting art (tell us your budget and space)', msgW: function (w) { return '[M Gallery inquiry] ' + w + ' — I would like to ask about this work.'; }, msgG: '[M Gallery inquiry] I would like to ask about buying a work.' },
    ja: { title: '作品のお問い合わせ', kakao: 'カカオトークで問い合わせる', tel: '電話 +82 ', talk: 'Naver TalkTalkで問い合わせる', sms: 'SMSで問い合わせる', tip: 'カカオトーク・TalkTalkを押すと作品名がコピーされます。チャットに貼り付けてください。', close: '閉じる ✕', ask: 'この作品について問い合わせる', general: '作品の購入・レンタル・ギフトのご相談（ご予算と飾る場所をお知らせください）', msgW: function (w) { return '[Mギャラリー作品のお問い合わせ] ' + w + ' — この作品について知りたいです。'; }, msgG: '[Mギャラリー作品のお問い合わせ] 作品購入の相談をお願いします。' },
    zh: { title: '作品咨询', kakao: '通过KakaoTalk咨询', tel: '电话 +82 ', talk: '通过Naver TalkTalk咨询', sms: '短信咨询', tip: '点击KakaoTalk或TalkTalk会复制作品名称，请粘贴到聊天窗口。', close: '关闭 ✕', ask: '咨询此作品', general: '作品购买、租赁、礼品咨询（请告诉我们预算和挂画空间）', msgW: function (w) { return '[M画廊作品咨询] ' + w + ' — 想咨询这件作品。'; }, msgG: '[M画廊作品咨询] 想咨询购买作品。' }
  };
  var X = TX[LANG] || TX.ko;

  function el(html) { var d = document.createElement('div'); d.innerHTML = html.trim(); return d.firstChild; }
  function $(id) { return document.getElementById(id); }

  var ask = el(
    '<dialog id="askDlg" aria-labelledby="askTitle"><div class="dlg">' +
    '<button class="x" type="button" data-close>' + X.close + '</button>' +
    '<h2 id="askTitle">' + X.title + '</h2>' +
    '<p class="what" id="askWhat"></p>' +
    '<div class="opts">' +
    '<a class="btn" href="' + KAKAO + '" target="_blank" rel="noopener" data-copy>' + X.kakao + '</a>' +
    '<a class="btn line" href="tel:15338771">' + X.tel + PHONE + '</a>' +
    '<a class="btn line" href="' + TALK + '" target="_blank" rel="noopener" data-copy>' + X.talk + '</a>' +
    '<a class="btn line" id="askSms" href="sms:15338771">' + X.sms + '</a>' +
    '</div>' +
    '<p class="tip">' + X.tip + '</p>' +
    '</div></dialog>');
  var viewer = el(
    '<dialog class="viewer" id="viewDlg" aria-label="작품 크게 보기"><div class="dlg">' +
    '<div class="vtop"><span id="vCount"></span><button class="x" type="button" data-close>' + X.close + '</button></div>' +
    '<div class="vimg"><img id="vImg" alt=""><button class="vnav prev" type="button" id="vPrev" aria-label="이전 작품">‹</button><button class="vnav next" type="button" id="vNext" aria-label="다음 작품">›</button></div>' +
    '<div class="vcap"><p id="vCap"></p><button class="btn" type="button" id="vAsk">' + X.ask + '</button></div>' +
    '</div></dialog>');
  document.body.appendChild(ask);
  document.body.appendChild(viewer);

  var current = '';
  function msg(w) { return w ? X.msgW(w) : X.msgG; }
  function copy(t) { try { navigator.clipboard.writeText(t).catch(function () {}); } catch (e) {} }

  function openAsk(work) {
    current = work || '';
    $('askWhat').textContent = current || X.general;
    $('askSms').href = 'sms:15338771?&body=' + encodeURIComponent(msg(current));
    if (viewer.open) viewer.close();
    ask.showModal();
  }

  // 같은 묶음(data-set)의 작품을 차례로 넘겨 본다
  var list = [], idx = 0;
  function show(i) {
    idx = (i + list.length) % list.length;
    var b = list[idx];
    $('vImg').src = b.getAttribute('data-src');
    $('vImg').alt = b.getAttribute('data-alt') || '';
    $('vCap').innerHTML = b.getAttribute('data-caphtml') || '';
    $('vCount').textContent = (idx + 1) + ' / ' + list.length;
    var one = list.length < 2;
    $('vPrev').hidden = one; $('vNext').hidden = one;
  }
  $('vPrev').addEventListener('click', function () { show(idx - 1); });
  $('vNext').addEventListener('click', function () { show(idx + 1); });
  $('vAsk').addEventListener('click', function () { openAsk(list[idx].getAttribute('data-work')); });
  document.addEventListener('keydown', function (e) {
    if (!viewer.open) return;
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
  var sx = null;
  viewer.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
  viewer.addEventListener('touchend', function (e) {
    if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
  });

  document.addEventListener('click', function (e) {
    var c = e.target.closest('[data-copy]'); if (c) { copy(msg(current)); return; }
    var t = e.target.closest('[data-ask]');
    if (t) { e.preventDefault(); openAsk(t.getAttribute('data-ask')); return; }
    var v = e.target.closest('[data-src]');
    if (v) {
      var set = v.getAttribute('data-set');
      list = Array.prototype.slice.call(document.querySelectorAll('[data-src][data-set="' + set + '"]'));
      show(list.indexOf(v));
      viewer.showModal(); return;
    }
    if (e.target.closest('[data-close]')) { var d = e.target.closest('dialog'); if (d) d.close(); return; }
    if (e.target.tagName === 'DIALOG') e.target.close();
  });
})();
