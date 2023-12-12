import numpy as np
from file_reader import FileReader

# Remove ehen in production
from debugger import Debugger
debugger = Debugger()

class DSP:
    def __init__ (self):
        file_reader = FileReader()
        self.dsp_const = file_reader.load_json("../settings/dsp.json")

    def butterworth_filter(self, data):
        n = self.dsp_const["butterworth order"]
        wc = self.dsp_const["butterworth cutoff"]
        fft = np.fft.fft(data)
        debugger.plot([fft], ["butterworth before"])
        for s in range(1, len(fft)):
            fft[s] = fft[s]/(1 + (s/wc)**(2*n))
        debugger.plot([fft], ["butterworth after"])
        return np.fft.ifft(fft)

    def moving_average(self, data):
        new_data = []
        size = self.dsp_const["moving avg size"]
        for x in range(len(data)-size):
            new_data.append(sum(data[x:x+size])/size)
        return new_data

    def remove_positive_peaks(self):
        print()

    def fft_filter(self, data):
        p = self.dsp_const["fft cutoff %"]/100
        fft = np.fft.fft(data)
        # debugger.plot([fft], ["fft old"])
        for s in range(int(len(fft)*p), len(fft)): fft[s] = 0
        # debugger.plot([fft], ["fft new"])
        return np.fft.ifft(fft)

    def amplify_signal(self, data):
        a = self.dsp_const["signal amplifier"]
        aplified_data = []
        for x in range(len(data)):
            aplified_data.append(a*data[x])
        return aplified_data

    def detect_plumb_line(self):
        print()
