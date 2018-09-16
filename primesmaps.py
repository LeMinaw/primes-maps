from svgwrite         import Drawing
from svgwrite.path    import Path
from svgwrite.shapes  import Circle, Line
from svgwrite.masking import Mask
from math import sqrt


def distance(a, b):
    """Quick helper function to get distance between two 2d vectors a and b."""
    return sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)


class Semicircle(Path):
    """Helper class to build a semi-circular path."""

    def __init__(self, origin, target, rotation=0, angle_dir='+', **extra):
        super().__init__(**extra)
        radius = distance(origin, target) / 2
        self.push('m', *origin)
        self.push_arc(target, rotation, radius, angle_dir=angle_dir, absolute=True)


class PrimeDiagram(Drawing):
    """Class representing a prime diagram, extending svgwrite.Drawing."""

    def __init__(self, iterations=100, circles=50, filename=None, **extra):
        self.iterations = iterations
        self.circles    = circles

        filename = filename or str(self.iterations)
        if not filename.endswith(".svg"):
            filename += ".svg"
        self.filename = filename
        super().__init__(filename, **extra)


    def __str__(self):
        return str(self.filename)


    def render(self):
        # Semicircles computation
        visited = {0}
        for multiple in range(2, self.circles):
            origin_x = 0
            target_x = multiple
            color = 'black'
            while target_x <= self.iterations:

                if origin_x == 0 and target_x not in visited :
                    direction = '-'
                    color = 'red'
                else:
                    direction = '+'
                
                semicircle = Semicircle((origin_x, 0), (target_x, 0), angle_dir=direction)
                semicircle.stroke(color, width=.6, opacity=.25)
                semicircle.fill('none')
                self.add(semicircle)
                
                visited.add(target_x)
                origin_x += multiple
                target_x += multiple
        
        # Number line
        for i in range(self.iterations + 1):
            circle = Circle((i, 0), .25)
            circle.stroke('black', width=.1)
            circle.fill('white')
            self.add(circle)
        
        self.stretch()
        self.save()


if __name__ == '__main__':
    diag = PrimeDiagram(100, 100)
    diag.render()