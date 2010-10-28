
CONTENT_API = "/api/1/content/"

PAGE = {
    id: null,
    render: (context, content_id) ->
        base_url = CONTENT_API+content_id
        $.getJSON(base_url+'?r=parents&oauth_token='+VAR.token, (data) ->
            $.getJSON(base_url+'?r=default&oauth_token='+VAR.token, (details) ->
                if (data.parents.length>0)
                    data.title = details.default.content
                # remove root node
                data.parents = data.parents.slice(1, data.parents.length)
                context.partial('/pm/templates/timeline.mustache', data)
                .then(() ->
                    $('#status-content').NobleCount('#status-content-count',{block_negative: true})
                    statuslist = $("#statuslist").detach()
                    @load(base_url+"?r=children&oauth_token="+VAR.token)
                    .then( (context) ->
                        items = @content.children
                        users = _.uniq(_.pluck(items, 'user'))
                        that = this
                        $.ajax({
                            url:'/api/1/users/names',
                            data: JSON.stringify(users),
                            type: 'POST',
                            processData: false,
                            contentType: "application/json",
                            success: (data) ->
                                res = []
                                _.each(items, (item) ->
                                    item.username = data[item.user]
                                    that.render('/pm/templates/entry.'+item._type+'.mustache', item)
                                    .appendTo(statuslist)
                                )
                                statuslist.appendTo("#timeline")
                        })
                    )
                )
            )
        )
    set_id: (id) ->
        PAGE.id = id

}

app = $.sammy(
    ->
      @element_selector = '#content'
      @use(Sammy.Mustache,'mustache')
      @use(Sammy.JSON)
      @use(Sammy.Title)

      @get('#/', (context) ->
          PAGE.render(context, content_id)
          PAGE.set_id(content_id)
      )

      @get('#/:id', (context) ->
          PAGE.render(context, @params.id)
          PAGE.set_id(@params.id)
      )

      @post('#/submit', (context) ->
        # call some view or so which returns the payload 
        p = {
            content : @params.content,
            user : VAR.poco.id,
            oauth_token : VAR.token
        }
        base_url = CONTENT_API+PAGE.id
        $.ajax({
            'url' : base_url
            'type' : 'POST',
            'data' : p,
            'dataType' : 'json',
            'success' : (data, textResponse) ->
                data.id = data._id
                data.username = VAR.poco.name.formatted
                data.profile = VAR.poco.thumbnailUrl
                context.render('/pm/templates/entry.mustache', data)
                .then( (content) ->
                    $(content).prependTo("#statuslist")
                    .slideDown()
                )
                $(':input','#entrybox')
                 .not(':button, :submit, :reset, :hidden')
                 .val('')
                 .removeAttr('checked')
                 .removeAttr('selected')
        })
        false
      )
)

VAR = {}

$(document).ready(
  ->
    $.getJSON('/pm/var', (data) ->
        VAR = data
        app.run("#/")
    )
)
