from django.views.generic.base import TemplateView

from pandas import DataFrame

from bokeh.plotting import figure
from bokeh.plotting.figure import Figure
from bokeh.embed import components
from bokeh import __version__ as bokeh_version

from my_project.hamiltonian.models import Contact as ContactHamiltonian
from my_project.hamiltonian.models import Eigenvalue

# Create your views here.


class HamiltonianStatusView(TemplateView):
    """Presents heatmap of finished computations
    """

    model = ContactHamiltonian
    template_name = "status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        df = self.prepare_data()
        fig = self.prepare_figure(df)
        script, div = components(fig)

        context["script"] = script
        context["div"] = div
        context["model"] = self.model
        context["bokeh_version"] = bokeh_version

        return context

    def prepare_data(self) -> DataFrame:
        """Finds all eigenvalues corresponding to the Hamitonian model and counts them.

        Returns a data frame which lists which hamiltonian has which columns.
        """
        hamiltonians = self.model.objects.all()

        # Find all energy levels which correspond to the hamiltonians
        eigenvalues = Eigenvalue.objects.filter(hamiltonian__in=hamiltonians)

        # Group all eigenvalues by their hamitonian and count them
        level_count = (
            eigenvalues.to_dataframe(fieldnames=["hamiltonian__id", "n_level"])
            .rename(columns={"hamiltonian__id": "id"})
            .groupby(["id"])
            .count()
        )

        # Join the hamitonian table with the count table
        df = (
            hamiltonians.to_dataframe(fieldnames=["id", "spacing", "n_sites", "c"])
            .set_index("id")
            .join(level_count, on="id")
        )

        # And check if it has as many eigenvalues as sites
        df["done"] = df["n_sites"] == df["n_level"]

        # And add  colors to help plotting
        df["color"] = "green"
        df["color"] = df.color.where(df.done, "red")

        return df

    @staticmethod
    def prepare_figure(data: DataFrame) -> Figure:
        """Prepares a bokeh heatmap for the input data.

        Needs columns `spacing`, `n_sites`, `c`, `n_level` and `done`.
        """
        fig = figure(
            x_axis_location="above",
            tools="hover",
            tooltips=[
                ("Paramaters", "spacing = @spacing{(0.3f)}, # sites = @n_sites"),
                ("Count", "@n_level/@n_sites "),
                ("Interaction", "c = @c "),
            ],
            width=600,
            height=600,
        )

        fig.rect(
            "spacing",
            "n_sites",
            width=0.09,
            height=4.6,
            source=data,
            fill_color="color",
            legend="done",
        )

        fig.xaxis.axis_label = "spacing [fm]"
        fig.xaxis.axis_label_standoff = 10
        fig.yaxis.axis_label = "# sites"
        fig.yaxis.axis_label_standoff = 10

        fig.outline_line_color = None
        fig.grid.grid_line_color = None
        fig.axis.axis_line_color = None
        fig.axis.major_tick_line_color = None
        fig.axis.minor_tick_line_color = None

        fig.x_range.range_padding = 0.0
        fig.y_range.range_padding = 0.0

        return fig
