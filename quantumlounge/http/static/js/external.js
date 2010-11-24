(function() {
  var Item, Processor;
  var __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  };
  Item = function(_a, _b, _c, _d, _e, _f, _g) {
    this.elem = _g;
    this.amount = _f;
    this.type = _e;
    this.templateurl = _d;
    this.apiurl = _c;
    this.node_id = _b;
    this.baseurl = _a;
    $.ajax({
      url: this.apiurl + this.node_id + ";query?type=" + this.type + "&so=date&sd=down&l=" + this.amount + "&fmt=html",
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
    var _a, _b, _c, amount, apiurl, baseurl, elem, item, item_elems, node_id, templateurl, type;
    this.items = [];
    item_elems = $(".ql-item");
    _b = item_elems;
    for (_a = 0, _c = _b.length; _a < _c; _a++) {
      elem = _b[_a];
      baseurl = $(elem).attr("data-baseurl");
      apiurl = $(elem).attr("data-api");
      node_id = $(elem).attr("data-node");
      if (!node_id) {
        node_id = "0";
      }
      templateurl = $(elem).attr("data-template");
      type = $(elem).attr("data-type");
      amount = $(elem).attr("data-amount");
      item = new Item(baseurl, node_id, apiurl, templateurl, type, amount, elem);
      this.items.push(item);
    }
    return this;
  };
  $(document).ready(function() {
    var p;
    return (p = new Processor());
  });
})();
