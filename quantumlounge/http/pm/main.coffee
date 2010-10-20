status = {
    active: 'note'
}

CONTENT_API = "/api/1/tweets/"

app = $.sammy(
    ->
      @element_selector = '#content'
      @use(Sammy.Mustache,'tmpl')
      @use(Sammy.JSON)
      @use(Sammy.Title)
      
      @get('#/', (context) ->
          @partial('/pm/templates/timeline.tmpl')
          .then(() ->
            $('#status-content').NobleCount('#status-content-count',{block_negative: true})
            @load(CONTENT_API)
            .then( (context) ->
                users = _.uniq(_.pluck(@content, 'user'))
                items = @content
                that = this
                $.ajax({
                    url:'/api/1/users/names',
                    data: JSON.stringify(users), 
                    type: 'POST',
                    processData: false,
                    contentType: "application/json",
                    success: (data) ->
                        items = _.map(items, (item) ->
                            item.username = data[item.user]
                            return item
                        )
                        that.renderEach('/pm/templates/entry.tmpl', items)
                        .appendTo("#statuslist")
                })
                    
                
            )
          )
      )
      @post('#/submit', (context) ->
        p = {
            content : @params.content,
            user : VAR.poco.id
        }
        $.ajax({
            'url' : CONTENT_API,
            'type' : 'POST',
            'data' : p,
            'dataType' : 'json',
            'success' : (data, textResponse) ->
                data.id = data._id
                data.username = VAR.poco.name.formatted;
                data.profile = VAR.poco.thumbnailUrl;
                context.render('/pm/templates/entry.tmpl', data)
                .then( (content) ->
                    $(content).prependTo("#statuslist")
                    .slideDown()
                )
                $(':input','#entrybox')
                 .not(':button, :submit, :reset, :hidden')
                 .val('')
                 .removeAttr('checked')
                 .removeAttr('selected');
        })
        false
      )
)

VAR = {}

$(document).ready(
  ->
    $.getJSON('/pm/var', (data) ->
        VAR = data
        console.log(data)
        app.run("#/")
    )
)
  
