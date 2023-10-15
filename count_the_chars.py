strng = input()

thisdict = {}

for i in range(len(strng)):
    if strng[i] not in thisdict:
        thisdict[strng[i]] = 1
    else:
        thisdict[strng[i]] += 1

print(thisdict)