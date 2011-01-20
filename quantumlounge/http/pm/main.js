(function() {
  var CONTENT_API, ERROR, Link, PAGE, Poll, Status, TABS, TEMPLATES, TYPEDEFS, TYPES, VAR, app;
  var __hasProp = Object.prototype.hasOwnProperty, __bind = function(func, context) {
    return function(){ return func.apply(context, arguments); };
  }, __extends = function(child, parent) {
    var ctor = function(){};
    ctor.prototype = parent.prototype;
    child.prototype = new ctor();
    child.prototype.constructor = child;
    if (typeof parent.extended === "function") parent.extended(child);
    child.__super__ = parent.prototype;
  };
  String.prototype.startsWith = function(str) {
    var r;
    r = this.match("^" + str);
    if (!r) {
      return false;
    }
    return r[0] === str;
  };
  CONTENT_API = "/api/1/content/";
  TEMPLATES = "/pm/templates/";
  ERROR = {
    status: false,
    on: function() {
      return $("#error").animate({
        top: -8
      }, 200, function() {
        return (ERROR.status = true);
      });
    },
    off: function() {
      return $("#error").animate({
        top: -68
      }, 200, function() {
        return (ERROR.status = false);
      });
    },
    error: function(msg) {
      $("#error-message").text(msg + "");
      ERROR.on();
      $("#error .closebutton").click(function() {
        ERROR.off();
        return false;
      });
      setTimeout(function() {
        return ERROR.off();
      }, 5000);
      return $(document).keyup(function(e) {
        return e.keyCode === 27 ? ERROR.off() : null;
      });
    }
  };
  TABS = {
    active_name: null,
    tab_element: null,
    active: null,
    tabs: null,
    active_tab: null,
    active_pane: null,
    init: function(_subtypes) {
      var _a, _b, _c, _d, _e, _type, alltabs, tab;
      if (_subtypes) {
        alltabs = $("#tabs").children();
        _b = alltabs;
        for (_a = 0, _c = _b.length; _a < _c; _a++) {
          tab = _b[_a];
          _type = $(tab).attr("data-type");
          if (!(function(){ for (var _d=0, _e=_subtypes.length; _d<_e; _d++) { if (_subtypes[_d] === _type) return true; } return false; }).call(this)) {
            $("#tab-" + _type).remove();
          }
        }
      }
      TABS.tab_element = $("#tabs");
      if (TABS.tab_element.children().length === 0) {
        $("#entryarea").remove();
        return false;
      }
      TABS.active_tab = TABS.tab_element.children().first();
      TABS.set();
      return $("#tabs li > a").click(function() {
        TABS.active_tab.removeClass("current");
        TABS.active_tab = $(this).parent();
        TABS.set();
        return false;
      });
    },
    set: function() {
      var mid, tabname;
      if (TABS.active_pane) {
        TABS.active_pane.slideUp();
      }
      TABS.active_tab.addClass("current");
      mid = TABS.active_tab.attr("id");
      tabname = mid.slice(4, mid.length);
      TABS.active_name = tabname;
      TABS.active_pane = $("#pane-" + tabname);
      return TABS.active_pane.slideDown();
    }
  };
  Status = function() {};
  Status.prototype.prepare = function(item) {
    var d, d1, d2, effective;
    item.meta = {
      user: item.user,
      id: item._id
    };
    if (item.date) {
      d = item.date.slice(0, 19);
      d = $D(d);
      item.meta.date = d.strftime("%d.%m.%y");
    } else {
      item.meta.date = "n/a";
    }
    effective = "";
    if (item.publication_date && !item.depublication_date) {
      d = $D(item.publication_date.slice(0, 19));
      effective = d.strftime("%d.%m.%Y -");
    }
    if (item.depublication_date && !item.publication_date) {
      d = $D(item.depublication_date.slice(0, 19));
      effective = d.strftime("- %d.%m.%Y");
    }
    if (item.depublication_date && item.publication_date) {
      d1 = $D(item.publication_date.slice(0, 19));
      d2 = $D(item.depublication_date.slice(0, 19));
      effective = d1.strftime("%d.%m.%Y") + " - " + d2.strftime("%d.%m.%Y");
    }
    if (effective) {
      item.meta.effective = "Published: " + effective;
    }
    return item;
  };
  Status.prototype.reset = function() {};
  Status.prototype.convert_dates = function(params) {
    var data, depublication_date, publication_date, s, today;
    today = new Date();
    publication_date = params.publication_date;
    depublication_date = params.depublication_date;
    if (!publication_date) {
      publication_date = "";
    } else {
      s = publication_date.split(".");
      s = s[2] + "-" + s[1] + "-" + s[0];
      publication_date = s;
    }
    if (!depublication_date) {
      depublication_date = "";
    } else {
      s = depublication_date.split(".");
      s = s[2] + "-" + s[1] + "-" + s[0];
      depublication_date = s;
    }
    if (publication_date !== "" && depublication_date !== "") {
      if (depublication_date < publication_date) {
        throw "Publication Date must be earlier than depublication\
            date";
      }
    }
    data = {
      publication_date: publication_date.toString(),
      depublication_date: depublication_date.toString()
    };
    return data;
  };
  Status.prototype.to_form = function(params) {
    var _a, a, data, v;
    if (params.content === "") {
      throw "Please enter a status message";
    }
    data = {
      content: params.content
    };
    _a = this.convert_dates(params);
    for (a in _a) {
      if (!__hasProp.call(_a, a)) continue;
      v = _a[a];
      data[a] = v;
    }
    return data;
  };
  Link = function() {
    var _a;
    _a = this;
    this.set_image = function(){ return Link.prototype.set_image.apply(_a, arguments); };
    this.prev_image = function(){ return Link.prototype.prev_image.apply(_a, arguments); };
    this.next_image = function(){ return Link.prototype.next_image.apply(_a, arguments); };
    this.url = null;
    this.img_idx = 0;
    this.img_url = null;
    this.img_amount = 0;
    this.data = null;
    this.active_image = null;
    $("#link-submit").click(__bind(function() {
      return this.process();
    }, this));
    $("#link").keydown(__bind(function(event) {
      if (event.keyCode === 13) {
        this.process();
        event.preventDefault();
        return false;
      }
    }, this));
    return this;
  };
  __extends(Link, Status);
  Link.prototype.reset = function() {
    Link.__super__.reset.apply(this, arguments);
    $("#link-box").slideUp();
    $("#link-box-title").text("");
    $("#link-box-description").text("");
    $("#link-box-url").text("");
    return $("#link-submit").text("Load");
  };
  Link.prototype.to_form = function(params) {
    var _a, a, data, v;
    data = {
      content: params.content,
      link: params.link
    };
    if (params.link === "") {
      throw "Well, you have to enter a link actually";
    }
    if (this.data) {
      data.link_title = this.data.title;
      data.link_description = this.data.content;
      data.link_image = this.active_image;
    } else {
      data.link_title = params.link;
    }
    _a = this.convert_dates(params);
    for (a in _a) {
      if (!__hasProp.call(_a, a)) continue;
      v = _a[a];
      data[a] = v;
    }
    return data;
  };
  Link.prototype.process = function() {
    var url;
    this.data = null;
    $("#link-box").slideUp();
    url = $("#link").val();
    if (url.length < 5) {
      return false;
    }
    if (!url.startsWith("http://")) {
      url = "http://" + url;
      $("#link").val(url);
    }
    $("#link-submit").text("Loading...");
    $.ajax({
      url: VAR.scraper + "?url=" + url,
      dataType: "jsonp",
      success: __bind(function(data) {
        if (data.error) {
          $("#link-submit").text("Cannot load!");
          setTimeout(function() {
            return $("#link-submit").text("Load");
          }, 2000);
          return null;
        }
        this.data = data;
        this.img_amount = data.all_image_urls.length;
        $("#link-box-title").text(data.title);
        $("#link-box-description").text(data.content);
        $("#link-box-url").text(url);
        $("#link-box").slideDown();
        $("#link-submit").text("Load");
        $("#link-box-image-next").click(this.next_image);
        $("#link-box-image-prev").click(this.prev_image);
        return this.set_image(0);
      }, this),
      error: function() {
        return $("#link-submit").text("Load");
      }
    });
    return false;
  };
  Link.prototype.next_image = function() {
    var idx;
    idx = this.img_idx;
    idx++;
    if (idx > (this.img_amount - 1)) {
      idx = this.img_amount - 1;
    }
    this.set_image(idx);
    return false;
  };
  Link.prototype.prev_image = function() {
    var idx;
    idx = this.img_idx;
    idx--;
    if (idx < 0) {
      idx = 0;
    }
    this.set_image(idx);
    return false;
  };
  Link.prototype.set_image = function(idx) {
    var img, imgurl;
    if (this.img_amount === 0) {
      $("#imageselector").hide();
      $("#link-box-image-container").hide();
      return null;
    }
    $("#imageselector").show();
    $("#link-box-image-container").show();
    this.img_idx = idx;
    imgurl = this.data.all_image_urls[idx];
    img = this.data.images[imgurl];
    this.active_image = img.thumb.url;
    return $("#link-box-image").attr("src", img.thumb.url);
  };
  Poll = function() {
    return Status.apply(this, arguments);
  };
  __extends(Poll, Status);
  Poll.prototype.to_form = function(params) {
    var _a, _b, _c, _d, a, answers, data, line, v;
    if (params.content === "") {
      throw "Please enter a poll title";
    }
    if (params.poll_answers === "") {
      throw "Please enter some answers";
    }
    answers = [];
    _b = params.poll_answers.split("\n");
    for (_a = 0, _c = _b.length; _a < _c; _a++) {
      line = _b[_a];
      if (line !== "") {
        answers.push(line);
      }
    }
    data = {
      content: params.content,
      answers: answers
    };
    _d = this.convert_dates(params);
    for (a in _d) {
      if (!__hasProp.call(_d, a)) continue;
      v = _d[a];
      data[a] = v;
    }
    return data;
  };
  TYPEDEFS = {
    status: Status,
    link: Link,
    poll: Poll,
    folder: Status
  };
  TYPES = {};
  PAGE = {
    id: null,
    render: function(context, content_id) {
      var base_url;
      base_url = CONTENT_API + content_id;
      return $.getJSON(base_url + ';parents?oauth_token=' + VAR.token, function(parents) {
        return $.getJSON(base_url + ';default?oauth_token=' + VAR.token, function(details) {
          var data;
          data = {};
          if (parents.length > 0) {
            data.title = details.content;
          }
          data.parents = parents.slice(1, parents.length);
          data.virtual_path = virtual_path;
          return context.partial(TEMPLATES + 'timeline.mustache', data).then(function() {
            var _a, a, statuslist, v;
            TABS.init(details._subtypes);
            _a = TYPEDEFS;
            for (a in _a) {
              if (!__hasProp.call(_a, a)) continue;
              v = _a[a];
              TYPES[a] = new v();
            }
            $(".dateinput").datepicker({
              dateFormat: 'dd.mm.yy'
            });
            $("#depubdate-remove").click(function() {
              $("#depublication-date").val("");
              return false;
            });
            $("#pubdate-remove").click(function() {
              $("#publication-date").val("");
              return false;
            });
            $(".item-removebutton").live('click', function() {
              var node_id;
              node_id = $(this).attr("data-nodeid");
              $.ajax({
                url: virtual_path + '/api/1/content/' + node_id,
                type: 'DELETE',
                data: JSON.stringify({
                  oauth_token: VAR.token
                }),
                processData: false,
                contentType: "application/json",
                success: function(data) {
                  var node;
                  node = $("#a-" + node_id);
                  node.css({
                    'background-color': 'red'
                  });
                  return node.fadeOut();
                }
              });
              return false;
            });
            statuslist = $("#statuslist").detach();
            statuslist.hide();
            return this.load(base_url + ";children?oauth_token=" + VAR.token, {
              cache: false
            }).then(function(context) {
              var items, that, users;
              items = this.content;
              users = _.uniq(_.pluck(items, 'user'));
              that = this;
              setTimeout(function() {
                return statuslist.fadeIn();
              }, 300);
              return $.ajax({
                url: virtual_path + '/api/1/users/names',
                data: JSON.stringify(users),
                type: 'POST',
                processData: false,
                contentType: "application/json",
                success: function(data) {
                  var res;
                  res = [];
                  _.each(items, function(item) {
                    var repr;
                    repr = TYPES[item._type].prepare(item);
                    repr.meta.username = data[item.user];
                    return that.render(TEMPLATES + 'meta.mustache', repr.meta).then(function(context2) {
                      return (repr.meta = context2);
                    }).render(TEMPLATES + 'entry.' + item._type + '.mustache', repr).appendTo(statuslist);
                  });
                  return statuslist.appendTo("#timeline");
                }
              });
            });
          });
        });
      });
    },
    set_id: function(id) {
      return (PAGE.id = id);
    }
  };
  app = $.sammy(function() {
    this.element_selector = '#content';
    this.use(Sammy.Mustache, 'mustache');
    this.use(Sammy.JSON);
    this.use(Sammy.Title);
    this.get('#/', function(context) {
      PAGE.render(context, content_id);
      return PAGE.set_id(content_id);
    });
    this.get('#/:id', function(context) {
      PAGE.render(context, this.params.id);
      return PAGE.set_id(this.params.id);
    });
    return this.post('#/submit', function(context) {
      var active, active_type, base_url, data, that;
      active = TABS.active_name;
      active_type = TYPES[active];
      try {
        data = active_type.to_form(this.params);
      } catch (error) {
        ERROR.error(error);
        false;
      }
      data._type = active;
      data.user = VAR.poco.id;
      data.oauth_token = VAR.token;
      base_url = CONTENT_API + PAGE.id;
      data = JSON.stringify(data);
      ERROR.off();
      that = this;
      $.ajax({
        url: base_url,
        type: 'POST',
        data: data,
        dataType: 'json',
        processData: false,
        contentType: 'application/json',
        success: function(data, textResponse) {
          var repr;
          if (!data.error) {
            data.id = data._id;
            data.username = VAR.poco.name.formatted;
            data.profile = VAR.poco.thumbnailUrl;
            repr = TYPES[active].prepare(data);
            repr.meta.username = data['username'];
            that.render(TEMPLATES + 'meta.mustache', repr.meta).then(function(context2) {
              return (repr.meta = context2);
            }).render(TEMPLATES + 'entry.' + active + '.mustache', repr).then(function(content) {
              var a;
              a = $("<div/>").html(content);
              a.hide();
              a.prependTo("#statuslist");
              a.slideDown();
              return TYPES[active].reset();
            });
            return $(':input', '#entrybox').not(':button, :submit, :reset, :hidden').val('').removeAttr('checked').removeAttr('selected');
          } else {
            return ERROR.error(data.error_msg);
          }
        }
      });
      return false;
    });
  });
  VAR = {};
  $(document).ready(function() {
    return $.getJSON(virtual_path + '/pm/var', function(data) {
      CONTENT_API = virtual_path + "/api/1/content/";
      TEMPLATES = virtual_path + "/pm/templates/";
      VAR = data;
      return app.run("#/");
    });
  });
})();
