import json
from PIL import Image, ImageDraw


class RegisterShape:
    data = {}

    @classmethod
    def registerShape(cls, name, dataCls):
        cls.data[name] = dataCls

    @classmethod
    def createShape(cls, data):
        name = list(data.keys())[0]
        classShape = cls.data.get(name)
        return classShape


class Frame:
    def __init__(self, config):
        self.config = config
        print(self.config)
        self.im = Image.new("RGB", (200, 200))
        self.drw = ImageDraw.Draw(self.im, "RGB")
        self.image_size = self.config['image_size']

    def save(self, output_folder):
        self.im.save(f"{output_folder}/img.png", "PNG")


class Shape:
    def __init__(self, shapeData, params, frame):
        self.drw = frame.drw


class Circle(Shape):
    def __init__(self, shapeData, params, frame):
        super().__init__(shapeData, params, frame)
        self.shapeData = shapeData

    def draw(self):
        self.centerX = self.shapeData['X_center']
        self.centerY = self.shapeData['Y_center']
        self.radius = self.shapeData['Radius']
        self.drw.ellipse([self.centerX - self.radius, self.centerY - self.radius, self.centerX + self.radius,
                          self.centerY + self.radius], fill="blue")


class Rectangle(Shape):
    def __init__(self, shapeData, params, frame):
        super().__init__(shapeData, params, frame)
        self.shapeData = shapeData

    def draw(self):
        self.leftUpX = self.shapeData['X_upper_left']
        self.leftUpY = self.shapeData['Y_upper_left']
        self.rightDwnX = self.shapeData['X_lower_right']
        self.rightDwnY = self.shapeData['Y_lower_right']
        self.drw.rectangle(((87, 18), (130, 92)), fill="white")


class Square(Rectangle):
    def __init__(self, shapeData, params, frame):
        super().__init__(shapeData, params, frame)
        self.shapeData = shapeData

    def draw(self):
        self.leftUpsqrX = self.shapeData['X_up_left']
        self.leftUpsqrY = self.shapeData['Y_up_left']
        self.side_length = self.shapeData['side_length']
        self.drw.rectangle(((11, 14), (11 + 10, 14 + 10)))


class Triangle(Shape):
    def __init__(self, shapeData, params, frame):
        super().__init__(shapeData, params, frame)
        self.shapeData = shapeData

    def draw(self):
        self.Point1 = self.shapeData['Point1']
        self.Point2 = self.shapeData['Point2']
        self.Point3 = self.shapeData['Point3']
        self.drw.polygon((tuple(self.Point1.values()), tuple(self.Point2.values()), tuple(self.Point3.values())),
                         fill="orange")


def drawImage():
    with open('config.json', 'r') as f:
        configRoot = json.load(f)

    with open(f"{configRoot['data_root_folder']}/config.json", 'r') as f:
        config = json.load(f)
        print(config)

    figures = config['figures']
    canvas = Frame(config)

    for figure in figures:
        figure_name = list(figure.keys())[0]
        match figure_name:
            case "Circle":
                figureClass = Circle
                RegisterShape.registerShape(figure_name, figureClass)
            case "Rectangle":
                figureClass = Rectangle
                RegisterShape.registerShape(figure_name, figureClass)
            case "Square":
                figureClass = Square
                RegisterShape.registerShape(figure_name, figureClass)
            case "Triangle":
                figureClass = Triangle
                RegisterShape.registerShape(figure_name, figureClass)

        shapeData = figure[f"{figure_name}"]['Shape']
        params = figure[f"{figure_name}"]['Params']
        shape = RegisterShape.createShape(figure)
        shape(shapeData, params, canvas).draw()
        canvas.save(configRoot['output_folder'])


drawImage()
