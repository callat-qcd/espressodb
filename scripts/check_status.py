"""Script which checks status of existing baryon 2pt correlators
"""
import os
import logging

from h5py import File

from lattedb.correlator.models import Baryon2pt
from lattedb.ensemble.models import Ensemble
from lattedb.status.models.correlator import Baryon2pt as Baryon2ptStatus

LOGGER = logging.getLogger("base")

HOME = "summit"
ROOT_PATH = {
    "a09m310_e": "/ccs/proj/lgt100/c51/x_files/project_2/production/a09m310_e/data"
}


def check_status(baryon2pt: Baryon2pt, root_path: str):
    """Checks status of baryon2pt correlator.

    The logic works as follows:

    **Arguments**
        baryon2pt: Baryon2pt
            The meta information database object of the correlator

        root_path: str
            The root path on the host where to expect the correlator.
    """
    LOGGER.debug("Checking status of %s", baryon2pt)

    # status, created = Baryon2ptStatus.objects.get_or_create(
    #     baryon2pt=baryon2pt, home=HOME
    # )
    status, created = Baryon2ptStatus(barryon2pt=baryon2pt, home=HOME), False
    LOGGER.debug(
        "Status entry found. Checking correctness."
        if created
        else "No status entry found. Creating new status."
    )

    directory = status.directory or os.path.join(
        root_path, f"{baryon2pt.short_tag}_{baryon2pt.n_config}.h5"
    )
    hdf5path = status.hdf5path or get_hdf5path(baryon2pt)
    LOGGER.debug("Looking up file %s and dset path %s", directory, hdf5path)

    if os.path.exists(directory) and data_exist(directory, hdf5path):
        LOGGER.debug("Data was found. Updating status")
        status.status = 2  # data exists
        status.directory = directory
        status.hdf5path = hdf5path
    else:
        LOGGER.debug("Data was not found. Updating status")
        status.status = 0  # data unknown
        status.directory = None
        status.hdf5path = None

    # status.save()


def get_hdf5path(baryon2pt: Baryon2pt) -> str:
    """Parses the hdf5 path for a baryon2pt correlator
    """
    prop = baryon2pt.propagator0
    config = prop.gaugeconfig
    src = baryon2pt.source
    return os.path.join(
        (
            f"gf{config.gaugesmear.flowtime:1.1f}"
            "_"
            f"w{src.interpolatorsmear.radius:1.1f}"
            "_"
            f"n{src.interpolatorsmear.step}"
            "_"
            f"M5{prop.fermionaction.m5:1.1f}"
            "_"
            f"L5{int(prop.fermionaction.l5)}"
            "_"
            f"a{prop.fermionaction.specialization.alpha5:1.1f}"
        ).replace(".", "p"),
        "spectrum",
        f"ml{config.light.quark_mass}".replace(".", "p"),
        f"{baryon2pt.tag}" + ("" if src.parity else "_np"),
        "spin_" + ("up" if src.spin_x2 else "dn"),
        f"x{prop.origin_x}y{prop.origin_y}z{prop.origin_z}t{prop.origin_t}",
    )


def data_exist(file_path: str, hdf5path: str) -> bool:
    """Checks if `hdf5path` is contained in `file_path`.

    **Arguments**
        file_path: str
            Path to HDF5 file

        hdf5path: str
            Path to data set in HDF5 file.
    """
    with File(file_path, "r") as h5f:
        return hdf5path in h5f


def main():
    """Looks up Baryon2pt correlators from the meta information and checks their status.
    """
    LOGGER.info("Start scaning for existing baryon 2pt correlators by ensemble")

    for ensemble in Ensemble.objects.all():

        LOGGER.info("Ensemble -> %s", ensemble)
        descriptor = f"{ensemble.short_tag}_{ensemble.stream}"
        root_path = ROOT_PATH.get(descriptor, None)

        if root_path is not None:

            correlators = Baryon2pt.get_from_ensemble(ensemble)
            LOGGER.info("Found meta information for %d correlators", correlators.count())

            for correlator in correlators:
                check_status(correlator, root_path)

        else:
            LOGGER.info("No path specified for ensemble %s.", descriptor)


if __name__ == "__main__":
    main()
