from structlog import PrintLogger, wrap_logger
from structlog.processors import JSONRenderer, TimeStamper

# renderers must come last
log = wrap_logger(PrintLogger(), processors=[TimeStamper(), JSONRenderer()])
