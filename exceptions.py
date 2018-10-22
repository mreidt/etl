class Error(Exception):
   """Base class for other exceptions"""
   pass

class NotAType(Error):
   """Raised when the input file extension is not accepted"""
   pass

class NoInputFiles(Error):
   """Raised when input files are not provided"""
   pass

class GMAPSError(Error):
   """Raised when GMaps API return an error"""
   pass

class LatitudeWrongValue(Error):
   """Raised when a latitude have an wrong value."""
   pass

class LongitudeWrongValue(Error):
   """Raised when a longitude have an wrong value."""
   pass
