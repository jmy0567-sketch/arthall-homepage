// 신불당아트센터 M갤러리 — 작품 문의 창과 크게 보기
(function () {
  var PHONE = '1533-8771';
  var TALK = 'https://talk.naver.com/w4maya';   // 네이버 톡톡 (공식 홈페이지와 같은 창구)
  var KAKAO = 'https://pf.kakao.com/_vaDxeX/chat';                                // 카카오톡 채널 링크가 생기면 여기에 (예: https://pf.kakao.com/_xxxx/chat)

  function el(html) { var d = document.createElement('div'); d.innerHTML = html.trim(); return d.firstChild; }

  var ask = el(
    '<dialog id="askDlg" aria-labelledby="askTitle"><div class="dlg">' +
    '<button class="x" type="button" data-close>닫기 ✕</button>' +
    '<h2 id="askTitle">작품 문의</h2>' +
    '<p class="what" id="askWhat"></p>' +
    '<div class="opts">' +
    '<a class="btn" id="askTel" href="tel:15338771">전화로 문의 ' + PHONE + '</a>' +
    (KAKAO ? '<a class="btn line" id="askKakao" target="_blank" rel="noopener" href="' + KAKAO + '">카카오톡으로 문의</a>' : '') +
    '<a class="btn line" id="askTalk" target="_blank" rel="noopener" href="' + TALK + '">네이버 톡톡으로 문의</a>' +
    '<a class="btn line" id="askSms" href="sms:15338771">문자로 문의</a>' +
    '</div>' +
    '<p class="tip" id="askTip">톡톡·카톡을 누르면 작품 이름이 복사돼요. 채팅창에 붙여 넣어 주세요.</p>' +
    '</div></dialog>');
  var view = el(
    '<dialog class="view" id="viewDlg" aria-label="작품 크게 보기"><div class="dlg">' +
    '<button class="x" type="button" data-close>닫기 ✕</button>' +
    '<img id="viewImg" alt="">' +
    '<p class="cap" id="viewCap"></p>' +
    '<button class="ask" type="button" id="viewAsk">이 작품 문의 →</button>' +
    '</div></dialog>');
  document.body.appendChild(ask);
  document.body.appendChild(view);

  var current = '';
  function msg(w) { return w ? '[M갤러리 작품 문의] ' + w + ' — 이 작품 문의드려요.' : '[M갤러리 작품 문의] 작품 구입 상담 부탁드려요.'; }
  function copy(t) { try { navigator.clipboard.writeText(t).catch(function () {}); } catch (e) {} }

  function openAsk(work) {
    current = work || '';
    document.getElementById('askWhat').textContent = current ? current : '작품 구입·대여·선물용 그림 상담 (예산과 걸 공간을 알려 주시면 골라 드려요)';
    var body = encodeURIComponent(msg(current));
    document.getElementById('askSms').href = 'sms:15338771?&body=' + body;
    if (view.open) view.close();
    ask.showModal();
  }
  ['askTalk', 'askKakao'].forEach(function (id) {
    var a = document.getElementById(id); if (a) a.addEventListener('click', function () { copy(msg(current)); });
  });

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-ask]');
    if (t) { e.preventDefault(); openAsk(t.getAttribute('data-ask')); return; }
    var p = e.target.closest('[data-view]');
    if (p) {
      var img = p.querySelector('img');
      var vi = document.getElementById('viewImg');
      vi.src = p.getAttribute('data-view'); vi.alt = img ? img.alt : '';
      document.getElementById('viewCap').textContent = p.getAttribute('data-cap') || '';
      var w = p.getAttribute('data-work');
      document.getElementById('viewAsk').onclick = function () { openAsk(w); };
      view.showModal(); return;
    }
    if (e.target.closest('[data-close]')) { var d = e.target.closest('dialog'); if (d) d.close(); return; }
    if (e.target.tagName === 'DIALOG') e.target.close();
  });
})();
