(function() {
  var PollProcessor;
  var __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  }, __hasProp = Object.prototype.hasOwnProperty;
  PollProcessor = function(_a) {
    var url;
    this.baseurl = _a;
    this.template = "";
    url = this.baseurl + this.template_api + 'entry.poll.mustache';
    $.ajax({
      url: url,
      dataType: 'jsonp',
      success: __bind(function(data) {
        return (this.template = data);
      }, this)
    });
    return this;
  };
  PollProcessor.prototype.content_api = "/api/1/content/";
  PollProcessor.prototype.template_api = "/api/templates/";
  PollProcessor.prototype.display_items = function() {
    return $.ajax({
      url: "http://localhost:9991/api/1/content/0?r=jsview&jsview_type=poll&so=date&sd=down&l=1",
      dataType: "jsonp",
      success: __bind(function(data) {
        var _a, _b, item, key;
        console.log(data);
        _a = []; _b = data.jsview;
        for (key in _b) {
          if (!__hasProp.call(_b, key)) continue;
          item = _b[key];
          _a.push($(Mustache.to_html(this.template, item)).appendTo("#poll"));
        }
        return _a;
      }, this)
    });
  };
  $(document).ready(function() {
    var p;
    p = new PollProcessor("http://localhost:9991");
    return p.display_items();
  });
})();
