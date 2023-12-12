def read_data_from_frame(raw_frame):
    raw_data = []
    for x in range(26, len(raw_frame)-8):
        raw_data.append(float.fromhex((raw_frame[x]))/1000)

    return raw_data