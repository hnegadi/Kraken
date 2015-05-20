"""Kraken - objects.Attributes.NumberAttribute module.

Classes:
NumberAttribute - Base Attribute.

"""

from kraken.core.objects.attributes.attribute import Attribute
# import integer_attribute
# import float_attribute

class NumberAttribute(Attribute):
    """Number Attributee. Base class for number attribute types"""

    def __init__(self, name, value=0, minValue=None, maxValue=None, parent=None):
        super(NumberAttribute, self).__init__(name, value=value, parent=parent)

        self._min = None
        self._max = None
        self._uiMin = None
        self._uiMax = None

        if minValue is None:
            if value < 0:
                self.setMin(value)
            else:
                self.setMin(0)

        if maxValue is None:
            if value == 0:
                self.setMax(10)
            else:
                self.setMax(value * 3)


    # ==============
    # Value Methods
    # ==============
    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if self.validateValue(value) is False:
            raise TypeError("Value: '" + str(value) + "' has an invalid type!")

        super(NumberAttribute, self).setValue(value)

        return True


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
        """Sets the minimum value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        minimum -- float / integer, minimum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(minimum) in (int, float), "'minimum' is not of type 'int' \
                                              or 'float'."
        if self._max is not None and minimum > self._max:
            raise ValueError("Minimum value is greater than attribute maximum value")
        self._min = minimum

        return True


    def getMax(self):
        """Gets the maximum value for this attribute.

        Return:
        Float / Integer - maximum value.

        """

        return self._max


    def setMax(self, maximum):
        """Sets the maximum value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        maximum -- float / integer, maximum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(maximum) in (int, float), "'maximum' is not of type 'int' \
                                              or 'float'."
        if self._min is not None and maximum < self._min:
            raise ValueError("Maximum value is less than attribute minimum value")
        self._max = maximum

        return True


    def getUIMin(self):
        """Gets the default minimum ui slider value for this attribute.

        Return:
        Float / Integer - default minimum ui slider value.

        """

        return self._uiMin


    def setUIMin(self, minimum):
        """Sets the default minimum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        minimum -- float / integer, default minimum ui slider value.

        Return:
        True if successful.

        """

        if self.isTypeOf('IntegerAttribute'):
            if type(minimum) is not int:
                raise TypeError("UiMin value is not of type 'int'.")

        if self.isTypeOf('FloatAttribute'):
            if type(minimum) not in (int, float):
                raise TypeError("UiMin value is not of type 'int' or 'float'.")

        if self._uiMax is not None:
            if minimum > self._uiMax:
                raise ValueError('UiMin value is greater than attribute uiMax')

        if minimum > self._max:
            raise ValueError('UiMin value is greater than attribute maximum')

        if minimum < self._min:
            raise ValueError('UiMin value is less than attribute minimum')

        self._uiMin = minimum

        return True


    def getUIMax(self):
        """Gets the default maximum ui slider value for this attribute.

        Return:
        Float / Integer - default maximum ui slider value.

        """

        return self._uiMax


    def setUIMax(self, maximum):
        """Sets the default maximum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        maximum -- float / integer, default maximum ui slider value.

        Return:
        True if successful.

        """

        if self.isTypeOf('IntegerAttribute'):
            if type(maximum) is not int:
                raise TypeError("UiMax value is not of type 'int'.")

        if self.isTypeOf('FloatAttribute'):
            if type(maximum) not in (int, float):
                raise TypeError("UiMax value is not of type 'int' or 'float'.")

        if self._uiMin is not None:
            if maximum < self._uiMin:
                raise ValueError('UiMax value is less than attribute uiMin')

        if maximum < self._min:
            raise ValueError('UiMax value is less than attribute minimum')

        if maximum > self._max:
            raise ValueError('UiMax value is greater than attribute maximum')

        self._uiMax = maximum

        return True
