"""Kraken - objects.Attributes.NumberAttribute module.

Classes:
NumberAttribute - Base Attribute.

"""

from attribute import Attribute


class NumberAttribute(Attribute):
    """Number Attributee. Base class for number attribute types"""

    def __init__(self, name, value=0, minValue=None, maxValue=None, keyable=None, lock=None):
        super(NumberAttribute, self).__init__(name, value, keyable=keyable, lock=lock)

        self._min = None
        self._max = None
        if minValue is not None:
            self.setMin(minValue)
        if maxValue is not None:
            self.setMax(maxValue)


    # ==================
    # Min / Max Methods
    # ==================
    def getMin(self):
        """Gets the minimum value for this attribute.

        Return:
        Float / Integer - minimum value.

        """

        return self._min


    def setMin(self, minimum):
        """Sets the minimum value for the attributeself.

        Note: Only works on float or integer attributes.

        Arguments:
        min -- float / integer, minimum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(minimum) in (int, float), "'minimum' is not of type 'int' or 'float'."

        self._min = minimum

        return True


    def getMax(self):
        """Gets the maximum value for this attribute.

        Return:
        Float / Integer - maximum value.

        """

        return self._max


    def setMax(self, maximum):
        """Sets the maximum value for the attributeself.

        Note: Only works on float or integer attributes.

        Arguments:
        min -- float / integer, maximum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(maximum) in (int, float), "'maximum' is not of type 'int' or 'float'."

        self._max = maximum

        return True
