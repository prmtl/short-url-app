from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from server.api.internal.schema import schema
from server.api.views import GraphQLView

urlpatterns = [
    path(
        "",
        # NOTE(prmtl): disable CSRF to save API clients hustle of obtaining it
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
    )
]
