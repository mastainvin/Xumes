from xumes.core.registry import create_registry, create_registry_content


config = create_registry()
given = create_registry_content()
when = create_registry_content()
then = create_registry_content()

config_registry = config.all
given_registry = given.all
when_registry = when.all
then_registry = then.all
