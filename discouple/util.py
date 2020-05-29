from abc import ABC


class Flags(ABC):
    class FlagList:
        @classmethod
        def collect_flags(cls):
            return {
                name: value
                for name, value in cls.__dict__.items()
                if isinstance(value, int)
            }

        @classmethod
        def max_value(cls):
            max_bits = max(cls.collect_flags().values()).bit_length()
            return (2 ** max_bits) - 1

    DEFAULT_VALUE = 0
    FLAGS = FlagList.collect_flags()

    def __init__(self, value=None, **kwargs):
        self.value = value or self.DEFAULT_VALUE
        for key, value in kwargs.items():
            flag = self.FLAGS.get(key)
            if flag is None:
                raise TypeError(f"{key} is not a valid flag name.")

            self._set_flag(flag, value)

    def reset(self):
        self.value = self.DEFAULT_VALUE

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def __int__(self):
        return int(self.value)

    def __getattr__(self, item):
        flag = self.FLAGS.get(item)
        if flag is not None:
            return self._has_flag(flag)

        raise AttributeError

    def __setattr__(self, key, value):
        flag = self.FLAGS.get(key)
        if flag is not None:
            return self._set_flag(flag, value)

        return super().__setattr__(key, value)

    def _set_flag(self, flag, value):
        if value:
            self.value |= flag

        else:
            self.value &= ~flag

    def _has_flag(self, flag):
        return (self.value & flag) == flag
