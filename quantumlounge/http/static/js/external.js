(function() {
  var CONTENT_API, Processor;
  var __hasProp = Object.prototype.hasOwnProperty, __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  };
  CONTENT_API = "/api/1/content/";
  Processor = function(_a) {
    this.baseurl = _a;
    return this;
  };
  Processor.prototype.templates = ['link', 'status'];
  Processor.prototype.tmpls = {
    link: '<div class="activity" id="a-{{id}}">\n    <div class="body">\n        {{content}}\n        <div class="link-info">\n            <img class="link-box-image" src="{{link_image}}" />\n            <strong class="link-box-title"><a href="{{link_url}}">{{link_title}}</a></strong>\n            <div class="link-box-description">{{link_description}}</div>\n        </div>\n    </div>\n</div>',
    status: '<div class="activity" id="a-{{ id }}">\n    <div class="body">\n        {{ content }}\n    </div>\n</div>'
  };
  Processor.prototype.display_items = function() {
    return $.ajax({
      url: "http://localhost:9991/api/1/content/0?r=jsview&jsview_type=link&so=date&sd=down",
      dataType: "jsonp",
      success: __bind(function(data) {
        var _a, _b, item, key, t;
        console.log("ok");
        console.log(data);
        _a = []; _b = data.jsview;
        for (key in _b) {
          if (!__hasProp.call(_b, key)) continue;
          item = _b[key];
          _a.push((function() {
            t = this.tmpls[item._type];
            return $(Mustache.to_html(t, item)).appendTo("#jsview");
          }).call(this));
        }
        return _a;
      }, this)
    });
  };
  $(document).ready(function() {
    var p;
    p = new Processor("http://localhost:9991");
    return p.display_items();
  });
})();
