class DependencyContainer:
    _dependencies = {}

    @classmethod
    def register(cls, class_obj):
        cls._dependencies[class_obj] = class_obj()

    @classmethod
    def get_instance(cls, class_obj):
        if class_obj in cls._dependencies:
            return cls._dependencies[class_obj]
        else:
            raise ValueError(f"{class_obj} isn't registered as a dependency")
