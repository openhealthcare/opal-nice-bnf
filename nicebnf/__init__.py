"""
Plugin definition for the nicebnf OPAL plugin
"""
from opal.core import plugins

from nicebnf.urls import urlpatterns

class nicebnfPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    urls = urlpatterns
    javascripts = {
        # Add your javascripts here!
        'opal.nicebnf': [
            # 'js/nicebnf/app.js',
            # 'js/nicebnf/controllers/larry.js',
            # 'js/nicebnf/services/larry.js',
        ]
    }

    def restricted_teams(self, user):
        """
        Return any restricted teams for particualr users that our
        plugin may define.
        """
        return []

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {}

    def flows(self):
        """
        Return any custom flows that our plugin may define
        """
        return {}

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}


plugins.register(nicebnfPlugin)