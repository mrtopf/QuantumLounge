
class Poll
    content_api: "/api/1/content/"
    template_api: "/api/templates/"

    constructor: (@apiurl, @tapiurl, @elem, @node_id) ->

        $.ajax({
            url: @apiurl+@node_id+"?r=jsview&jsview_type=poll&so=date&sd=down&l=1"
            dataType: "jsonp"
            success: (data) =>
                @item = data.jsview[0]
                @item_id = @item._id
                $.ajax({
                    url : @apiurl+@item._id+";voted"
                    dataType: "jsonp"
                    success: (data) =>
                        @voted = data.voted
                        @load_template()
                })
            })

    load_template: () =>
        if (@voted)
            url = @tapiurl+'entry.poll.results.mustache'
        else
            url = @tapiurl+'entry.poll.mustache'
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
                'title': ""+answer
                'no': i
            })
            i=i+1
        @item.answers = new_answers
        h = $(Mustache.to_html(@template, @item))
        $(@elem).html(h)
        $("#ql-poll-form-"+@item._id).change(@vote)

    display_results: ->
        $.ajax({
            url : @apiurl+@item._id+";results"
            dataType: "jsonp"
            success: (data) =>
                h = $(Mustache.to_html(@template, data))
                $(@elem).html(h)
        })

    vote: (ev) =>
        elem = ev.target
        qid = $(elem).attr('data-qid')
        aid = $(elem).attr('data-aid')
        url = @apiurl+qid+";vote"
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
            apiurl = $(elem).attr("data-api")
            tapiurl = $(elem).attr("data-tapi")
            node_id = $(elem).attr("data-node")
            poll = new Poll apiurl, tapiurl, elem, node_id
            @polls.push(poll)


$(document).ready(
  ->
      p = new PollProcessor
)
