from django.db import connection

# Create your tests here.


class BaseTest:
    """Abstract implementation of a table class test
    """

    cls = None
    parameters = {}
    tree = None

    @classmethod
    def check(cls, instance, parameters):
        for key in cls.parameters:
            if key in cls.cls.__dict__:
                value = getattr(instance.specialization, key)
                field = [
                    field for field in cls.cls._meta.get_fields() if field.name == key
                ][0]
                if value != field.get_db_prep_value(parameters[key], connection):
                    raise ValueError(
                        "%s parameters for %s not agree with input:\n%s != %s"
                        % (instance, key, value, parameters[key])
                    )

    def test_get_or_create_from_parameters(self):
        """Tests get or create from parameters method

        Creates an instance and checks attributes.
        """

        self.cls.get_or_create_from_parameters(self.parameters, tree=self.tree)

        # Get created object
        instance = self.cls.objects.last()
        # check if parameters correct
        self.check(instance, self.parameters)
