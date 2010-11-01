CONTENT_API = "/api/1/content/"

class Processor
    templates: ['link','status']
    tmpls: {
        link: '''
                <div class="activity" id="a-{{id}}">
                    <div class="body">
                        {{content}}
                        <div class="link-info">
                            <img class="link-box-image" src="{{link_image}}" />
                            <strong class="link-box-title"><a href="{{link_url}}">{{link_title}}</a></strong>
                            <div class="link-box-description">{{link_description}}</div>
                        </div>
                    </div>
                </div>
         '''
        status: '''
                <div class="activity" id="a-{{ id }}">
                    <div class="body">
                        {{ content }}
                    </div>
                </div>
        '''
    }
    constructor: (@baseurl) ->
    display_items: ->
        document.write("<div id='jsview'></div>")
        $.ajax({
            url: "http://localhost:9991/api/1/content/0?r=jsview&jsview_type=link&so=date&sd=down"
            dataType: "jsonp"
            success: (data) =>
                    for key, item of data.jsview
                        t = @tmpls[item._type]
                        $(Mustache.to_html(t, item)).appendTo("#jsview")
        })


$(document).ready(
  ->
      p = new Processor "http://localhost:9991"
      p.display_items()
)
