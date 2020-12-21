import hashlib
from typing import List

from pydantic import BaseModel


class CodebookDTO(BaseModel):
    name: str
    tags: List[str]

    @property
    def id(self) -> str:
        """
        Computes the ID for the given Codebook by MD5-hashing it's JSON representation (after sorting tags)
        and adding its lowercase name as a prefix Note that this is just an identifier / handle that does not guarantee
        that data for the Codebook exists.
        :return: The ID as a string
        """
        self.tags.sort()
        return self.name.lower() + "_" + hashlib.md5(self.json().encode('utf-8')).hexdigest()
