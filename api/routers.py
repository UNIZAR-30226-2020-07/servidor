from rest_framework import routers


class DefaultRouter(routers.DefaultRouter):
    """
    Extends `DefaultRouter` class to add a method for extending url routes from another router.
    And also allows to insert custom urls in the api root view
    Adapted from https://stackoverflow.com/a/40904241
    """

    customUrls = []

    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)

    def addCustomUrl(self, label, urlName):
        """
        Add a custom url to show in the root view
        Args:
            label: string name in the list
            urlName: name of the url to show
        """
        self.customUrls.append((label, urlName))

    def get_api_root_view(self, api_urls=None):
        """
        Inyect custom urls via black magic
        """
        view = super().get_api_root_view(api_urls=api_urls)

        for label, urlName in self.customUrls:
            view.view_initkwargs['api_root_dict'][label] = urlName

        return view
