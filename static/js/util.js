
function numbers_with_commas(x) {
  return parseInt(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function urlify(text) {
  var urlRegex = /(https?:\/\/[^\s]+)/g;
  return text.replace(urlRegex, function(url) {
      return '<a href="' + url + '">' + url + '</a>';
  });
}

function chunk_string(str, length) {
	return str.match(new RegExp('.{1,' + length + '}', 'g'));
}

$.fn.redraw = function(){
  $(this).each(function(){
    var redraw = this.offsetHeight;
  });
};