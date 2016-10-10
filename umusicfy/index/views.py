
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/user-profile/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
