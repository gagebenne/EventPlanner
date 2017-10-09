$("#new").addClass('active')
$(".date-picker").datepicker()
$(".24-hour-form").hide();

$('.toggle-time-button').on('click', function(e){
	e.preventDefault()
	$('.24-hour-form').toggle()
	$('.12-hour-form').toggle()
});

$('.timeslot-picker').selectable({
	selected: function(event, ui){
		$(ui.selected).addClass('active')
		$(ui.selected).removeClass('selecting')
		$(ui.selected).children('input').val('1')
	},
	unselected: function(event, ui){
		$(ui.unselected).removeClass('active')
		$(ui.unselected).removeClass('selecting')
		$(ui.unselected).children('input').val('0')
	},
	selecting: function(event, ui){
		$(ui.selecting).addClass('selecting')
	}
});
