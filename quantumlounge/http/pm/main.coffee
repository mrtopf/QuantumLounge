
CONTENT_API = "/api/1/content/"

TABS = {
    active: null
    tab_elem: null
    tabs: null
    active_tab: null
    init: () ->
        TABS.tab_element = $("#tabs")
        TABS.active = TABS.tab_element.children().first()
        TABS.set()
        $("#tabs li > a").click( () ->
            TABS.active.removeClass("current")
            TABS.active = $(this).parent()
            TABS.set()
            return false
        )
    set: () ->
        if (TABS.active_tab)
            TABS.active_tab.slideUp()
        TABS.active.addClass("current")
        mid = TABS.active.children().first().attr("id")
        tabname = mid.slice(4, mid.length)
        TABS.active_tab = $("#pane-"+tabname)
        TABS.active_tab.slideDown()
}

LINKS = {
    url: null
    img_idx: 0
    img_url: null
    img_amount: 0
    data: null
    process: () ->
        LINKS.data = null
        $("#link-submit").text("Loading...")
        $("#link-box").slideUp()
        url = $("#link").val()
        $.ajax({
            url: VAR.scraper+"?url="+url
            dataType: "jsonp"
            success: (data) ->
                LINKS.data = data
                LINKS.img_amount = data.all_image_urls.length
                $("#link-box-title").text(data.title)
                $("#link-box-description").text(data.content)
                $("#link-box-url").text(url)
                $("#link-box").slideDown()
                $("#link-submit").text("Load")
                $("#link-box-image-next").click(LINKS.next_image)
                $("#link-box-image-prev").click(LINKS.prev_image)
                LINKS.set_image(0)
        })
        false

    next_image: () ->
        console.log("next")
        idx = LINKS.img_idx
        idx++
        if idx>(LINKS.img_amount-1)
            idx= LINKS.img_amount-1
        LINKS.set_image(idx)
        false

    prev_image: () ->
        idx = LINKS.img_idx
        idx--
        if idx<0
            idx= 0
        LINKS.set_image(idx)
        false

    set_image: (idx) ->
        LINKS.img_idx = idx
        imgurl = LINKS.data.all_image_urls[idx]
        img = LINKS.data.images[imgurl]
        $("#link-box-image").attr("src",img.thumb.url)

    init: () ->
        $("#link-submit").click( () ->
            LINKS.process()
        )
        $("#link").submit( () ->
            LINKS.process()
        )
}

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
                    TABS.init()
                    LINKS.init()
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
