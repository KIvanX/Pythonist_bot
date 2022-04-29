def main():
    input_file = open("input.txt", "r")
    output_file = open("output.txt", "w")
    line = input_file.readline().split()
    a, b = int(line[0]), int(line[1])
 
    while a != 0 and b !=0:
        if a > b:
            a = a % b
        else:
            b = b % a
 
    gcd = a + b
 
 
 
    output_file.write(str(gcd) + "\n")
main()