from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)

def test_log(request):
    logger.debug("Debug Message from View")
    logger.info("Info Message from View")
    logger.error("Error Message from View")
    return HttpResponse("Log successfully written.")
