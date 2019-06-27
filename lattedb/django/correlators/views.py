from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components


def index(request):
    x = [1, 3, 5, 7, 9, 11, 13]
    y = [1, 2, 3, 4, 5, 6, 7]
    title = "y = f(x)"

    plot = figure(
        title=title,
        x_axis_label="X-Axis",
        y_axis_label="Y-Axis",
        plot_width=400,
        plot_height=400,
    )

    plot.line(x, y, legend="f(x)", line_width=2)
    plot.sizing_mode = "scale_width"

    script, div = components(plot)
    correlator = None

    context = {"script": script, "div": div, "correlator": correlator}

    # Feed them to the Django template.
    return render(request, "correlator.html", context)
