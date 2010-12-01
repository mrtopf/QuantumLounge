String::startsWith = (str) ->
    r = @match("^"+str)
    if not r
        return false
    (r[0]==str)

CONTENT_API = "/api/1/content/"
TEMPLATES = "/pm/templates/"

ERROR = {
    status: false
    on: () ->
        $("#error").animate({
            top: -8
        },200, () -> ERROR.status=true)
    off: () ->
        $("#error").animate({
            top: -68
        },200, () -> ERROR.status=false)
    error: (msg) ->
        $("#error-message").text(msg+"")
        ERROR.on()
        $("#error .closebutton").click( () ->
            ERROR.off()
            false
        )
        setTimeout( () ->
                ERROR.off()
            , 5000)
        $(document).keyup( (e) ->
            if e.keyCode == 27
                ERROR.off()
        )
}

TABS = {
    active_name: null       # name of active type
    tab_element: null       # the tab element object containing the tabs
    active: null
    tabs: null
    active_tab: null        # the active tab object (li)
    active_pane: null       # the active pane object
    init: (_subtypes) ->
        # remove tabs which are not allowed
        if _subtypes
            alltabs = $("#tabs").children()
            for tab in alltabs
                _type = $(tab).attr("data-type")
                if _type not in _subtypes
                    $("#tab-"+_type).remove()

        TABS.tab_element = $("#tabs")
        if TABS.tab_element.children().length==0
            $("#entryarea").remove()
            return false
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
        mid = TABS.active_tab.attr("id")
        tabname = mid.slice(4, mid.length)
        TABS.active_name = tabname
        TABS.active_pane = $("#pane-"+tabname)
        TABS.active_pane.slideDown()
}

class Status

    prepare: (item) ->
        item.meta = {
            user: item.user
        }
        if item.date
            d = item.date.slice(0,19)
            d = $D(d)
            item.meta.date = d.strftime("%d.%m.%y")
        else
            item.meta.date = "n/a"
        effective = ""
        if item.publication_date and not item.depublication_date
            d = $D(item.publication_date.slice(0,19))
            effective = d.strftime("%d.%m.%Y -")
        if item.depublication_date and not item.publication_date
            d = $D(item.depublication_date.slice(0,19))
            effective = d.strftime("- %d.%m.%Y")
        if item.depublication_date and item.publication_date
            d1 = $D(item.publication_date.slice(0,19))
            d2 = $D(item.depublication_date.slice(0,19))
            effective = d1.strftime("%d.%m.%Y")+" - "+d2.strftime("%d.%m.%Y")
        if effective
            item.meta.effective = "Published: "+effective
        item

    reset: () ->

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
        if publication_date!="" and depublication_date!=""
            if depublication_date<publication_date
                throw "Publication Date must be earlier than depublication
            date"
        data = {
            publication_date : publication_date.toString()
            depublication_date : depublication_date.toString()
        }
        data

    to_form: (params) ->
        if params.content==""
            throw "Please enter a status message"
        data = {
                content: params.content
            }
        for a,v of @convert_dates(params)
            data[a]=v
        data

class Link extends Status

    reset: () ->
        super
        $("#link-box").slideUp()
        $("#link-box-title").text("")
        $("#link-box-description").text("")
        $("#link-box-url").text("")
        $("#link-submit").text("Load")

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
        }
        if params.link==""
            throw "Well, you have to enter a link actually"
        if @data
            data.link_title = @data.title
            data.link_description = @data.content
            data.link_image = @active_image
        else
            data.link_title = params.link
        data

    process: () ->
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
                if data.error
                    $("#link-submit").text("Cannot load!")
                    setTimeout( () ->
                        $("#link-submit").text("Load")
                    , 2000)
                    return
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
        if @img_amount == 0
            $("#imageselector").hide()
            $("#link-box-image-container").hide()
            return
        $("#imageselector").show()
        $("#link-box-image-container").show()
        @img_idx = idx
        imgurl = @data.all_image_urls[idx]
        img = @data.images[imgurl]
        @active_image = img.thumb.url
        $("#link-box-image").attr("src",img.thumb.url)

class Poll extends Status

    to_form: (params) ->
        if params.content == ""
                throw "Please enter a poll title"
        if params.poll_answers == ""
                throw "Please enter some answers"
        answers = []
        for line in params.poll_answers.split("\n")
            if line != ""
                answers.push(line)
        data = {
            content: params.content
            answers: answers
        }
        for a,v of @convert_dates(params)
            data[a]=v
        data

TYPEDEFS = {
    status: Status
    link: Link
    poll: Poll
    folder: Status
}

TYPES = {}

PAGE = {
    id: null,
    render: (context, content_id) ->
        base_url = CONTENT_API+content_id
        $.getJSON(base_url+';parents?oauth_token='+VAR.token, (parents) ->
            $.getJSON(base_url+';default?oauth_token='+VAR.token, (details) ->
                data = {}
                if (parents.length>0)
                    data.title = details.content
                # remove root node
                data.parents = parents.slice(1, parents.length)
                data.virtual_path = virtual_path
                context.partial(TEMPLATES+'timeline.mustache', data)
                .then(() ->
                    # initialize tabs and types
                    TABS.init(details._subtypes)
                    for a,v of TYPEDEFS
                        TYPES[a] = new v

                    # setup the date fields
                    $(".dateinput" ).datepicker({dateFormat: 'dd.mm.yy'});
                    $("#depubdate-remove" ).click(() ->
                        $("#depublication-date").val("")
                        false
                    )
                    $("#pubdate-remove" ).click(() ->
                        $("#publication-date").val("")
                        false
                    )

                    # fill the status list
                    statuslist = $("#statuslist").detach()
                    statuslist.hide()
                    @load(base_url+";children?oauth_token="+VAR.token, {cache:false})
                    .then( (context) ->
                        items = @content
                        users = _.uniq(_.pluck(items, 'user'))
                        that = this
                        setTimeout( () ->
                            statuslist.fadeIn()
                        , 300)
                        $.ajax({
                            url: virtual_path+'/api/1/users/names'
                            data: JSON.stringify(users)
                            type: 'POST'
                            processData: false
                            contentType: "application/json"
                            success: (data) ->
                                res = []
                                _.each(items, (item) ->
                                    repr = TYPES[item._type].prepare(item)
                                    repr.meta.username = data[item.user]
                                    that.render(TEMPLATES+'meta.mustache', repr.meta)
                                    .then( (context2) ->
                                        repr.meta = context2
                                    )
                                    .render(TEMPLATES+'entry.'+item._type+'.mustache', repr )
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
        try
            data = active_type.to_form(@params)
        catch error
            ERROR.error(error)
            false
        data._type = active
        data.user = VAR.poco.id
        data.oauth_token = VAR.token
        base_url = CONTENT_API+PAGE.id
        data = JSON.stringify(data)
        ERROR.off()
        that = this
        $.ajax({
            url : base_url
            type : 'POST'
            data : data
            dataType : 'json'
            processData : false
            contentType: 'application/json'
            success : (data, textResponse) ->
                if not data.error
                    data.id = data._id
                    data.username = VAR.poco.name.formatted
                    data.profile = VAR.poco.thumbnailUrl
                    repr = TYPES[active].prepare(data)
                    repr.meta.username = data['username']
                    that.render(TEMPLATES+'meta.mustache', repr.meta)
                    .then( (context2) ->
                        repr.meta = context2
                    )
                    .render(TEMPLATES+'entry.'+active+'.mustache', repr)
                    .then( (content) ->
                        a = $("<div/>").html(content)
                        a.hide()
                        a.prependTo("#statuslist")
                        a.slideDown()
                        TYPES[active].reset()
                    )
                    $(':input','#entrybox')
                     .not(':button, :submit, :reset, :hidden')
                     .val('')
                     .removeAttr('checked')
                     .removeAttr('selected')
                else
                    ERROR.error(data.error_msg)
        })
        false
      )
)

VAR = {}

$(document).ready(
  ->
    $.getJSON(virtual_path+'/pm/var', (data) ->
        CONTENT_API = virtual_path+"/api/1/content/"
        TEMPLATES = virtual_path+"/pm/templates/"
        VAR = data
        app.run("#/")
    )
)
