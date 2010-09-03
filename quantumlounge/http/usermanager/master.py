from quantumlounge.framework import Handler
from quantumlounge.framework.decorators import html

class Master(Handler):
    """handles the OAuth authorize endpoint. For this we need to do the following things:

    **Allowed Methods** : GET
    
    **URL parameters**
        
    **Remarks**
        
    """

    @html
    def get(self):
        """render the login form"""
        return self.app.settings.templates['templates/master.pt'].render(
            handler = self,
            js_jquery_link = self.settings['js_resources']("jquery"),            
            js_head_link = self.settings['js_resources']("head"),
            jslinks = self.settings['js_resources'](),
            csslinks = self.settings['css_resources'](),
        )
            