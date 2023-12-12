import sys
from dsp import DSP
from debugger import Debugger
from tcp_ip import TCPClient
from file_reader import FileReader
from lidar import read_data_from_frame

if __name__ == "__main__":
    # Initiate Settings and Debuggers
    dsp = DSP()
    debugger = Debugger()
    file_reader = FileReader()
    comms = file_reader.load_json("../settings/communication.json")
    msgs = file_reader.load_json("../settings/lidar_messages.json")

    # Initiate LiDARs
    lidarA = TCPClient(comms["lidarA IP"], comms["lidarA PORT"])
    lidarB = TCPClient(comms["lidarB IP"], comms["lidarB PORT"])

    try:
        # Connect to LiDARs
        lidarA.connect()
        lidarB.connect()

        # Start LiDARs
        lidarA.send_message(msgs["start lidar"])
        lidarB.send_message(msgs["start lidar"])

        # Remove initial responses from buffer
        lidarA.receive_response()
        lidarB.receive_response()

    except: 
        # Close LiDAR connections
        lidarA.close_connection()
        lidarB.close_connection()
        sys.exit()

# debugger.save_array_to_txt(raw_data, "../test/test_data.txt")

    while True:
        # try:
            for lidar in [lidarA, lidarB]:
                # get data from lidar
                lidar.send_message(msgs["poll one telegram"])

                # wait for lidar response
                frame = lidar.receive_response()

                # proccess data
                raw_data = read_data_from_frame(frame)
                moving_avg = dsp.moving_average(raw_data)
                fft_data = dsp.fft_filter(moving_avg)
                butterworth = dsp.butterworth_filter(fft_data)
                amplified = dsp.amplify_signal(butterworth)

                # Do some Debugging
                # debugger.plot([raw_data, fft_data], ["raw data", "fft filtered data"])
                # debugger.plot([raw_data, moving_avg], ["raw data", "moving average filtered"])
                debugger.plot([raw_data, amplified], ["raw data", "buttered signal"])

                # get final position readings


                # send results to plc

        # except: break