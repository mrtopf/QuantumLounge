
class Item

    constructor: (@baseurl, @apiurl, @templateurl, @type, @amount, @elem) ->
        $.ajax({
            url:
                @apiurl+"0;query?type="+@type+"&so=date&sd=down&l="+@amount+"&fmt=html"
            dataType: "jsonp"
            success: (data) =>
                e = $("<div />").html(data.html)
                e.hide()
                $(@elem).html(e)
                e.fadeIn()
            })

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
