import time

from java.net import Socket, InetSocketAddress
from java.io import BufferedInputStream, BufferedOutputStream
from java.lang import Exception as JavaException


ENQ = 0x05
ACK = 0x06
NAK = 0x15
STX = 0x02
ETX = 0x03
DLE = 0x10

DEFAULT_IP = "10.55.27.31"
DEFAULT_PORT = 1024
DEFAULT_TIMEOUT = 5000


def bytes_to_hex(values):
    return " ".join([
        "%02X" % (value & 0xFF)
        for value in values
    ])


def apply_dynamic_values(text):
    now = system.date.now()

    if text is None:
        text = ""
    else:
        text = str(text)

    text = text.replace(
        "{TIME}",
        system.date.format(now, "HH:mm:ss")
    )

    text = text.replace(
        "{DATE}",
        system.date.format(now, "dd/MM/yy")
    )

    text = text.replace(
        "{DATETIME}",
        system.date.format(now, "dd/MM/yy HH:mm:ss")
    )

    return text


def socket_exchange(
    send_bytes,
    ip=DEFAULT_IP,
    port=DEFAULT_PORT,
    timeout=DEFAULT_TIMEOUT
):
    sock = None

    try:
        sock = Socket()

        sock.connect(
            InetSocketAddress(str(ip), int(port)),
            int(timeout)
        )

        sock.setSoTimeout(int(timeout))

        out = BufferedOutputStream(
            sock.getOutputStream()
        )

        inp = BufferedInputStream(
            sock.getInputStream()
        )

        out.write(
            send_bytes,
            0,
            len(send_bytes)
        )

        out.flush()

        response = []

        try:
            while True:
                value = inp.read()

                if value == -1:
                    break

                response.append(value)

                if value == ACK or value == NAK:
                    break

        except:
            pass

        return {
            "success": (
                len(response) > 0
                and response[-1] == ACK
            ),
            "sentBytes": list(send_bytes),
            "sentHex": bytes_to_hex(send_bytes),
            "responseBytes": response,
            "responseHex": bytes_to_hex(response),
            "responseText": "".join([
                chr(value)
                for value in response
            ])
        }

    except JavaException as error:
        return {
            "success": False,
            "error": str(error),
            "sentBytes": list(send_bytes),
            "sentHex": bytes_to_hex(send_bytes),
            "responseBytes": [],
            "responseHex": "",
            "responseText": ""
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
            "sentBytes": list(send_bytes),
            "sentHex": bytes_to_hex(send_bytes),
            "responseBytes": [],
            "responseHex": "",
            "responseText": ""
        }

    finally:
        if sock is not None:
            try:
                sock.close()
            except:
                pass


def test_enq():
    packet = bytearray()
    packet.append(ENQ)

    return socket_exchange(packet)


def write_packet_with_enq(packet):
    enq_result = test_enq()

    if not enq_result["success"]:
        return {
            "success": False,
            "stage": "ENQ",
            "enqResult": enq_result
        }

    write_result = socket_exchange(packet)

    return {
        "success": write_result["success"],
        "stage": "WRITE",
        "enqResult": enq_result,
        "writeResult": write_result
    }


def write_item_with_enq(item_number, text):
    item_number = int(item_number)
    text = apply_dynamic_values(text)

    packet = bytearray()

    packet.append(STX)
    packet.append(DLE)
    packet.append(0x30 + item_number)

    packet.extend(
        str(text).encode("ascii", "ignore")
    )

    packet.append(ETX)

    result = write_packet_with_enq(packet)

    result["item_number"] = item_number
    result["text"] = str(text)

    return result


def read_message_tags(message_number):
    message_number = int(message_number)

    base = (
        "[default]Hitachi_UX2/message%s"
        % message_number
    )

    tag_paths = [
        base + "/line1",
        base + "/line2"
    ]

    tag_values = system.tag.readBlocking(
        tag_paths
    )

    return {
        "message_number": message_number,
        "line1": (
            ""
            if tag_values[0].value is None
            else str(tag_values[0].value)
        ),
        "line2": (
            ""
            if tag_values[1].value is None
            else str(tag_values[1].value)
        ),
        "quality1": str(tag_values[0].quality),
        "quality2": str(tag_values[1].quality),
        "quality1Good": tag_values[0].quality.isGood(),
        "quality2Good": tag_values[1].quality.isGood()
    }


def write_message_from_tags(message_number):
    message_number = int(message_number)

    if message_number not in [1, 2, 3, 4]:
        return {
            "success": False,
            "stage": "VALIDATION",
            "error": (
                "Message number must be 1, 2, 3 or 4. "
                "Received: %s"
                % message_number
            )
        }

    message = read_message_tags(
        message_number
    )

    if not message["quality1Good"]:
        return {
            "success": False,
            "stage": "TAG_QUALITY",
            "error": (
                "Bad quality on message%s/line1: %s"
                % (
                    message_number,
                    message["quality1"]
                )
            )
        }

    if not message["quality2Good"]:
        return {
            "success": False,
            "stage": "TAG_QUALITY",
            "error": (
                "Bad quality on message%s/line2: %s"
                % (
                    message_number,
                    message["quality2"]
                )
            )
        }

    line1 = apply_dynamic_values(
        message["line1"]
    )

    line2 = apply_dynamic_values(
        message["line2"]
    )

    result_line1 = write_item_with_enq(
        1,
        line1
    )

    if not result_line1["success"]:
        return {
            "success": False,
            "stage": "LINE1",
            "message_number": message_number,
            "line1": line1,
            "line2": line2,
            "result_line1": result_line1
        }

    time.sleep(0.5)

    result_line2 = write_item_with_enq(
        2,
        line2
    )

    return {
        "success": (
            result_line1["success"]
            and result_line2["success"]
        ),
        "stage": (
            "COMPLETE"
            if result_line2["success"]
            else "LINE2"
        ),
        "message_number": message_number,
        "line1": line1,
        "line2": line2,
        "result_line1": result_line1,
        "result_line2": result_line2
    }


def test_printer_enq():
    return test_enq()


def test_printer_write(text="TEST {DATETIME}"):
    return write_item_with_enq(
        1,
        text
    )


def test_message1():
    return write_message_from_tags(1)


def test_message2():
    return write_message_from_tags(2)


def test_message3():
    return write_message_from_tags(3)


def test_message4():
    return write_message_from_tags(4)