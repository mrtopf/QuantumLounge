function TemplateManager() {
    
    var templates = {};

    /*
        load and render a named template.
        
        name -- the name of the template file to load (will be cached)
        callback -- a function called once the template is loaded and rendered. It receives
            the html data which the callback can further process.
        payload -- the JSON payload to be passed to the template.
    */
    function render(name, callback, payload) {
        if (name in templates) {
            callback(templates[name].expand(payload));
            return false;
        }
        $.ajax({
            url: "/jst/"+name,
            success: function (data, textResponse) {
                templates[name] = jsontemplate.Template(data);
                callback(templates[name].expand(payload));
            }
        })
        return false;
    }
    return {
        render: render
    }
}

