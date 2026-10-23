'use strict';
const answers = {
  'jack-yes': 'Right! Jack scored 78 in <strong>100%</strong> of his games.',
  'jack-no': 'Sure you can. Jack scored 78 in <strong>100%</strong> of his games.',
  'chance-yes': 'He sure does. He’ll win 25% of the time.',
  'chance-no': 'Sure he does. He’ll win 25% of the time.'
};
document.querySelectorAll('[data-answer]').forEach((button) => {
  button.addEventListener('click', () => {
    const group = button.closest('.question');
    group.querySelectorAll('[data-answer]').forEach((choice) => {
      choice.setAttribute('aria-pressed', String(choice === button));
    });
    document.getElementById(button.getAttribute('aria-controls')).innerHTML = answers[button.dataset.answer];
  });
});
document.getElementById('reveal-jill').addEventListener('click', (event) => {
  const button = event.currentTarget;
  const expanded = button.getAttribute('aria-expanded') !== 'true';
  button.setAttribute('aria-expanded', String(expanded));
  document.querySelectorAll('.reveal-value').forEach((value) => { value.hidden = !expanded; });
  document.querySelectorAll('.placeholder').forEach((value) => { value.hidden = expanded; });
  button.textContent = expanded ? 'hide the answer' : 'click to show the answer';
  document.getElementById('jill-status').textContent = expanded ? 'Jill scored 81 in 25% of her games and 77 in 75% of her games.' : 'Jill’s answer is hidden.';
});
