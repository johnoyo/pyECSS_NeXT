from ECS.Registry import Registry

class System:
    def __init__(self, filters: list[type]):
        self.filters = filters
        self.filtered_components = []
        self.filtered_entities = []

        components_array = Registry().get_components_array()

        for entity in Registry().get_entities():
            entity_components = Registry().get_entity_component_references(entity)
            self.filter_entity_components(entity, entity_components, components_array)

    def filter_entity_components(self, entity, entity_components, components_array):
        if (entity in self.filtered_entities):
            return
        
        i, j = 0, 0
        for filter in self.filters:
            j += 1
            if filter in entity_components.keys():
                i += 1            
        if (j == i):
            self.filtered_components.append(tuple(components_array[filter][entity_components[filter]] for filter in self.filters))
            self.filtered_entities.append(entity)

    def on_create_base(self):
        # Check if the subclass has overridden the method
        if hasattr(self, 'on_create') and callable(getattr(self, 'on_create')):
            for entity, components in zip(self.filtered_entities, self.filtered_components):
                if (len(components) == 1):
                    self.on_create(entity, components[0])
                else:
                    self.on_create(entity, components)
        else:
            print("on_update method not implemented")

    def on_update_base(self):
        # Check if the subclass has overridden the method
        if hasattr(self, 'on_update') and callable(getattr(self, 'on_update')):
            for entity, components in zip(self.filtered_entities, self.filtered_components):
                if (len(components) == 1):
                    self.on_update(entity, components[0])
                else:
                    self.on_update(entity, components)
        else:
            print("on_update method not implemented")