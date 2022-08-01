import scipy
import numpy as np
import matplotlib.pyplot as plt

# result = scipy.fromfile(open('../data/lobee_result'), dtype=scipy.uint8)
result = scipy.fromfile(open('../data/lora_result'), dtype=scipy.uint8)
chirp_result = scipy.fromfile(open('../data/lora_chirp_result'), dtype=scipy.uint32)
# snr_pow = scipy.fromfile(open('../data/snr_pow'), dtype=scipy.float32)
# snr_db = scipy.fromfile(open('../data/snr_db'), dtype=scipy.uint8)
# signal_pow = scipy.fromfile(open('../data/signal_pow'), dtype=scipy.float32)
# noise_pow = scipy.fromfile(open('../data/noise_pow'), dtype=scipy.float32)

num_packets = 10
packet_len = 4
# packet_basic = np.array([18, 52, 86, 120], dtype=np.uint8) # 4 bytes 12 34 56 78
packet_basic = np.array([33, 67, 101, 135, 33, 67, 101], dtype=np.uint8) # 4 bytes 21 43 65 87
# packet = np.array([4, 128, 240], dtype=np.uint8) # 4 bytes
packet = np.array([7, 128, 0], dtype=np.uint8) # 7 bytes
# packet = np.array([8, 128, 144], dtype=np.uint8)  # 8 bytes
# packet = np.array([16, 129, 64], dtype=np.uint8) # 16 bytes
# packet = np.array([32, 129, 112], dtype=np.uint8) # 32bytes
# packet = np.array([64, 129, 16], dtype=np.uint8) # 64bytes
# packet = np.array([128, 129, 208], dtype=np.uint8) # 128bytes
for i in range(int(packet_len/4)):
    packet = np.concatenate((packet, packet_basic))
error_cnt = []
header_err_cnt = []
i = 0
while i < len(result):
    length = 3 + result[i]
    comp_result = []
    header_result = []
    for j in range(i, i+3):
        header_result.append(bin(packet[j-i] ^ result[j]).count('1'))
    for j in range(i, i+length):
        if (j-i) > 2+packet_len:
            break
        comp_result.append(bin(packet[j-i] ^ result[j]).count('1'))
    print(comp_result)
    # if length-comp_result.count(0) != 0:
    #     error_cnt.append(1)
    error_cnt.append(np.sum(comp_result))
    header_err_cnt.append(np.sum(header_result))
    i += length

print("Bit Error Rate: ", np.sum(error_cnt) / 8 / len(result))
print("Packet Reception Ratio: ", (len(error_cnt)-len(np.nonzero(header_err_cnt)[0]))/num_packets)
print("Frame Reception Ratio: ", (len(error_cnt)-len(np.nonzero(error_cnt)[0]))/num_packets)
# print("Average SNR dB: ", np.average(snr_db))
# print("Average Signal Power: ", np.average(signal_pow))
# print("Average Noise Power:", np.average(noise_pow))

snr = [i for i in range(-10, 11)]
signal = 1
noise = []
for i in range(len(snr)):
    noise.append(signal/pow(10, float(snr[i]/10)))
print("Noise Power: ", noise)
