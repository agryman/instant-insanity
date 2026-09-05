"""
This module implements the ObjectToCountMapping class which can be used to keep
a running total of the occurrences of any object.
"""
class ObjectToCountMapping:
    """
    This class keeps tracks of counts on any set of objects.

    Attributes:
        object_to_count: the mapping of objects to counts.

    """
    object_to_count: dict[object, int]

    def __init__(self):
        self.object_to_count = {}

    def post_increment(self, key: object) -> int:
        """
        Returns the current count and increments it.
        A count of 0 is returned the first time the key is used.

        Args:
            key: the immutable object to increment.

        Returns:
            the count before incrementing.
        """

        count: int = self.object_to_count.get(key, 0)
        self.object_to_count[key] = count + 1
        return count
