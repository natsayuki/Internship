with open ("male.txt", "r") as myfile:
    data=myfile.readlines()
for line in data:
    firstName = line.split()[1]
    with open("maleLast.txt", "a") as myfile:
        myfile.write('\n' + firstName)
