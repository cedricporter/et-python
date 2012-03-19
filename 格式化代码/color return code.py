inf = open("1.txt", "r")
text = ""
for line in inf.readlines():
    try:
        i = int(line[:2])
        line = line[:3] + "</font></strong>" + line[3:]
        line = '<strong><font color="#f79646">' + line
    except:
        pass
    text += line
print text
out = open("out.txt", 'w')
out.write(text)
