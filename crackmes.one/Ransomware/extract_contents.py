from scapy.all import rdpcap, TCP, Raw, IP
packets = rdpcap("RecordUser.pcapng")
tcp_data = bytearray()
src_ip = "192.168.134.1"
dst_ip = "192.168.134.132"

for pkt in packets:
    if TCP in pkt and Raw in pkt:
        if pkt[IP].src == src_ip and pkt[IP].dst == dst_ip and pkt[TCP].dport == 8888 and pkt[TCP].sport in [24027, 24028]:
            tcp_data += bytes(pkt[Raw].load)

length = tcp_data[:4]
length = int.from_bytes(length, byteorder='big')
file_1 = tcp_data[4:4+length]
file_2_length = tcp_data[4 + length:8 + length]
file_2_length = int.from_bytes(file_2_length, byteorder='big')
file_2 = tcp_data[8 + length : 8 + length + file_2_length]
assert 8 + length + file_2_length == len(tcp_data)
with open("file1_enc", "wb") as file:
    file.write(file_1)
with open("dll_enc", "wb") as file:
    file.write(file_2)
