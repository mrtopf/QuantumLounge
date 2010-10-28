(function() {
  var CONTENT_API, LINKS, PAGE, TABS, VAR, app;
  CONTENT_API = "/api/1/content/";
  TABS = {
    active: null,
    tab_elem: null,
    tabs: null,
    active_tab: null,
    init: function() {
      TABS.tab_element = $("#tabs");
      TABS.active = TABS.tab_element.children().first();
      TABS.set();
      return $("#tabs li > a").click(function() {
        TABS.active.removeClass("current");
        TABS.active = $(this).parent();
        TABS.set();
        return false;
      });
    },
    set: function() {
      var mid, tabname;
      if (TABS.active_tab) {
        TABS.active_tab.slideUp();
      }
      TABS.active.addClass("current");
      mid = TABS.active.children().first().attr("id");
      tabname = mid.slice(4, mid.length);
      TABS.active_tab = $("#pane-" + tabname);
      return TABS.active_tab.slideDown();
    }
  };
  LINKS = {
    url: null,
    img_idx: 0,
    img_url: null,
    img_amount: 0,
    data: null,
    process: function() {
      var url;
      LINKS.data = null;
      $("#link-submit").text("Loading...");
      $("#link-box").slideUp();
      url = $("#link").val();
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
        }
      });
      return false;
    },
    next_image: function() {
      var idx;
      console.log("next");
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
      return $("#link-box-image").attr("src", img.thumb.url);
    },
    init: function() {
      $("#link-submit").click(function() {
        return LINKS.process();
      });
      return $("#link").submit(function() {
        return LINKS.process();
      });
    }
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
            var statuslist;
            TABS.init();
            LINKS.init();
            $('#status-content').NobleCount('#status-content-count', {
              block_negative: true
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
      var base_url, p;
      p = {
        content: this.params.content,
        user: VAR.poco.id,
        oauth_token: VAR.token
      };
      base_url = CONTENT_API + PAGE.id;
      $.ajax({
        'url': base_url,
        'type': 'POST',
        'data': p,
        'dataType': 'json',
        'success': function(data, textResponse) {
          data.id = data._id;
          data.username = VAR.poco.name.formatted;
          data.profile = VAR.poco.thumbnailUrl;
          context.render('/pm/templates/entry.mustache', data).then(function(content) {
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
