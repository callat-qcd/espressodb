from lattedb.gaugeconfig.models import Nf211
from lattedb.ensemble.models import Ensemble

gauge_configs = Nf211.objects.all()

keys = ("nx", "nt", "gaugeaction", "light", "strange", "charm")
for distinct in Nf211.objects.values_list(*keys).distinct():
    query = {key: val for key, val in zip(keys, distinct)}
    nfs = Nf211.objects.filter(**query).filter(config__lte = 500)
    config = nfs.first()
    label = f"{config.short_tag}_{config.stream}_{nfs.count()}"
    ensemble, created = Ensemble.objects.get_or_create(label=label)   
    ensemble.configurations.add(*nfs)
    ensemble.save()

