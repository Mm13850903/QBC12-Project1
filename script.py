def f1(a, b):
    f = open("main.text", "w")
    for i in a:
        temp = "N"
        temp1 = "N"
        for j in b:
            if j.name == i.line_name:
                temp = j.destination
                temp1 = j.source
                break
        f.write(i.name + " " + temp + " " + temp1 + " " + str(i.capacity) + " " + str(i.price) )
    f.close()

def f2(a, b, x, y):
    f = open("main.text", "a")
    f.write(a )
    f.write(b )
    f.write(str(x) )
    f.write(str(y) )
    f.close()