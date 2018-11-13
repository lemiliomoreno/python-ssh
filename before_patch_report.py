import subprocess as sp

def checking_for_root_space():
    print("********************")
    print("Checking if root has more than 20% space available...")
    first_for_root_check = ['df', '/']
    second_for_root_check = ['awk', """NR==2 {print $5}"""]

    p1 = sp.Popen(first_for_root_check, stdout=sp.PIPE)
    p2 = sp.Popen(second_for_root_check, stdin=p1.stdout, stdout=sp.PIPE)

    p1.stdout.close()

    out_to_test = p2.communicate()[0].decode('utf-8')
	
    if(out_to_test[:3] == '100'): print("CANT_PATCH: Root (/) has {0}% space left, need more than 20%.".format(int(out_to_test[:3]) - 100))
    elif(int(out_to_test[:2]) >= 80): print("CANT_PATCH: Root (/) has {0}% space left, need more than 20%.".format(abs(int(out_to_test[:2]) - 100)))
    else: print("OK_TO_PATCH: Root (/) has {0}% space left.".format(abs(int(out_to_test[:2]) - 100)))

    p2.stdout.close()
    print("********************")

checking_for_root_space()
