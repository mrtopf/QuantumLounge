(function() {
  var CONTENT_API, Link, PAGE, Poll, Status, TABS, TYPEDEFS, TYPES, VAR, app;
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
  TABS = {
    active_name: null,
    tab_element: null,
    active: null,
    tabs: null,
    active_tab: null,
    active_pane: null,
    init: function() {
      TABS.tab_element = $("#tabs");
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
      mid = TABS.active_tab.children().first().attr("id");
      tabname = mid.slice(4, mid.length);
      TABS.active_name = tabname;
      TABS.active_pane = $("#pane-" + tabname);
      return TABS.active_pane.slideDown();
    }
  };
  Status = function() {};
  Status.prototype.prepare = function(item) {
    console.log(item._type);
    console.log(item);
    return item;
  };
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
    data = {
      publication_date: publication_date.toString(),
      depublication_date: depublication_date.toString()
    };
    return data;
  };
  Status.prototype.to_form = function(params) {
    var _a, a, data, v;
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
  Link.prototype.to_form = function(params) {
    var _a, a, data, v;
    data = {
      content: params.content,
      link: params.link,
      link_title: this.data.title,
      link_description: this.data.content,
      link_image: this.active_image
    };
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
    console.log("process");
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
    var _a, a, data, v;
    console.log(params);
    data = {
      content: params.content,
      answers: params.poll_answers.split("\n")
    };
    _a = this.convert_dates(params);
    for (a in _a) {
      if (!__hasProp.call(_a, a)) continue;
      v = _a[a];
      data[a] = v;
    }
    console.log(data);
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
          return context.partial('/pm/templates/timeline.mustache', data).then(function() {
            var _a, a, statuslist, v;
            TABS.init();
            _a = TYPEDEFS;
            for (a in _a) {
              if (!__hasProp.call(_a, a)) continue;
              v = _a[a];
              TYPES[a] = new v();
            }
            $(".dateinput").datepicker({
              dateFormat: 'dd.mm.yy'
            });
            statuslist = $("#statuslist").detach();
            return this.load(base_url + ";children?oauth_token=" + VAR.token).then(function(context) {
              var items, that, users;
              items = this.content;
              users = _.uniq(_.pluck(items, 'user'));
              that = this;
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
                    item.username = data[item.user];
                    repr = TYPES[item._type].prepare(item);
                    console.log(repr);
                    console.log("render");
                    that.render('/pm/templates/entry.' + item._type + '.mustache', repr).appendTo(statuslist);
                    return console.log("done");
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
      var active, active_type, base_url, data;
      active = TABS.active_name;
      active_type = TYPES[active];
      data = active_type.to_form(this.params);
      data._type = active;
      data.user = VAR.poco.id;
      data.oauth_token = VAR.token;
      base_url = CONTENT_API + PAGE.id;
      data = JSON.stringify(data);
      $.ajax({
        url: base_url,
        type: 'POST',
        data: data,
        dataType: 'json',
        processData: false,
        contentType: 'application/json',
        success: function(data, textResponse) {
          var repr;
          console.log(data);
          data.id = data._id;
          data.username = VAR.poco.name.formatted;
          data.profile = VAR.poco.thumbnailUrl;
          repr = TYPES[active].prepare(data);
          context.render('/pm/templates/entry.' + active + '.mustache', repr).then(function(content) {
            return $(content).prependTo("#statuslist").slideDown();
          });
          return $(':input', '#entrybox').not(':button, :submit, :reset, :hidden').val('').removeAttr('checked').removeAttr('selected');
        }
      });
      return false;
    });
  });
  VAR = {};
  $(document).ready(function() {
    return $.getJSON(virtual_path + '/pm/var', function(data) {
      CONTENT_API = virtual_path + "/api/1/content/";
      VAR = data;
      return app.run("#/");
    });
  });
})();
