from matplotlib import pyplot
import numpy as np


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, theta):
        x_new = self.x * np.cos(theta) - self.y * np.sin(theta)
        y_new = self.x * np.sin(theta) + self.y * np.cos(theta)
        self.x = x_new
        self.y = y_new

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def divide(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __add__(self, other): # Enables Vector + Vector
        if isinstance(other, Vector):
            return self.add(other)
        raise TypeError("Can only add another Vector.")

    def __sub__(self, other): # Enables Vector - Vector
        if isinstance(other, Vector):
            return self.subtract(other)
        raise TypeError("Can only subtract another Vector.")

    def __truediv__(self, scalar): # Enables Vector / Scalar
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return self.divide(scalar)
        raise TypeError("Can only divide by a scalar (int or float).")


class Arrow:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def get_point(self):
        return Vector(
            self.position.x + self.direction.x, self.position.y + self.direction.y
        )

    def rotate(self, theta):
        self.direction.rotate(theta)


class Visualizer:
    def __init__(self, size=10):
        self.size = size
        self.xlim = [-(size / 2), (size / 2)]
        self.ylim = [-(size / 2), (size / 2)]

        self.fig, self.ax = pyplot.subplots(figsize=(self.size, self.size))
        self.ax.set_xlim(self.xlim[0], self.xlim[1])
        self.ax.set_ylim(self.ylim[0], self.ylim[1])

        self.points_x = []
        self.points_y = []

        pyplot.ion()

    def clear_canvas(self):
        self.ax.clear()
        self.ax.set_xlim(self.xlim[0], self.xlim[1])
        self.ax.set_ylim(self.ylim[0], self.ylim[1])

    def draw_arrow(self, arrow, color="b", head_width=0.1, head_length=0.1):
        self.ax.arrow(
            arrow.position.x,
            arrow.position.y,
            arrow.direction.x,
            arrow.direction.y,
            head_width=head_width,
            head_length=head_length,
            fc=color,
            ec=color,
        )

    def draw_points(self):
        self.ax.plot(self.points_x, self.points_y)

    def add_point(self, point):
        self.points_x.append(point.x)
        self.points_y.append(point.y)

    def draw_circle(self, center, radius, color="b"):
        circle = pyplot.Circle((center.x, center.y), radius, color=color, fill=False)
        self.ax.add_artist(circle)

    def draw_dot(self, center, radius=0.1, color="b"):
        circle = pyplot.Circle((center.x, center.y), radius, color=color, fill=True)
        self.ax.add_artist(circle)


class RideModel:
    def __init__(self, big_circle_radius, small_circle_radius, big_circle_angular_velocity, small_circle_angular_velocity):
        self.big_circle_radius = big_circle_radius
        self.small_circle_radius = small_circle_radius
        self.big_w = big_circle_angular_velocity
        self.small_w = small_circle_angular_velocity

        self.big_arrow = Arrow(Vector(0, 0), Vector(0, self.big_circle_radius))
        self.small_arrow = Arrow(
            self.big_arrow.direction, Vector(0, self.small_circle_radius)
        )
        self.velocity_arrow = Arrow(self.small_arrow.direction, Vector(0, 0))
        self.acceleration_arrow = Arrow(self.small_arrow.direction, Vector(0, 0))

        self.dt = 0.05
        self.steps = 1000

        self.visualizer = Visualizer()

    def calculate(self):
        resulting_before = (
            self.big_arrow.position
            + self.big_arrow.direction
            + self.small_arrow.direction
        )
        velocity_before = self.velocity_arrow.direction

        self.big_arrow.rotate(self.big_w * self.dt)

        self.small_arrow.position = self.big_arrow.position + self.big_arrow.direction
        self.small_arrow.rotate(self.small_w * self.dt)

        resulting_after = (
            self.big_arrow.position
            + self.big_arrow.direction
            + self.small_arrow.direction
        )
        self.velocity_arrow.position = (
            self.big_arrow.position
            + self.big_arrow.direction
            + self.small_arrow.direction
        )
        self.velocity_arrow.direction = resulting_after - resulting_before
        self.velocity_arrow.direction /= self.dt

        self.acceleration_arrow.position = self.velocity_arrow.position
        self.acceleration_arrow.direction = (
            self.velocity_arrow.direction - velocity_before
        )
        self.acceleration_arrow.direction /= self.dt

        self.visualizer.add_point(self.small_arrow.get_point())

    def draw(self):
        # self.visualizer.draw_circle(
        #     self.big_arrow.position, self.big_circle_radius, color="b"
        # )
        self.visualizer.draw_circle(
            self.small_arrow.position, self.small_circle_radius, color="b"
        )
        #self.visualizer.draw_arrow(self.big_arrow)
        #self.visualizer.draw_arrow(self.small_arrow)
        self.visualizer.draw_dot(self.velocity_arrow.position, color="r")
        self.visualizer.draw_arrow(self.velocity_arrow, color="r")
        self.visualizer.draw_arrow(self.acceleration_arrow, color="g")
        self.visualizer.draw_points()

    def run(self):
        for t in range(0, self.steps):
            self.visualizer.clear_canvas()
            self.calculate()
            self.draw()
            pyplot.pause(self.dt)


if __name__ == "__main__":
    model = RideModel(
        big_circle_radius=2,
        small_circle_radius=1,
        big_circle_angular_velocity=-1.25,
        small_circle_angular_velocity=0.75
        )
    model.run()
