from typing import Optional, Callable
from datetime import datetime
from xml.dom.minidom import parseString as parser_xml_from_str


async def send_response_in_one_call(
    send, status: int,
    message: bytes = b''
) -> None:
    """moved to  DAVResponse.send_in_one_call()
    """
    headers = [
        (b'Content-Type', b'text/html'),
        # (b'Content-Type', b'application/xml'),
        (b'Content-Length', bytes(str(len(message)), encoding='utf8')),
        (b'Date', bytes(datetime.utcnow().isoformat(), encoding='utf8')),
    ]
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': headers,
    })
    await send({
        'type': 'http.response.body',
        'body': message,
    })

    return


async def receive_all_data_in_one_call(receive: Callable) -> bytes:
    data = b''
    more_body = True
    while more_body:
        request_data = await receive()
        data += request_data.get('body', b'')
        more_body = request_data.get('more_body')

    return data


class DateTime:
    def __init__(self, timestamp: float):
        self.datetime = datetime.fromtimestamp(timestamp)

    def iso_850(self) -> str:
        return self.datetime.strftime(
            '%a, %d %b %Y %H:%M:%S GMT'
        )

    def iso_8601(self) -> str:
        return self.datetime.isoformat()[:19] + 'Z'


def pprint_xml(xml_str):
    xml = parser_xml_from_str(xml_str).toprettyxml()
    print(xml)
