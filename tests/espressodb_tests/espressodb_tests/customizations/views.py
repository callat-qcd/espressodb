"""Views for the customizations app
"""
from espressodb.base.views import IndexView as BaseIndexView


class IndexView(BaseIndexView):
    """Index view of base app with different template which overrides default links
    """

    template_name = "customized-index.html"
