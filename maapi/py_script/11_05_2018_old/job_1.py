
"""Zadanie nr1 """
def gen_post_codes(code_from, code_to):
    codes_list=[]
    codes_range  = (int("{0}{1}".format(
                                        code_from[:2],
                                        code_from[3:])),
                    int("{0}{1}".format(
                                        code_to[:2],
                                        code_to[3:])))

    for codes in range(min(codes_range),max(codes_range)+1):
        codes_list.append("{0}-{1}".format(
                                        str(codes)[:2],
                                        str(codes)[2:]))
    return codes_list

"""Zadanie nr2 """
def lost_number_checker(num_list,n):
    num = []
    for n in range(1,n+1):
        if n not in num_list:
            num.append(n)
    return num

"""Zadanie nr2 """
def number_gen(n_from, n_to):
    n_gen =[]
    for i in range(int(n_from*10),int(n_to*10)+1,5):
        n_gen.append(float(i)/10)
    return(n_gen)


print ("Lista kodow pocztowych:")
print (gen_post_codes("79-900", "81-155"))
print ("\n\n")

print ("Zaginone cyfry:")
print (lost_number_checker([2,3,7,4,9],10))
print ("\n\n")

print ("generator liczb:")
print (number_gen(2,5.5))
print ("\n\n")
