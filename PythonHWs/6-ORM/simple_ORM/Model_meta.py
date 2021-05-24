from .fields import Field


class ModelMeta(type):
    """
    Meta class for orm model
    """

    def __new__(mcs, future_class_name,
                future_class_parents, future_class_attr):
        meta = future_class_attr.pop('Meta', None)
        if meta:
            for k, v in meta.__dict__.items():
                if not k.startswith('_'):
                    future_class_attr[k] = v

        future_class_attr['_name'] = future_class_name
        future_class_attr['_data'] = {}
        for name, value in future_class_attr.items():
            if isinstance(value, Field):
                value._name = name
                future_class_attr['_data'][name] = {
                    '_meta': value
                }

        return super(ModelMeta, mcs).__new__(mcs,
                                             future_class_name,
                                             future_class_parents,
                                             future_class_attr)