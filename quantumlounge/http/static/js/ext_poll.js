(function() {
  var Poll, PollProcessor;
  var __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  };
  Poll = function(_arg, _arg2, _arg3, _arg4) {
    var _this;
    this.node_id = _arg4;
    this.elem = _arg3;
    this.tapiurl = _arg2;
    this.apiurl = _arg;
    _this = this;
    this.vote = function(){ return Poll.prototype.vote.apply(_this, arguments); };
    this.load_template = function(){ return Poll.prototype.load_template.apply(_this, arguments); };
    $.ajax({
      url: this.apiurl + this.node_id + "?r=jsview&jsview_type=poll&so=date&sd=down&l=1",
      dataType: "jsonp",
      success: __bind(function(data) {
        this.item = data.jsview[0];
        this.item_id = this.item._id;
        return $.ajax({
          url: this.apiurl + this.item._id + ";voted",
          dataType: "jsonp",
          success: __bind(function(data) {
            this.voted = data.voted;
            return this.load_template();
          }, this)
        });
      }, this)
    });
    return this;
  };
  Poll.prototype.content_api = "/api/1/content/";
  Poll.prototype.template_api = "/api/templates/";
  Poll.prototype.load_template = function() {
    var url;
    if (this.voted) {
      url = this.tapiurl + 'entry.poll.results.mustache';
    } else {
      url = this.tapiurl + 'entry.poll.mustache';
    }
    return $.ajax({
      url: url,
      dataType: 'jsonp',
      success: __bind(function(data) {
        this.template = data;
        return (this.voted) ? this.display_results() : this.display_poll();
      }, this)
    });
  };
  Poll.prototype.display_poll = function() {
    var _i, _len, _ref, answer, h, i, new_answers;
    new_answers = [];
    i = 0;
    _ref = this.item.answers;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      answer = _ref[_i];
      new_answers.push({
        'title': "" + answer,
        'no': i
      });
      i = i + 1;
    }
    this.item.answers = new_answers;
    h = $(Mustache.to_html(this.template, this.item));
    $(this.elem).html(h);
    return $("#ql-poll-form-" + this.item._id).change(this.vote);
  };
  Poll.prototype.display_results = function() {
    return $.ajax({
      url: this.apiurl + this.item._id + ";results",
      dataType: "jsonp",
      success: __bind(function(data) {
        var h;
        h = $(Mustache.to_html(this.template, data));
        return $(this.elem).html(h);
      }, this)
    });
  };
  Poll.prototype.vote = function(ev) {
    var aid, data, elem, qid, url;
    elem = ev.target;
    qid = $(elem).attr('data-qid');
    aid = $(elem).attr('data-aid');
    url = this.apiurl + qid + ";vote";
    data = {
      answer_no: aid
    };
    return $.ajax({
      url: url,
      dataType: 'jsonp',
      type: "GET",
      data: data,
      success: __bind(function(data) {
        this.voted = true;
        return this.load_template();
      }, this)
    });
  };
  PollProcessor = function() {
    var _i, _len, _ref, apiurl, elem, node_id, poll, poll_elements, tapiurl;
    this.template = "";
    this.voted = false;
    this.polls = [];
    poll_elements = $(".ql-poll");
    _ref = poll_elements;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      elem = _ref[_i];
      apiurl = $(elem).attr("data-api");
      tapiurl = $(elem).attr("data-tapi");
      node_id = $(elem).attr("data-node");
      poll = new Poll(apiurl, tapiurl, elem, node_id);
      this.polls.push(poll);
    }
    return this;
  };
  $(document).ready(function() {
    var p;
    return (p = new PollProcessor());
  });
}).call(this);
