from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Whisker


def index(request):
    x = [1, 3, 5, 7, 9, 11, 13]
    y = [1, 2, 3, 4, 5, 6, 7]

    plot = figure(
        x_axis_label="X-Axis", y_axis_label="Y-Axis", plot_width=600, plot_height=400
    )
    plot.sizing_mode = "scale_width"

    plot.circle(x, y, legend="Data", size=5)

    lower, upper = [], []
    for yi in y:
        lower.append(yi - 0.1)
        upper.append(yi + 0.1)

    source_error = ColumnDataSource(data=dict(base=x, lower=lower, upper=upper))

    plot.add_layout(
        Whisker(source=source_error, base="base", upper="upper", lower="lower")
    )

    script, div = components(plot)
    correlator = None

    context = {"script": script, "div": div, "correlator": correlator}

    # Feed them to the Django template.
    return render(request, "correlator.html", context)
