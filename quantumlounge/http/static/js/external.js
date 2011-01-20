(function() {
  var Item, Processor;
  var __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  };
  Item = function(_arg, _arg2, _arg3, _arg4, _arg5, _arg6, _arg7) {
    this.elem = _arg7;
    this.amount = _arg6;
    this.type = _arg5;
    this.templateurl = _arg4;
    this.apiurl = _arg3;
    this.node_id = _arg2;
    this.baseurl = _arg;
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
    var _i, _len, _ref, amount, apiurl, baseurl, elem, item, item_elems, node_id, templateurl, type;
    this.items = [];
    item_elems = $(".ql-item");
    _ref = item_elems;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      elem = _ref[_i];
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
}).call(this);
