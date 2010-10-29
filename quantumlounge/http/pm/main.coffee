String::startsWith = (str) ->
    r = @match("^"+str)
    if not r
        return false
    (r[0]==str)

CONTENT_API = "/api/1/content/"

TABS = {
    active_name: null       # name of active type
    tab_element: null       # the tab element object containing the tabs
    active: null
    tabs: null
    active_tab: null        # the active tab object (li)
    active_pane: null       # the active pane object
    init: () ->
        TABS.tab_element = $("#tabs")
        TABS.active_tab = TABS.tab_element.children().first()
        TABS.set()
        $("#tabs li > a").click( () ->
            TABS.active_tab.removeClass("current")
            TABS.active_tab = $(this).parent()
            TABS.set()
            return false
        )
    set: () ->
        if (TABS.active_pane)
            TABS.active_pane.slideUp()
        TABS.active_tab.addClass("current")
        mid = TABS.active_tab.children().first().attr("id")
        tabname = mid.slice(4, mid.length)
        TABS.active_name = tabname
        TABS.active_pane = $("#pane-"+tabname)
        TABS.active_pane.slideDown()
}

STATUS = {
    init: () ->

    to_form: (params) ->
        {
            content: params.content
        }


}

LINKS = {
    url: null
    img_idx: 0
    img_url: null
    img_amount: 0
    data: null
    active_image: null

    to_form: (params) ->
        console.log(LINKS.active_image)
        data = {
            content: params.content
            link: params.link
            link_title: LINKS.data.title
            link_description: LINKS.data.content
            link_image: LINKS.active_image
        }
        console.log("sending: "+data)
        data

    process: () ->
        LINKS.data = null
        $("#link-box").slideUp()
        url = $("#link").val()
        if url.length<5
            return false
        console.log(url.startsWith("http://"))
        if not url.startsWith("http://")
            url = "http://"+url
            $("#link").val(url)
        $("#link-submit").text("Loading...")
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
            error: ->
                $("#link-submit").text("Load")
        })
        false

    next_image: () ->
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
        LINKS.active_image = img.thumb.url
        console.log(img)
        console.log(LINKS.active_image)
        $("#link-box-image").attr("src",img.thumb.url)

    init: () ->
        $("#link-submit").click( () ->
            LINKS.process()
        )
        $("#link").keydown( (event) ->
            if event.keyCode == 13
                console.log("ok")
                LINKS.process()
                event.preventDefault()
                false
        )
}

TYPES = {
    link: LINKS
    status: STATUS
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
                    for name, obj of TYPES
                        obj.init()
                    $('#status-content').NobleCount('#status-content-count',{block_negative: true})
                    statuslist = $("#statuslist").detach()
                    @load(base_url+"?r=children&oauth_token="+VAR.token)
                    .then( (context) ->
                        items = @content.children
                        users = _.uniq(_.pluck(items, 'user'))
                        that = this
                        $.ajax({
                            url:'/api/1/users/names'
                            data: JSON.stringify(users)
                            type: 'POST'
                            processData: false
                            contentType: "application/json"
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
        active = TABS.active_name
        active_type = TYPES[active]
        data = active_type.to_form(@params)
        data._type = active
        data.user = VAR.poco.id
        data.oauth_token = VAR.token
        base_url = CONTENT_API+PAGE.id
        $.ajax({
            'url' : base_url
            'type' : 'POST',
            'data' : data,
            'dataType' : 'json',
            'success' : (data, textResponse) ->
                console.log(data)
                data.id = data._id
                data.username = VAR.poco.name.formatted
                data.profile = VAR.poco.thumbnailUrl
                context.render('/pm/templates/entry.'+active+'.mustache', data)
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
