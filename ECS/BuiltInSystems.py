from ECS.System import System
from ECS.Entity import Entity
from ECS.Registry import Registry
from ECS.Renderer import Renderer
from ECS.Utilities.MaterialLib import MaterialLib

from ECS.BuiltInComponents import TransformComponent, LinkComponent

from ECS.Math import *

import OpenGL.GL as gl

class TransformSystem(System):
    """
    The system responsible for transformations.
    """

    def on_create(self, entity: Entity, components):
        """
        Gets called once in the first frame for every entity that the system operates on.
        """
        transform = components

        T = translate(transform.translation[0], transform.translation[1], transform.translation[2])
        R = rotate((1, 0, 0), transform.rotation[0]) @ rotate((0, 1, 0), transform.rotation[1]) @ rotate((0, 0, 1), transform.rotation[2])
        S = scale(transform.scale[0], transform.scale[1], transform.scale[2])
        
        transform.local_matrix = S @ R @ T

    def on_update(self, entity: Entity, components):
        """
        Gets called every frame for every entity that the system operates on.
        """
        transform = components

        previous_local_matrix = transform.local_matrix
        
        T = translate(transform.translation[0], transform.translation[1], transform.translation[2])
        R = rotate((1, 0, 0), transform.rotation[0]) @ rotate((0, 1, 0), transform.rotation[1]) @ rotate((0, 0, 1), transform.rotation[2])
        S = scale(transform.scale[0], transform.scale[1], transform.scale[2])
        
        transform.local_matrix = S @ R @ T
        transform.world_matrix = transform.local_matrix

        if (np.array_equal(previous_local_matrix, transform.local_matrix)):
            transform.is_dirty = False
        else:
            transform.is_dirty = True

class LinkSystem(System):
    """
    The system responsible for the scene hierachy.
    """

    def on_create(self, entity: Entity, components):
        """
        Gets called once in the first frame for every entity that the system operates on.
        """
        link, transform = components
        transform.world_matrix = self.get_world_space_transform(entity, link)

    def on_update(self, entity: Entity, components):
        """
        Gets called every frame for every entity that the system operates on.
        """
        link, transform = components
        transform.world_matrix = self.get_world_space_transform(entity, link)

    def get_world_space_transform(self, entity, link):
        transform = np.identity(4)

        if (link != None):
            if (link.parent != None):
                parent_link = Registry().get_component(link.parent, LinkComponent)
                transform = self.get_world_space_transform(link.parent, parent_link)

        return transform @ Registry().get_component(entity, TransformComponent).local_matrix

class RenderingSystem(System):
    """
    The system responsible for rendering.
    """

    def on_create(self, entity: Entity, components):
        """
        Gets called once in the first frame for every entity that the system operates on.
        """
        render_data, material, transform = components

        material.instance = MaterialLib().get(material.name)

        render_data.batch = Renderer().add_batch(render_data, material)

        # Set up matrices for projection and view
        projection = perspective(45.0, 1920 / 1080, 0.1, 100.0)
        view = translate(0.0, 0.0, -5.0)
        model = identity()

        gl.glUniformMatrix4fv(gl.glGetUniformLocation(material.instance.shader_program, "projection"), 1, gl.GL_FALSE, projection)
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(material.instance.shader_program, "view"), 1, gl.GL_FALSE, view)
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(material.instance.shader_program, "model"), 1, gl.GL_FALSE, model)

    def on_update(self, entity: Entity, components):
        """
        Gets called every frame for every entity that the system operates on.
        """
        render_data, material, transform = components
        Renderer().draw(transform.world_matrix, render_data, material)
