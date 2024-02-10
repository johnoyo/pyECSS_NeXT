from ECS.Utilities.ShaderLib import ShaderLib
from ECS.Utilities.TextureLib import TextureLib

class MaterialInstance:
    def __init__(self, shader_program, textures, shader_params = []):
        self.shader_program = shader_program
        self.textures = textures
        self.shader_params = shader_params

class MaterialData:
    def __init__(self, base_template, textures):
        self.base_template = base_template
        self.textures = textures

    def __eq__(self, other):
        if self.base_template != other.base_template:
            return False
        if len(self.textures) != len(other.textures):
            return False
        for i in range(len(self.textures)):
            if (self.textures[i] != other.textures[i]):
                return False
        return True
    
    def __hash__(self):
        return hash((self.base_template, len(self.textures), tuple(texture for texture in self.textures)))

class MaterialLib(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MaterialLib, cls).__new__(cls)
            cls.instance.cached_materials: dict[MaterialData, MaterialInstance] = {}
            cls.instance.materials: dict[str, MaterialInstance] = {}
        return cls.instance
    
    def build(cls, name: str, data: MaterialData):
        print('build')
        if cls.instance.cached_materials.get(data) != None:
            print('cached')
            material = cls.instance.cached_materials[data]
            cls.instance.materials[name] = material
            return material

        print('created')
        shader_program = ShaderLib().get(data.base_template)

        textures = []
        for texture_name in data.textures: 
            textures.append(texture_name)

        cls.instance.cached_materials[data] = MaterialInstance(shader_program, textures)
        cls.instance.materials[name] = MaterialInstance(shader_program, textures)

        return cls.instance.materials[name]

    def get(cls, name):
        return cls.instance.materials.get(name)