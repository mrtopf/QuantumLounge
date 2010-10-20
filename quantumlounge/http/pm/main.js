(function() {
  var CONTENT_API, VAR, app, status;
  status = {
    active: 'note'
  };
  CONTENT_API = "/api/1/tweets/";
  app = $.sammy(function() {
    this.element_selector = '#content';
    this.use(Sammy.Mustache, 'tmpl');
    this.use(Sammy.JSON);
    this.use(Sammy.Title);
    this.get('#/', function(context) {
      return this.partial('/pm/templates/timeline.tmpl').then(function() {
        $('#status-content').NobleCount('#status-content-count', {
          block_negative: true
        });
        return this.load(CONTENT_API).then(function(context) {
          var items, that, users;
          users = _.uniq(_.pluck(this.content, 'user'));
          items = this.content;
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
              return that.renderEach('/pm/templates/entry.tmpl', items).appendTo("#statuslist");
            }
          });
        });
      });
    });
    return this.post('#/submit', function(context) {
      var p;
      p = {
        content: this.params.content,
        user: VAR.poco.id
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
          context.render('/pm/templates/entry.tmpl', data).then(function(content) {
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
      console.log(data);
      return app.run("#/");
    });
  });
})();
