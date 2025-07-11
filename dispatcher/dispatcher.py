import asyncio
import io

from fastapi import FastAPI, UploadFile
from PIL import Image

class Dispatcher:
    def __init__(self):
        
        # This queue is going to hold inference requests:
        self.request_queue = asyncio.Queue()
        self.request = None


    
    async def qsize(self) -> int:
        "Returns the size of the queue as an int"
        return self.request_queue.qsize()


    async def add_to_queue(self, request, request_id) -> asyncio.queues.Queue:
        """
        This function receives requests from the load balancer and puts them in a queue using asyncio.
        
        1. Load tester will send 'workload/sec' (workload = number of requests) 
        2. I need to see how these requests are actually sent and then store them in the asyncio Queue.
        """

        image_bytes = await request.read() # The reqeuest is basically the image sent by the load tester.
        image = Image.open(io.BytesIO(image_bytes))
        await self.request_queue.put((image, request_id)) # Store tuple instead of just image
        return self.request_queue

    async def round_robin(self):
        
        pass