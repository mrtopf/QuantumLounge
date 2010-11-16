(function() {
  var Item, Processor;
  var __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  };
  Item = function(_b, _c, _d, _e, _f, _g) {
    var _a;
    this.elem = _g;
    this.amount = _f;
    this.type = _e;
    this.templateurl = _d;
    this.apiurl = _c;
    this.baseurl = _b;
    _a = this;
    this.load_template = function(){ return Item.prototype.load_template.apply(_a, arguments); };
    $.ajax({
      url: this.apiurl + "0?r=jsview&jsview_type=" + this.type + "&so=date&sd=down&l=" + this.amount,
      dataType: "jsonp",
      success: __bind(function(data) {
        this.item = data.jsview[0];
        return this.load_template();
      }, this)
    });
    return this;
  };
  Item.prototype.load_template = function() {
    return $.ajax({
      url: this.templateurl,
      dataType: 'jsonp',
      success: __bind(function(data) {
        var h;
        h = $(Mustache.to_html(data, this.item));
        return $(this.elem).html(h);
      }, this)
    });
  };
  Processor = function() {
    var _a, _b, _c, amount, apiurl, baseurl, elem, item, item_elems, templateurl, type;
    this.items = [];
    item_elems = $(".ql-item");
    _b = item_elems;
    for (_a = 0, _c = _b.length; _a < _c; _a++) {
      elem = _b[_a];
      baseurl = $(elem).attr("data-baseurl");
      apiurl = $(elem).attr("data-api");
      templateurl = $(elem).attr("data-template");
      type = $(elem).attr("data-type");
      amount = $(elem).attr("data-amount");
      item = new Item(baseurl, apiurl, templateurl, type, amount, elem);
      this.items.push(item);
    }
    return this;
  };
  $(document).ready(function() {
    var p;
    return (p = new Processor());
  });
})();
