import itertools, csv, io

def full_factorial_3level(na,wp,overlay_um=.1):
    rows=[]
    i=1
    for a,b,c in itertools.product([.95,1.,1.05],[.95,1.,1.05],[-overlay_um,0.,overlay_um]):
        rows.append({"run":i,"NA_factor":a,"NA_cm3":na*a,"WP_factor":b,"WP_um":wp*b,"overlay_um":c,
                     "extract_BV":True,"extract_Ron":True,"extract_SC_hotspot":True})
        i+=1
    return rows

def to_csv(rows):
    out=io.StringIO(); w=csv.DictWriter(out,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows);return out.getvalue()
