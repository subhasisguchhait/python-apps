import time
import logging
from fastapi import Request


logger = logging.getLogger("request")

async def log_requests(request: Request, call_next):    
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.3f}'.format(process_time)
    
    logger.info(f"{request.method} {request.url.path} completed_in={formatted_process_time} ms status_code={response.status_code}")
    
    return response