import ciso8601


class ObjectUtils:

    @staticmethod
    def to_string(value):
        new_value = str(value).strip()
        if not new_value:
            raise ValueError("Empty column value")
        return new_value

    @staticmethod
    def to_integer(value):
        return int(ObjectUtils.to_string(value))

    @staticmethod
    def to_number(value):
        return float(ObjectUtils.to_string(value))

    @staticmethod
    def to_datetime(value):
        return ciso8601.parse_datetime(ObjectUtils.to_string(value))
