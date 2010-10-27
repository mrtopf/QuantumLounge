(function() {
  var CONTENT_API, VAR, app;
  CONTENT_API = "/api/1/content/0?r=children";
  app = $.sammy(function() {
    this.element_selector = '#content';
    this.use(Sammy.Mustache, 'mustache');
    this.use(Sammy.JSON);
    this.use(Sammy.Title);
    this.get('#/', function(context) {
      return $.getJSON('/api/1/content/17456c03-ba37-4ca6-8925-a906678bc79d?r=parents', function(data) {
        data.parents = data.parents.slice(1, data.parents.length);
        return $.getJSON('/api/1/content/17456c03-ba37-4ca6-8925-a906678bc79d?r=default', function(details) {
          data.title = details["default"].content;
          return context.partial('/pm/templates/timeline.mustache', data).then(function() {
            $('#status-content').NobleCount('#status-content-count', {
              block_negative: true
            });
            return this.load(CONTENT_API).then(function(context) {
              var items, that, users;
              console.log("ok");
              items = this.content.children;
              console.log(items);
              users = _.uniq(_.pluck(items, 'user'));
              that = this;
              return $.ajax({
                url: '/api/1/users/names',
                data: JSON.stringify(users),
                type: 'POST',
                processData: false,
                contentType: "application/json",
                success: function(data) {
                  items = _.map(items, function(item) {
                    item.username = data[item.user];
                    return item;
                  });
                  return that.renderEach('/pm/templates/entry.mustache', items).appendTo("#statuslist");
                }
              });
            });
          });
        });
      });
    });
    return this.post('#/submit', function(context) {
      var p;
      p = {
        content: this.params.content,
        user: VAR.poco.id,
        oauth_token: VAR.token
      };
      $.ajax({
        'url': CONTENT_API,
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
