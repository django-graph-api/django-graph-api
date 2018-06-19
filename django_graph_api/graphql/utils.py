from traceback import format_exc

from django.conf import settings


class GraphQLError(Exception):
    def __init__(self, message, line=None, column=None):
        super(GraphQLError, self).__init__(message)

        self.message = message
        self.line = line
        self.column = column

        if settings.DEBUG:
            self.traceback = format_exc().split('\n')

    def serialize(self):
        serialized = {
            'message': self.message,
        }

        if self.line:
            serialized['line'] = self.line

            if self.column:
                serialized['column'] = self.column

        if settings.DEBUG:
            serialized['traceback'] = self.traceback

        return serialized

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.message == other.message

    def __hash__(self):
        return super(GraphQLError, self).__hash__() + self.message.__hash__()
