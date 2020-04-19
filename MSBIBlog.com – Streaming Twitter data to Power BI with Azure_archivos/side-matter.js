/*
side-matter.js
Version 1.4

Plugin: Side Matter
Author: Christopher Setzer
URI: http://wordpress.org/extend/plugins/side-matter/
License: GPLv2
*/
(function($){
    $.fn.offsetRelative = function(top){
        var $this = $(this);
        var $parent = $this.offsetParent();
        var offset = $this.position();
        if(!top) return offset; // Didn't pass a 'top' element 
        else if($parent.get(0).tagName == "BODY") return offset; // Reached top of document
        else if($(top,$parent).length) return offset; // Parent element contains the 'top' element we want the offset to be relative to 
        else if($parent[0] == $(top)[0]) return offset; // Reached the 'top' element we want the offset to be relative to 
        else { // Get parent's relative offset
            var parent_offset = $parent.offsetRelative(top);
            offset.top += parent_offset.top;
            offset.left += parent_offset.left;
            return offset;
        }
    };
    $.fn.positionRelative = function(top){
        return $(this).offsetRelative(top);
    };
}(jQuery));

(function($) {

/* These variables obtain their values from the settings fields in `side-matter.php`. */
var isResponsive = side_matter.is_responsive; // If true, reposition notes on resize/zoom (boolean)
var useEffects = side_matter.use_effects; // If true, enable fade effects when positioning notes (boolean)
var noteAdjust = side_matter.note_adjust; // Distance to arbitrarily offset note position, in px (integer)
var htmlClass = side_matter.html_class; // Class to use when selecting Side Matter tags (string; default: 'side-matter')

var isResizing; // Used for resize-timeout function

function placeNotes() {
	for (n = 1, refCount = $('a.side-matter-ref').length; n <= refCount; n++) { // Iterate through notes and position each
		var ref = '#ref-' + n; // Reference anchor
		var note = '#note-' + n; // Sidenote
		var refPosition = $(ref).positionRelative('.uk-panel').top; // Position of reference anchor
		var notePosition = $(note).positionRelative('.uk-panel').top; // Position of sidenote
		var noteOffset = refPosition - notePosition - noteAdjust; // Get current offset between reference and note, minus noteAdjust
		var finalOffset = (noteOffset < 0) ? 0 : noteOffset; // If offset is negative, set to 0 (prevents layout problems)
		$(note).css('marginTop', finalOffset); // Position note
	}
}

$(document).ready(function() { // Loop twice to correct any misplacements on first load
	if (useEffects == 1) $('ol.' + htmlClass + '-list').css('opacity', 0); // Make notes briefly transparent
});

$(window).load(function() { // Position notes and fade in
	for (i = 1; i <= 2; i++) placeNotes(); // Run loop twice to correct initial misplacements
	if (useEffects == 1) $('ol.' + htmlClass + '-list').fadeTo(360, 1);
});

if (isResponsive == 1) {
	$(window).resize(function() { // Reposition notes on resize/zoom
		if (useEffects == 1) $('li.' + htmlClass + '-note').fadeTo(20, 0);
		var timeoutInterval = 600; // Time (in ms) to throttle the re-positioning loop, preventing script overload on resize (default: 600)
		function doneResizing() {
			for (i = 1; i <= 2; i++) placeNotes();
			if (useEffects == 1) $('li.' + htmlClass + '-note').fadeTo(360, 1);
		}
		clearTimeout(isResizing);
		isResizing = setTimeout(doneResizing, timeoutInterval);
	});
}

})(jQuery);
