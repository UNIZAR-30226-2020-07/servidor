from django.forms import Select
from django.template import Template, Context
from rest_framework.filters import SearchFilter


class SongSearch(SearchFilter):
    """
    A custom search filter for the songs model to search (the 'search' value) for these fields:
    paramater name: search_for
    parameter value: one of 'genre', 'album', 'artist' or none (uses title)
    Example: "/songs/?search=happy&search_for=artist" will return songs whose artists matches 'happy'
    """
    search_for_param = 'search_for'
    search_for_choices = (  # (query, name, field)
        ('title', 'Title', 'title'),  # default
        ('genre', 'Genre', 'genre'),
        ('album', 'Album', 'album__name'),
        ('artist', 'Artist', 'album__artist__name'),
    )

    def get_search_fields(self, view, request):
        return [{q: f for q, _, f in self.search_for_choices}.get(  # cases
            request.query_params.get(self.search_for_param),  # switch
            self.search_for_choices[0][2]  # default
        )]

    def to_html(self, request, queryset, view):
        """
        For documentation purposes, ugly and probably can be better
        """
        term = self.get_search_terms(request)
        term = term[0] if term else ''
        context = {
            'param': self.search_param,
            'term': term,
            'select': Select(choices=[(q, n) for q, n, _ in self.search_for_choices])
                .render(self.search_for_param, request.query_params.get(self.search_for_param, '')),
        }
        template = Template("""{% load i18n %}
<h2>{% trans "Search" %}</h2>
<form class="form-inline">
  <div class="form-group">
    <div class="input-group">
      <input type="text" class="form-control" style="width: 350px" name="{{ param }}" value="{{ term }}">
      {{ select }}
      <span class="input-group-btn">
        <button class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search" aria-hidden="true"></span> Search</button>
      </span>
    </div>
  </div>
</form>""")
        return template.render(Context(context))
