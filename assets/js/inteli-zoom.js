// Zoom de texto por teclado. "+" aumenta e "-" diminui --escala-texto do
// slide ativo em passos de 2px, "0" volta ao padrao. Serve para quem esta
// longe da tela, na sala grande. O JS nao declara cor nem fonte nenhuma
// aqui: so le e escreve a custom property, o valor visual vem do CSS.
(function () {
  'use strict';

  var PASSO = 2;

  function slideAtivo() {
    return document.querySelector('.reveal .slides section.present') ||
      document.querySelector('.reveal .slides section');
  }

  function escalaAtual(slide) {
    var valor = getComputedStyle(slide).getPropertyValue('--escala-texto').trim();
    var numero = parseFloat(valor);
    return isNaN(numero) ? 18 : numero;
  }

  function ajustar(delta) {
    var slide = slideAtivo();
    if (!slide) return;
    var nova = escalaAtual(slide) + delta;
    slide.style.setProperty('--escala-texto', nova + 'px');
  }

  function resetar() {
    var slide = slideAtivo();
    if (!slide) return;
    slide.style.removeProperty('--escala-texto');
  }

  function foco_em_campo_editavel(alvo) {
    return alvo && (alvo.tagName === 'INPUT' || alvo.tagName === 'TEXTAREA' || alvo.isContentEditable);
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (foco_em_campo_editavel(e.target)) return;

    if (e.key === '+' || (e.key === '=' && e.shiftKey)) {
      e.preventDefault();
      ajustar(PASSO);
    } else if (e.key === '-') {
      e.preventDefault();
      ajustar(-PASSO);
    } else if (e.key === '0') {
      e.preventDefault();
      resetar();
    }
  });
})();
