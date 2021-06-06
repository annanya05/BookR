import collab_filtering as cf
import demo_filtering2 as df
import content_filtering as ctf

def result(bname):
    cr = []
    cr = cf.recomendation()
    cr_n = cr[:5]

    dr = []
    dr = df.drecom()
    dr_n = dr[:2]

    ctr = []
    ctr = ctf.crecom(bname=bname)
    ctr_n = ctr[:3]

    print("CR", cr_n)
    print("CTR", ctr_n)
    print("DR", dr_n)

    comb1 = []
    comb1 = ctr_n + dr_n
    comb2 = []
    comb2 = comb1 + cr_n
    return comb2