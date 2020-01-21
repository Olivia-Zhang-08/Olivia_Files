// With JQuery, get the item with the id "colorpicker", which is a dom element and on it use spectrum (which is a function I imported in layout.html) and give this function options for the initialization process.
// Here I have two options (two key:value pairs); the key color is a string, and the key change is an event (events can be put in this initialization process as options)

// JavaScript should be run only whne the page is fully loaded, so the ready function takes care of that by running only when the whole document is ready.
$(document).ready(function(){
    // https://bgrins.github.io/spectrum/
    $("#colorpicker").spectrum({
    change: colorChanged
    });
});

// Convert the color in HSV format to RGB string format
function colorChanged(color) {
    var colorRgb = color.toRgbString();
    $("#colorpicker").val(colorRgb)
}
