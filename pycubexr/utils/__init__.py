from typing import List, Any

from pycubexr.utils.logger import logger


def chunk_list(elements: List[Any], chunk_size: int):
    return [elements[x: x + chunk_size] for x in range(0, len(elements), chunk_size)]
