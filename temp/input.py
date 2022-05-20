input_file = open("input.txt", "r")
output_file = open("output.txt", "w")
line = input_file.readline().split()
n, m, r = int(line[0]), int(line[1]),  int(line[2])
v = n * m * r
s = n * m * 2 + n * r * 2 + m * r * 2


output_file.write(str(s) + " " + str(v) + "\n"))