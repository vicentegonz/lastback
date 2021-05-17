from django.db import models


class ExtendedQ(models.Q):
    def __xor__(self, other):
        neg_self = ~self
        neg_other = ~other
        return (self & neg_other) | (neg_self & other)
