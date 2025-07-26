from typing import Optional

from pydantic import BaseModel


class CallbackListElement(BaseModel):
    photo_index: Optional[int] = None
    text: str




if __name__ == '__main__':
    data = CallbackListElement(
        text='ewmfpwemfpwemf'
    )
    print(data.photo_path)