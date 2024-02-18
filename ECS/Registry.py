from ECS.Entity import Entity
from ECS.Application import Application

class Registry(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Registry, cls).__new__(cls)
            cls.instance.entity_components = {}
            cls.instance.component_arrays = {}
            cls.instance.entities = []
            cls.instance.systems = []
        return cls.instance
    
    def enroll_entity(cls):
        entity = Entity()
        cls.instance.entities.append(entity)
        return entity

    def get_entities(cls):
        return cls.instance.entities
    
    def add_component(cls, entity: Entity, component):
        # Create new component reference array for entity if it does not exist
        if entity.id not in cls.instance.entity_components:
            cls.instance.entity_components[entity.id] = {}

        # Retrieve type from component
        component_type = type(component)

        # Create new component array if it does not exist yet
        if component_type not in cls.instance.component_arrays:
            cls.instance.component_arrays[component_type] = []

        # Find the entities component reference
        component_array = cls.instance.component_arrays[component_type]
        component_index = len(component_array)

        # Update entity's component reference  
        cls.instance.entity_components[entity.id][component_type] = component_index

        # Add the new component to the appropriate component array
        component_array.append(component)

        # Update existing systems that operate on this component. (Usefull in runtime addition of components)
        for system in cls.instance.systems:
            entity_components = Registry().get_entity_component_references(entity)
            system.filter_entity_components(entity, entity_components, cls.instance.component_arrays)

        return component

    def has_component(cls, entity: Entity, component_type: type):
        return component_type in cls.instance.entity_components.get(entity.id)
    
    def get_component(cls, entity: Entity, component_type: type):
        if component_type in cls.instance.entity_components[entity.id]:
            component_index = cls.instance.entity_components[entity.id][component_type]
            return cls.instance.component_arrays[component_type][component_index]
        else:
            return None
    
    def get_entity_component_references(cls, entity: Entity):
        return cls.instance.entity_components.get(entity.id, {})
    
    def get_components_array(cls):
        return cls.instance.component_arrays
    
    def register_system(cls, system):
        cls.instance.systems.append(system)

        if (Application().is_running()):
            system.on_create_base()

    def get_systems(cls):
        return cls.instance.systems
    
    def start(cls):
        Application().set_is_running(True)
        
        for system in Registry().get_systems():
            system.on_create_base()

    def update(cls, ts):
        for system in Registry().get_systems():
            system.on_update_base(ts)