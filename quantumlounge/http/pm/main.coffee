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

class Status


    prepare: (item) ->
        item

    convert_dates: (params) ->
        today = new Date
        publication_date = params.publication_date
        depublication_date = params.depublication_date
        if !publication_date
            publication_date = ""
        else
            s = publication_date.split(".")
            s=s[2]+"-"+s[1]+"-"+s[0]
            publication_date = s
        if !depublication_date
            depublication_date = ""
        else
            s = depublication_date.split(".")
            s=s[2]+"-"+s[1]+"-"+s[0]
            depublication_date = s
        data = {
            publication_date : publication_date.toString()
            depublication_date : depublication_date.toString()
        }
        data

    to_form: (params) ->
        data = {
                content: params.content
            }
        for a,v of @convert_dates(params)
            data[a]=v
        data

class Link extends Status

    constructor: () ->
        @url = null
        @img_idx = 0
        @img_url = null
        @img_amount = 0
        @data = null
        @active_image = null
        $("#link-submit").click( () =>
            @process()
        )
        $("#link").keydown( (event) =>
            if event.keyCode == 13
                @process()
                event.preventDefault()
                false
        )

    to_form: (params) ->
        data = {
            content: params.content
            link: params.link
            link_title: @data.title
            link_description: @data.content
            link_image: @active_image
        }
        for a,v of @convert_dates(params)
            data[a]=v
        data

    process: () ->
        console.log("process")
        @data = null
        $("#link-box").slideUp()
        url = $("#link").val()
        if url.length<5
            return false
        if not url.startsWith("http://")
            url = "http://"+url
            $("#link").val(url)
        $("#link-submit").text("Loading...")
        $.ajax({
            url: VAR.scraper+"?url="+url
            dataType: "jsonp"
            success: (data) =>
                @data = data
                @img_amount = data.all_image_urls.length
                $("#link-box-title").text(data.title)
                $("#link-box-description").text(data.content)
                $("#link-box-url").text(url)
                $("#link-box").slideDown()
                $("#link-submit").text("Load")
                $("#link-box-image-next").click(@next_image)
                $("#link-box-image-prev").click(@prev_image)
                @set_image(0)
            error: ->
                $("#link-submit").text("Load")
        })
        false

    next_image: () =>
        idx = @img_idx
        idx++
        if idx>(@img_amount-1)
            idx= @img_amount-1
        @set_image(idx)
        false

    prev_image: () =>
        idx = @img_idx
        idx--
        if idx<0
            idx= 0
        @set_image(idx)
        false

    set_image: (idx) =>
        @img_idx = idx
        imgurl = @data.all_image_urls[idx]
        img = @data.images[imgurl]
        @active_image = img.thumb.url
        $("#link-box-image").attr("src",img.thumb.url)

class Poll extends Status

    to_form: (params) ->
        console.log(params)
        data = {
            content: params.content
            answers: params.poll_answers.split("\n")
        }
        for a,v of @convert_dates(params)
            data[a]=v
        console.log(data)
        data

    prepare: (item) ->
        answers = item.answers
        new_answers = []
        for a in answers
            new_answers.push({title: a})
        item.answers = new_answers
        item

TYPES = {
    status: Status
    link: Link
    poll: Poll
    folder: Status
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
                    for a,v of TYPES
                        TYPES[a] = new v
                    $( ".dateinput" ).datepicker({dateFormat: 'dd.mm.yy'});
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
                                    repr = TYPES[item._type].prepare(item)
                                    that.render('/pm/templates/entry.'+item._type+'.mustache', repr)
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
        data = JSON.stringify(data)
        $.ajax({
            url : base_url
            type : 'POST'
            data : data
            dataType : 'json'
            processData : false
            contentType: 'application/json'
            success : (data, textResponse) ->
                console.log(data)
                data.id = data._id
                data.username = VAR.poco.name.formatted
                data.profile = VAR.poco.thumbnailUrl
                repr = TYPES[active].prepare(data)
                context.render('/pm/templates/entry.'+active+'.mustache', repr)
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
