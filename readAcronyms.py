

with open("diseasesAcronyms.txt", "r") as f:
    lines = f.readlines()


for line in lines:
    fields = line.split(",")
    print fields[0], fields[1].strip()

