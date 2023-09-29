mydict={}

#mydict["Jingting"] = 3
print(mydict)

if "Jingting" in mydict:
    mydict["Jingting"] += 10000000
else:
    mydict["Jingting"] = 10000000

print(mydict)