
class Item

    constructor: (@baseurl, @node_id, @apiurl, @templateurl, @type, @amount, @elem) ->
        $.ajax({
            url:
                @apiurl+@node_id+";query?type="+@type+"&so=date&sd=down&l="+@amount+"&fmt=html"
            dataType: "jsonp"
            success: (data) =>
                console.log(@node_id)
                console.log(data.html)
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
            node_id = $(elem).attr("data-node")
            if not node_id
                node_id = "0"
            templateurl = $(elem).attr("data-template")
            type = $(elem).attr("data-type")
            amount = $(elem).attr("data-amount")
            item = new Item(baseurl, node_id, apiurl, templateurl, type, amount, elem)
            @items.push(item)


$(document).ready(
  ->
      p = new Processor
)
