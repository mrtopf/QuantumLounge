(function() {
  var Item, Processor;
  var __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  };
  Item = function(_a, _b, _c, _d, _e, _f) {
    this.elem = _f;
    this.amount = _e;
    this.type = _d;
    this.templateurl = _c;
    this.apiurl = _b;
    this.baseurl = _a;
    $.ajax({
      url: this.apiurl + "0;query?type=" + this.type + "&so=date&sd=down&l=" + this.amount + "&fmt=html",
      dataType: "jsonp",
      success: __bind(function(data) {
        var e;
        e = $("<div />").html(data.html);
        e.hide();
        $(this.elem).html(e);
        return e.fadeIn();
      }, this)
    });
    return this;
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
