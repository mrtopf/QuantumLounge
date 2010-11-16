
class Item

    constructor: (@baseurl, @apiurl, @templateurl, @type, @amount, @elem) ->

        $.ajax({
            url: @apiurl+"0?r=jsview&jsview_type="+@type+"&so=date&sd=down&l="+@amount
            dataType: "jsonp"
            success: (data) =>
                @item = data.jsview[0]
                @load_template()
            })

    load_template: () =>
        $.ajax {
            url: @templateurl
            dataType: 'jsonp'
            success: (data) =>
                h = $(Mustache.to_html(data, @item))
                $(@elem).html(h)
        }

class Processor

    constructor: () ->
        @items = []

        # retrieve the polls
        item_elems = $(".ql-item")
        for elem in item_elems
            baseurl = $(elem).attr("data-baseurl")
            apiurl = $(elem).attr("data-api")
            templateurl = $(elem).attr("data-template")
            type = $(elem).attr("data-type")
            amount = $(elem).attr("data-amount")
            item = new Item(baseurl, apiurl, templateurl, type, amount, elem)
            @items.push(item)


$(document).ready(
  ->
      p = new Processor
)
