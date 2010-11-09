

class PollProcessor
    content_api: "/api/1/content/"
    template_api: "/api/templates/"

    constructor: (@baseurl) ->
        @template = ""
        # load template
        url = @baseurl+@template_api+'entry.poll.mustache'
        $.ajax {
            url: url
            dataType: 'jsonp'
            success: (data) =>
                @template = data
        }
    display_items: ->
        $.ajax({
            url: "http://localhost:9991/api/1/content/0?r=jsview&jsview_type=poll&so=date&sd=down&l=1"
            dataType: "jsonp"
            success: (data) =>
                console.log data
                for key, item of data.jsview
                    $(Mustache.to_html(@template, item)).appendTo("#poll")
        })


$(document).ready(
  ->
      p = new PollProcessor "http://localhost:9991"
      p.display_items()
)
