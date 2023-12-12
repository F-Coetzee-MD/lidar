import json

file = open("./settings/modbus_messages.json", "r")
jsonF = json.load(file)

file = open("./settings/file_handler.json", "r")
settings = json.load(file)

file = open("./settings/variables.json", "r")
variables = json.load(file)

file.close()


def to_word(decimal):
    msb = (decimal >> 8) & 0xff
    lsb = decimal & 0xff
    return [msb, lsb]


def to_byte(decimal):
    return [decimal]


def word_to_decimal(msb, lsb):
    return (msb << 8) + lsb


def initiate_log_counts():
    frame_count = int(len(variables["names"])/settings["plc max data per frame"])
    frame_lengths = []

    for x in range(frame_count):
        frame_lengths.append(settings["plc max data per frame"])
	
    frame_lengths.append(len(variables["names"]) - sum(frame_lengths))

    if (frame_lengths[len(frame_lengths)-1] == 0):
        frame_lengths.pop()

    return frame_lengths


def initiate_modbus_overheads():
    frame = []
    frame += to_word(jsonF["transaction id"])
    frame += to_word(jsonF["protocol id"])
    frame += to_word(jsonF["length"])
    frame += to_byte(jsonF["device address"])
    frame += to_byte(jsonF["function code"])
    frame += to_word(jsonF["register"])
    frame += to_word(jsonF["byte count"])
    return frame


def read_modbus_message(raw_frame):
    # exstract the data from the modbus frame
    data = []

    for count in range(int(raw_frame[8]/2)):
        position = count*2 + 9
        data.append(str(word_to_decimal(raw_frame[position], raw_frame[position+1])/variables["devider"]))

    return data


def create_modbus_frame(start, count, frame):
	start_register = to_word(start)
	register_count = to_word(count)
	frame[8] = start_register[0]
	frame[9] = start_register[1]
	frame[10] = register_count[0]
	frame[11] = register_count[1]
	return frame


def check_frame_valid(raw_frame):
    if (raw_frame[7] == 83): 
        if (len(raw_frame) == 9):
            if (raw_frame[8] != 0):
                return False

    return True
