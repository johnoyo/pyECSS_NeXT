class WebGPURenderer:
    def __init__(self) -> None:
        self.name = 'WebGPURenderer'

    def draw(self):
        print(f'WebGPURenderer draw {self.name}')

    def draw_indexed(self):
        print(f'WebGPURenderer draw_indexed {self.name}')