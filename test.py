rating1=0
rating2=None
rating3=None
rating4=None
rating5=None

for i in range(1,6):
    if (globals()['rating{}'.format(i)]) == None:
        globals()['rating{}'.format(i)] = 0
    globals()['star{}'.format(i)] = globals()['rating{}'.format(i)]
    print(globals()['star{}'.format(i)])