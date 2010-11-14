
class Poll
    content_api: "/api/1/content/"
    template_api: "/api/templates/"

    constructor: (@baseurl, @elem) ->

        $.ajax({
            url: @baseurl+@content_api+"0?r=jsview&jsview_type=poll&so=date&sd=down&l=1"
            dataType: "jsonp"
            success: (data) =>
                @item = data.jsview[0]
                @item_id = @item._id
                $.ajax({
                    url : @baseurl+@content_api+@item._id+";voted"
                    dataType: "jsonp"
                    success: (data) =>
                        @voted = data.voted
                        @load_template()
                })
            })

    load_template: () =>
        if (@voted)
            url = @baseurl+@template_api+'entry.poll.results.mustache'
        else
            url = @baseurl+@template_api+'entry.poll.mustache'
        $.ajax {
            url: url
            dataType: 'jsonp'
            success: (data) =>
                @template = data
                if (@voted)
                    @display_results()
                else
                    @display_poll()
        }

    display_poll: () ->
        # convert answers
        new_answers = []
        i=0
        for answer in @item.answers
            new_answers.push({
                title: answer
                no: i
            })
            i=i+1
        @item.answers = new_answers
        h = $(Mustache.to_html(@template, @item))
        $(@elem).html(h)
        $("#ql-poll-form-"+@item._id).change(@vote)

    display_results: ->
        $.ajax({
            url : @baseurl+@content_api+@item._id+";results"
            dataType: "jsonp"
            success: (data) =>
                h = $(Mustache.to_html(@template, data))
                $(@elem).html(h)
        })

    vote: (ev) =>
        elem = ev.target
        qid = $(elem).attr('data-qid')
        aid = $(elem).attr('data-aid')
        url = @baseurl+@content_api+qid+";vote"
        data = {answer_no: aid}
        $.ajax({
            url: url
            dataType: 'jsonp'
            type: "GET"
            data: data 
            success: (data) =>
                @voted = true
                @load_template()
        })

class PollProcessor

    constructor: () ->
        @template = ""
        @voted = false
        @polls = []

        # retrieve the polls
        poll_elements = $(".ql-poll")
        for elem in poll_elements
            baseurl = $(elem).attr("data-baseurl")
            poll = new Poll baseurl, elem
            polls.push(poll)


$(document).ready(
  ->
      p = new PollProcessor
)
