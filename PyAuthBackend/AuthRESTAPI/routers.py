from rest_framework.routers import Route, DynamicRoute, DefaultRouter

class WriteOnlyRouter(DefaultRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={
                'get'  : 'list',
                'post' : 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': ''}
        )
    ] 
