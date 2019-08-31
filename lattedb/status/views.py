from django.shortcuts import render

# Create your views here.

from django.views.generic.base import TemplateView


class ProgressView(TemplateView):

    template_name = "progress.html"

    def get_context_data(self, **kwargs):
        context = {}

        queued = 500
        running = 200
        collecting = 50
        done = 100

        total = queued + running + collecting + done

        context = {
            "summary": {
                "Baryon2pt": [
                    int(queued / total * 100),
                    int(running / total * 100),
                    int(collecting / total * 100),
                ],
                "OneToAll": [0, 0, 0],
            }
        }
        for key in context["summary"]:
            context["summary"][key].append(100 - sum(context["summary"][key]))

        return context
