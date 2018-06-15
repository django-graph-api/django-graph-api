from traceback import format_exc

from django.conf import settings


class GraphQLError(Exception):
    def __init__(self, message):
        super(GraphQLError, self).__init__(message)
        self.message = message
        if settings.DEBUG:
            self.traceback = format_exc().split('\n')

    def serialize(self):
        return {'message': self.message}

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.message == other.message

    def __hash__(self):
        return super(GraphQLError, self).__hash__() + self.message.__hash__()
