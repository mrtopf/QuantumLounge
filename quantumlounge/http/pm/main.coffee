
app = $.sammy(
    ->
      @element_selector = '#content'
      @use(Sammy.Template)
      
      @get('#/', (context) ->
          context.partial('/pm/templates/timeline.tmpl')
      )
)

$(document).ready(
  ->
    app.run("#/")
)
  
