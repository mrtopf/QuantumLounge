(function() {
  var PollProcessor;
  var __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  };
  PollProcessor = function(_b) {
    var _a;
    this.baseurl = _b;
    _a = this;
    this.vote = function(){ return PollProcessor.prototype.vote.apply(_a, arguments); };
    this.load_template = function(){ return PollProcessor.prototype.load_template.apply(_a, arguments); };
    this.template = "";
    this.voted = false;
    $.ajax({
      url: this.baseurl + this.content_api + "0?r=jsview&jsview_type=poll&so=date&sd=down&l=1",
      dataType: "jsonp",
      success: __bind(function(data) {
        this.item = data.jsview[0];
        this.item_id = this.item._id;
        return $.ajax({
          url: this.baseurl + this.content_api + this.item._id + ";voted",
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
  PollProcessor.prototype.content_api = "/api/1/content/";
  PollProcessor.prototype.template_api = "/api/templates/";
  PollProcessor.prototype.load_template = function() {
    var url;
    if (this.voted) {
      url = this.baseurl + this.template_api + 'entry.poll.results.mustache';
    } else {
      url = this.baseurl + this.template_api + 'entry.poll.mustache';
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
  PollProcessor.prototype.display_poll = function() {
    var _a, _b, _c, answer, h, i, new_answers;
    new_answers = [];
    i = 0;
    _b = this.item.answers;
    for (_a = 0, _c = _b.length; _a < _c; _a++) {
      answer = _b[_a];
      new_answers.push({
        title: answer,
        no: i
      });
      i = i + 1;
    }
    this.item.answers = new_answers;
    h = $(Mustache.to_html(this.template, this.item));
    $("#poll").html(h);
    return $(".ql-poll-box").change(this.vote);
  };
  PollProcessor.prototype.display_results = function() {
    return $.ajax({
      url: this.baseurl + this.content_api + this.item._id + ";results",
      dataType: "jsonp",
      success: __bind(function(data) {
        var h;
        h = $(Mustache.to_html(this.template, data));
        return $("#poll").html(h);
      }, this)
    });
  };
  PollProcessor.prototype.vote = function(ev) {
    var aid, data, elem, qid, url;
    elem = ev.target;
    qid = $(elem).attr('data-qid');
    aid = $(elem).attr('data-aid');
    url = this.baseurl + this.content_api + qid + ";vote";
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
  $(document).ready(function() {
    var p;
    return (p = new PollProcessor("http://localhost:9991"));
  });
})();
