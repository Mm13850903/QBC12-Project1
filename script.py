def f1(trains_list, lines_list):
    f = open("main.text", "w")
    for i in trains_list:
        temp = "N"
        temp1 = "N"
        for j in lines_list:
            if j.name == i.line_name:
                temp = j.destination
                temp1 = j.source
                break
        f.write(i.name + " " + temp + " " + temp1 + " " + str(i.capacity) + " " + str(i.price) )
    f.close()

def f2(a, b, count,total_price ):
    f = open("main.text", "a")
    f.write(a )
    f.write(b )
    f.write(str(count) )
    f.write(str(total_price) )
    f.close()