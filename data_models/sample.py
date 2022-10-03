count=0
while True:
    n = input("Enter your number")
    if n.isdigit():
        count+=1
    elif n =='':
        print("Total counter value : {}".format(count))
        break
    else:
        print("Input {} must be an integer".format(n))