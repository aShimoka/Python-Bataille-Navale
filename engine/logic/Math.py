#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the cosine and sine functions.
from math import cos, sin, sqrt, atan2, degrees, radians


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            ArithmeticError("Cannot add a vector to something that is not a vector.")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            ArithmeticError("Cannot add a vector to something that is not a vector.")

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        else:
            ArithmeticError("Cannot add a vector to something that is not a vector.")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)
        else:
            ArithmeticError("Cannot divide a vector by something other that a number.")

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)
        else:
            ArithmeticError("Cannot divide a vector by something other that a number.")

    def __eq__(self, other):
        if isinstance(other, (Vector2)):
            return self.x == other.x and self.y == other.y
        else:
            ArithmeticError("Cannot divide a vector by something other that a vector.")

    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def tuple(self, integers=False):
        if integers:
            return tuple([round(self.x), round(self.y)])
        else:
            return tuple([self.x, self.y])

    def positive(self):
        return Vector2(abs(self.x), abs(self.y))

    def __str__(self):
        return "({:10.2f}, {:10.2f})".format(self.x, self.y)

    @staticmethod
    def in_rect(self, origin, size):
        extent = origin + size
        return (self.x > origin.x) and (self.x < extent.x) and (self.y > origin.y) and (self.y < extent.y)


UNIT_VECTOR = Vector2(1, 1)
RIGHT_VECTOR = Vector2(1, 0)
TOP_VECTOR = Vector2(0, 1)
ZERO_VECTOR = Vector2(0, 0)


class Mat3x3:
    """
    Simple 3x3 matrix.
    Used for 2D vector transformations.
    """

    def __init__(self, components=None):
        """
        Creates a new matrix with the given components.
        :param components: The components of the new matrix.
        """
        # If the components are unset.
        if components is None:
            # Load the default 0 matrix.
            components = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        if not isinstance(components, list):
            raise ArithmeticError("Mat3 constructor MUST use a list.")

        if len(components) != 3:
            raise ArithmeticError("Cannot create a Mat3x3 with " + str(len(components)) + " rows")

        for i in range(3):
            if len(components[i]) != 3:
                raise ArithmeticError("Cannot create a Mat3x3 with " + str(len(components[i])) + " columns")

        self.components = components

    @staticmethod
    def create_matrix(position, rotation, scale=UNIT_VECTOR):
        """
        Generates the matrix from the specified components.
        :param position: The position component to apply to the matrix.
        :param rotation: The rotation component to apply to the matrix.
        :param scale: The scale of the matrix.
        :returns: The generated matrix.
        """
        # Convert the rotation in radians.
        rotation = radians(rotation)
        # Create the three base matrices.
        t_mat = Mat3x3(
            [[1, 0, position.x],
             [0, 1, position.y],
             [0, 0, 1]]
        )
        r_mat = Mat3x3(
            [[cos(rotation), -sin(rotation), 0],
             [sin(rotation), cos(rotation), 0],
             [0, 0, 1]]
        )
        s_mat = Mat3x3(
            [[scale.x, 0, 0],
             [0, scale.y, 0],
             [0, 0, 1]]
        )

        # Compute the final matrix.
        return t_mat * r_mat * s_mat

    def __add__(self, other):
        """
        Adds two matrices together.
        :param other: The other matrix to add.
        :return: The added matrix.
        """
        if isinstance(other, Mat3x3):
            return Mat3x3([
                [
                 self.components[0][0] + other.components[0][0],
                 self.components[0][1] + other.components[0][1],
                 self.components[0][2] + other.components[0][2]
                 ],
                [
                 self.components[1][0] + other.components[1][0],
                 self.components[1][1] + other.components[1][1],
                 self.components[1][2] + other.components[1][2]
                ],
                [
                 self.components[2][0] + other.components[2][0],
                 self.components[2][1] + other.components[2][1],
                 self.components[2][2] + other.components[2][2]
                ]
            ])
        else:
            ArithmeticError("Cannot add a matrix to anything other than a matrix")

    def __mul__(self, other):
        """
        Adds two matrices together, or a matrix and a vector.
        :param other: The other matrix, or vector, to multiply.
        :return: The multiplied object.
        """
        out = Mat3x3()
        # If the other object is a matrix.
        if isinstance(other, Mat3x3):
            for i in range(3):
                for j in range(3):
                    out.components[i][j] = \
                        self.i(0, i) * other.i(j, 0) + \
                        self.i(1, i) * other.i(j, 1) + \
                        self.i(2, i) * other.i(j, 2)
            return out

        # If the other object is a vector2.
        elif isinstance(other, Vector2):
            return Vector2(
                (self.i(0, 0) * other.x) +
                (self.i(1, 0) * other.y) +
                (self.i(2, 0)),
                (self.i(0, 1) * other.x) +
                (self.i(1, 1) * other.y) +
                (self.i(2, 1))
            )
        else:
            raise ArithmeticError("Cannot multiply a matrix to anything other than a matrix")

    def i(self, x, y):
        return self.components[y][x]

    def get_rotation(self):
        return degrees(atan2(self.components[1][0], -self.components[0][1]))

    def get_translation(self):
        return Vector2(self.components[0][2], self.components[1][2])

    def get_scale(self):
        return Vector2(
            self.components[0][0] / self.components[1][0] if self.components[1][0] != 0 else 1,
            self.components[1][1] / -self.components[0][1] if self.components[0][1] != 0 else 1
        )

    def __str__(self):
        return "| {:10.5f} {:10.5f} {:10.5f} |\n| {:10.5f} {:10.5f} {:10.5f} |\n| {:10.5f} {:10.5f} {:10.5f} |".format(
            self.i(0, 0), self.i(1, 0), self.i(2, 0),
            self.i(0, 1), self.i(1, 1), self.i(2, 1),
            self.i(0, 2), self.i(1, 2), self.i(2, 2),
        )


IDENTITY_MATRIX = Mat3x3([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
ZERO_MATRIX = Mat3x3()
