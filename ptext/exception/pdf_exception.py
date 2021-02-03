from typing import Optional, Type, Union


class PDFException(Exception):
    """
    All built-in, PDF-related, non-system-exiting exceptions are derived from this class.
    All user-defined, PDF-related, exceptions should also be derived from this class.
    """

    def __init__(
        self, byte_offset: Optional[int] = None, message: Optional[str] = None
    ):
        super().__init__(message or "")
        self.byte_offset = byte_offset

    def set_byte_offset(self, byte_offset: int) -> "PDFException":
        self.byte_offset = byte_offset
        return self

    def get_byte_offset(self) -> Optional[int]:
        return self.byte_offset


class PDFSyntaxError(PDFException):
    def __init__(
        self,
        message: Optional[str] = None,
        byte_offset: Optional[int] = None,
    ):
        super(PDFSyntaxError, self).__init__(message=message, byte_offset=byte_offset)


class PDFTypeError(PDFException, TypeError):
    """
    PDFTypeError is thrown when an operation or function is applied to an object of an inappropriate type.
    """

    def __init__(
        self,
        received_type: Union[Type, None],
        expected_type: Type,
        byte_offset: Optional[int] = None,
    ):
        super(PDFTypeError, self).__init__(
            byte_offset=byte_offset,
            message="must be %s, not %s" % (expected_type, received_type),
        )


class PDFValueError(PDFException, ValueError):
    """
    PDFValueError is thrown when a function's argument is of an inappropriate type.
    """

    def __init__(
        self,
        received_value_description: str,
        expected_value_description: str,
        byte_offset: Optional[int] = None,
    ):
        super(PDFValueError, self).__init__(
            byte_offset=byte_offset,
            message="must be %s, not %s"
            % (expected_value_description, received_value_description),
        )


class PDFTokenNotFoundError(PDFException):
    def __init__(
        self, byte_offset: Optional[int] = None, message: Optional[str] = None
    ):
        super(PDFTokenNotFoundError, self).__init__(
            byte_offset=byte_offset, message=message
        )


class PDFCommentTokenNotFoundError(PDFTokenNotFoundError):
    """
    PDFCommentTokenNotFoundError is thrown when a PDF does not contain the magic comment '%PDF-X.X'
    """

    def __init__(self, byte_offset: Optional[int] = None):
        super(PDFCommentTokenNotFoundError, self).__init__(
            byte_offset=byte_offset,
            message="No token found that starts with %PDF-",
        )


class PDFEOFError(PDFException, EOFError):
    """
    PDFEOFError is thrown when the input (unexpectedly) hits the end-of-file condition.
    """

    def __init__(self, byte_offset: Optional[int] = None):
        super(PDFEOFError, self).__init__(
            byte_offset=byte_offset, message="Unexpectedly reached EOF"
        )
