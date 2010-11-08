(function() {
  var CONTENT_API, LINKS, PAGE, STATUS, TABS, TYPES, VAR, app;
  var __hasProp = Object.prototype.hasOwnProperty;
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
  STATUS = {
    init: function() {},
    convert_dates: function(params) {
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
    },
    to_form: function(params) {
      var _a, a, data, v;
      data = {
        content: params.content
      };
      _a = STATUS.convert_dates(params);
      for (a in _a) {
        if (!__hasProp.call(_a, a)) continue;
        v = _a[a];
        data[a] = v;
      }
      console.log(data);
      return data;
    }
  };
  LINKS = {
    url: null,
    img_idx: 0,
    img_url: null,
    img_amount: 0,
    data: null,
    active_image: null,
    to_form: function(params) {
      var data;
      console.log(LINKS.active_image);
      data = {
        content: params.content,
        link: params.link,
        link_title: LINKS.data.title,
        link_description: LINKS.data.content,
        link_image: LINKS.active_image
      };
      if (params.publication_date !== "Today") {
        data.publication_date = params.publication_date;
      }
      if (params.depublication_date !== "Today") {
        data.depublication_date = params.depublication_date;
      }
      return data;
    },
    process: function() {
      var url;
      LINKS.data = null;
      $("#link-box").slideUp();
      url = $("#link").val();
      if (url.length < 5) {
        return false;
      }
      console.log(url.startsWith("http://"));
      if (!url.startsWith("http://")) {
        url = "http://" + url;
        $("#link").val(url);
      }
      $("#link-submit").text("Loading...");
      $.ajax({
        url: VAR.scraper + "?url=" + url,
        dataType: "jsonp",
        success: function(data) {
          LINKS.data = data;
          LINKS.img_amount = data.all_image_urls.length;
          $("#link-box-title").text(data.title);
          $("#link-box-description").text(data.content);
          $("#link-box-url").text(url);
          $("#link-box").slideDown();
          $("#link-submit").text("Load");
          $("#link-box-image-next").click(LINKS.next_image);
          $("#link-box-image-prev").click(LINKS.prev_image);
          return LINKS.set_image(0);
        },
        error: function() {
          return $("#link-submit").text("Load");
        }
      });
      return false;
    },
    next_image: function() {
      var idx;
      idx = LINKS.img_idx;
      idx++;
      if (idx > (LINKS.img_amount - 1)) {
        idx = LINKS.img_amount - 1;
      }
      LINKS.set_image(idx);
      return false;
    },
    prev_image: function() {
      var idx;
      idx = LINKS.img_idx;
      idx--;
      if (idx < 0) {
        idx = 0;
      }
      LINKS.set_image(idx);
      return false;
    },
    set_image: function(idx) {
      var img, imgurl;
      LINKS.img_idx = idx;
      imgurl = LINKS.data.all_image_urls[idx];
      img = LINKS.data.images[imgurl];
      LINKS.active_image = img.thumb.url;
      console.log(img);
      console.log(LINKS.active_image);
      return $("#link-box-image").attr("src", img.thumb.url);
    },
    init: function() {
      $("#link-submit").click(function() {
        return LINKS.process();
      });
      return $("#link").keydown(function(event) {
        if (event.keyCode === 13) {
          console.log("ok");
          LINKS.process();
          event.preventDefault();
          return false;
        }
      });
    }
  };
  TYPES = {
    link: LINKS,
    status: STATUS
  };
  PAGE = {
    id: null,
    render: function(context, content_id) {
      var base_url;
      base_url = CONTENT_API + content_id;
      return $.getJSON(base_url + '?r=parents&oauth_token=' + VAR.token, function(data) {
        return $.getJSON(base_url + '?r=default&oauth_token=' + VAR.token, function(details) {
          if (data.parents.length > 0) {
            data.title = details["default"].content;
          }
          data.parents = data.parents.slice(1, data.parents.length);
          return context.partial('/pm/templates/timeline.mustache', data).then(function() {
            var _a, name, obj, statuslist;
            TABS.init();
            _a = TYPES;
            for (name in _a) {
              if (!__hasProp.call(_a, name)) continue;
              obj = _a[name];
              obj.init();
            }
            $(".dateinput").datepicker({
              dateFormat: 'dd.mm.yy'
            });
            statuslist = $("#statuslist").detach();
            return this.load(base_url + "?r=children&oauth_token=" + VAR.token).then(function(context) {
              var items, that, users;
              items = this.content.children;
              users = _.uniq(_.pluck(items, 'user'));
              that = this;
              return $.ajax({
                url: '/api/1/users/names',
                data: JSON.stringify(users),
                type: 'POST',
                processData: false,
                contentType: "application/json",
                success: function(data) {
                  var res;
                  res = [];
                  _.each(items, function(item) {
                    item.username = data[item.user];
                    return that.render('/pm/templates/entry.' + item._type + '.mustache', item).appendTo(statuslist);
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
      $.ajax({
        'url': base_url,
        'type': 'POST',
        'data': data,
        'dataType': 'json',
        'success': function(data, textResponse) {
          console.log(data);
          data.id = data._id;
          data.username = VAR.poco.name.formatted;
          data.profile = VAR.poco.thumbnailUrl;
          context.render('/pm/templates/entry.' + active + '.mustache', data).then(function(content) {
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
    return $.getJSON('/pm/var', function(data) {
      VAR = data;
      return app.run("#/");
    });
  });
})();
