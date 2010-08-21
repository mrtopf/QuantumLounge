========================
The JavaScript framework
========================

loading templates
=================

Client-side templates can be loaded and cached dynamically. For this you can use the
``TemplateLoader`` component which allows you to load and render templates based on the 
`json-template templating engine <http://code.google.com/p/json-template>`_.

Templates are loaded dynamically and cached locally in the page then.

Setup
-----

In order to use this component you need to include ``static/js/tmpl.js`` in your JavaScript code. You can use the resource like this::

    JS = [
        ...
        js_from_pkg_stream(__name__, 'static/js/tmpl.js', name="", merge=True, prio=4,),
        ...
    ]
    
(check out ``http/setup.py`` and ``main.py`` for an example.


Usage
-----

To load and render a template called ``status`` you can use the following JS code::

    var tm = TemplateManager();
    tm.render('status', function (d) {
        $("#statuses").append(d);
    }, {content: "my status"})
    
This initializes the template manager and then calls the ``render`` function with 
three parameters:

* the name of the template to load (here ``status``)
* the callback to call once the template is loaded and rendered
* the JSON payload to be passed to the template

loading the template
********************

The template per default will be loaded from ``jst/status``, so a ``/jst`` is prepended.
Make sure you have a static url handler attached to that path pointing to a directory
containing the templates.

the callback
************

The callback function is called with the expanded template as the only argument. It is called after loading and rendering of the template and can e.g. append the result to an existing div. 

The payload
***********

The payload argument is the JSON data to be passed into the template. The template will automatically rendered using it.



