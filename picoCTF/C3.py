ct_file = open("ciphertext", "r")
ct = ct_file.read()
ct_file.close()
prev = 0
res = ""
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"
for char in ct:
    ind = lookup2.find(char)
    in_lookup1 = (ind + prev) % 40
    res += lookup1[in_lookup1]
    prev = in_lookup1
print(res)
