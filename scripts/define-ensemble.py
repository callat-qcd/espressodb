"""Creates ensemble for all gaugeconfigs
"""

from lattedb.gaugeconfig.models import Nf211
from lattedb.ensemble.models import Ensemble


def main():
    """Creates ensemble for all gaugeconfigs
    """

    keys = ("nx", "nt", "gaugeaction", "light", "strange", "charm")
    for distinct in Nf211.objects.values_list(*keys).distinct():
        query = {key: val for key, val in zip(keys, distinct)}
        nfs = Nf211.objects.filter(**query)  # .filter(config__lte = 500)
        config = nfs.first()
        label = f"{config.short_tag}_{config.stream}_{nfs.count()}"
        ensemble, _ = Ensemble.objects.get_or_create(label=label)
        ensemble.configurations.add(*nfs)
        ensemble.save()


if __name__ == "__main__":
    main()
