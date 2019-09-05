from django.db import models

from lattedb.project.models import Data

from lattedb.correlator.models import Baryon2pt


class SourceAvg2pt(Data):
    """ Base table for origin averaged data. This data is what is in hdf5.
    """

    baryon2pts = models.ManyToManyField(Baryon2pt)

    # @property
    # def long_tag(self) -> Optional[str]:
    #    """Returns descriptive long tag of first configuration
    #    """
    #    first = self.configurations.first()  # pylint: disable=E1101
    #    return first.specialization.long_tag if first else None

    # def check_consistency(self):
    # """Checks if all correlators in same set have the same meta info. except spin, parity
    # """
    # corrtype = np.unique([corr.type for corr in self.correlators.all()])
    # if len(corrtype) != 1:
    #    raise ValidationError(
    #        f"{corrtype} should only have one unique entry"
    #    )
    # if corrtype[0] != "Baryon2pt":
    #    raise ValidationError(
    #        f"SourceAvg2pt should only have Baryon2pt for this project."
    #    )

    # for corr in self.correlators.all():
    #    check_i = {"type": [], "gaugeconfig_ptr_id": [],
    #    for corr_i in corr:
    #        check_i["type"].extend(corr_i.type)
    #        check_i["gaugeconfig_ptr_id"].extend = corr_i.specialization.propagator0.specialization.gaugeconfig.specialization

    # first = self.correlators.first()  # pylint: disable=E1101
    # if first:
    #    for config in self.configurations.all()[1:]:  # pylint: disable=E1101
    #        if not first.same_ensemble(config):
    #            raise ValidationError(
    #                f"{config} if different from first config {first}"
    #            )
    class Meta:
        app_label="project_fhcompare"