class CeayDocsError(Exception):
    """Base class for internal CeayDocs exceptions."""


class ConversionError(CeayDocsError):
    pass


class CompressionError(CeayDocsError):
    pass


class FileValidationError(CeayDocsError):
    pass


class UnsupportedFormatError(CeayDocsError):
    pass


class OCRProcessingError(CeayDocsError):
    pass

