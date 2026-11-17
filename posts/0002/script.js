'use strict';
jQuery(function ($) {
	// Native buttons supply Enter/Space activation without custom key handlers.
	$('[data-feedback]').on('click', function () {
		const $button = $(this);
		$button.closest('.question').find('[data-feedback]').attr('aria-pressed', 'false');
		$button.attr('aria-pressed', 'true');
		const $answer = $('#' + $button.attr('aria-controls'));
		const templateId = $button.attr('data-feedback-template');
		if (templateId) {
			$answer.empty().append(document.getElementById(templateId).content.cloneNode(true));
		} else {
			$answer.text($button.attr('data-feedback'));
		}
	});

	$('#game-count').on('submit', function (event) {
		event.preventDefault();
		const correct = Number($('#count').val()) === 12;
		$('#count-answer').text(correct
			? 'Right! The measures are independent, so twelve games.'
			: 'No, because they play in different games, each cell in the table represents a game.');
	});

	$('#reveal-u').on('click', function () {
		const expanded = $(this).attr('aria-expanded') !== 'true';
		$(this).attr('aria-expanded', String(expanded)).text(expanded
			? 'Hide Melanie’s stats' : 'Click to reveal Melanie’s stats');
		$('.u-value').prop('hidden', !expanded);
		$('.u-placeholder').prop('hidden', expanded);
		$('#u-status').text(expanded ? 'Melanie’s contributions are 4.5, 4, 4.5, 1.5, 4, and 4.' : 'Melanie’s contributions are hidden.');
	});

	const $games = $('.game');
	function highlight(button) {
		$games.removeClass('is-highlighted');
		if (button) $(button).addClass('is-highlighted');
	}
	$games.on('mouseenter focus', function () { highlight(this); });
	$games.on('mouseleave blur', function () {
		// Restore the selected score when a temporary hover/focus ends.
		highlight($games.filter('[aria-pressed="true"]')[0]);
	});
	$games.on('click', function () {
		const wasSelected = $(this).attr('aria-pressed') === 'true';
		$games.attr('aria-pressed', 'false');
		$(this).attr('aria-pressed', String(!wasSelected));
		highlight(this);
		$('#game-selection').text(wasSelected ? 'Game selection cleared.' : 'Selected ' + $(this).attr('aria-label') + '.');
	});
});
