import json
from PIL import Image, ImageDraw
from matplotlib import colors


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
        self.image_size = self.config['image_size']
        self.im = Image.new("RGB", tuple(self.image_size.values()), color="lightgreen")
        self.drw = ImageDraw.Draw(self.im, "RGBA")


    def save(self, output_folder):
        self.im.save(f"{output_folder}/img.png", "PNG")


class Shape:
    def __init__(self, shapeData: dict, params: dict, frame):
        self.drw = frame.drw
        self.shapeData = shapeData
        self.params = params

        self.lineColor = self.params['Line_color']
        self.lineWidth = self.params['Line_width']
        self.color = colors.to_rgba(self.params['Color'])
        self.transparency = round((self.params['TransparencyPercent'] / 100), 2) * 255


class Circle(Shape):
    def draw(self):
        self.centerX = self.shapeData['X_center']
        self.centerY = self.shapeData['Y_center']
        self.radius = self.shapeData['Radius']

        color = []
        for i in range(len(self.color)):
            color.append(int(self.color[i] * 255))
        color = color[:-1]
        color.append(int(self.transparency))

        self.drw.ellipse(
            [self.centerX - self.radius, self.centerY - self.radius,
             self.centerX + self.radius, self.centerY + self.radius],
            fill=(tuple(color)), outline=self.lineColor, width=self.lineWidth
        )


class Rectangle(Shape):
    def draw(self):
        self.leftUpX = self.shapeData['X_upper_left']
        self.leftUpY = self.shapeData['Y_upper_left']
        self.rightDwnX = self.shapeData['X_lower_right']
        self.rightDwnY = self.shapeData['Y_lower_right']

        color = []
        for i in range(len(self.color)):
            color.append(int(self.color[i] * 255))
        color = color[:-1]
        color.append(int(self.transparency))

        self.drw.rectangle((
            (self.leftUpX, self.leftUpY),
            (self.rightDwnX, self.rightDwnY)),
            fill=(tuple(color)),
            outline=self.lineColor, width=self.lineWidth
        )


class Square(Rectangle):
    def draw(self):
        self.leftUpsqrX = self.shapeData['X_up_left']
        self.leftUpsqrY = self.shapeData['Y_up_left']
        self.sideLength = self.shapeData['side_length']

        colorSquare = []
        for i in range(len(self.color)):
            colorSquare.append(int(self.color[i] * 255))
        color = colorSquare[:-1]
        color.append(int(self.transparency))

        self.drw.rectangle((
            (self.leftUpsqrX, self.leftUpsqrY),
            (self.leftUpsqrX + self.sideLength, self.leftUpsqrY + self.sideLength)),
            fill=(tuple(color)), outline=self.lineColor, width=self.lineWidth
        )


class Triangle(Shape):
    def draw(self):
        self.Point1 = self.shapeData['Point1']
        self.Point2 = self.shapeData['Point2']
        self.Point3 = self.shapeData['Point3']

        color = []
        for i in range(len(self.color)):
            color.append(int(self.color[i] * 255))
        color = color[:-1]
        color.append(int(self.transparency))

        self.drw.polygon(
            (tuple(self.Point1.values()),
             tuple(self.Point2.values()),
             tuple(self.Point3.values())),
            fill=(tuple(color)), outline=self.lineColor, width=self.lineWidth
        )


def drawImage():
    with open('config.json', 'r') as f:
        configRoot = json.load(f)

    with open(f"{configRoot['data_root_folder']}/config.json", 'r') as f:
        config = json.load(f)

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
    print('Drawing Complete!')


drawImage()
