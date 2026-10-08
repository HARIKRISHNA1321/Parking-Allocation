import csv
import os
from linalg import subtract,l1_norm,l2_norm,argmin

COMPATIBLE={"Standard":["Standard"],"EV":["EV"]}
ROAD_ROWS=(0,3,6)
MAX_X=7
MAX_Y=6
slots=[]

def reset():
    slots.clear()
    path=os.path.join(os.path.dirname(__file__),"slots.csv")
    with open(path) as f:
        for row in csv.DictReader(f):
            slots.append({"id":row["id"],"x":int(row["x"]),"y":int(row["y"]),
                          "type":row["type"],"status":row["status"]})

# road cells: column 0 and the horizontal road rows 0, 3 and 6
def is_road(x,y):
    return 0<=x<=MAX_X and 0<=y<=MAX_Y and (x==0 or y in ROAD_ROWS)

def candidate_slots(vehicle_type):
    return [s for s in slots
            if s["status"]=="Available" and s["type"] in COMPATIBLE[vehicle_type]]

# the car drives only on road cells and cannot pass through parking slots,
# so a trip is a list of straight road legs; each leg length is an L1 norm
def road_legs(p,q):
    if (p[0]==0 and q[0]==0) or p[1]==q[1]:
        points=[p,q]
    else:
        # p -> column 0 -> along column 0 -> q
        points=[p,(0,p[1]),(0,q[1]),q]
    legs=[]
    for start,end in zip(points,points[1:]):
        d=subtract(end,start)
        if l1_norm(d)>0:
            legs.append({"from":start,"to":end,"d":d,"l1":l1_norm(d)})
    return legs

def road_distance(p,q):
    return sum(leg["l1"] for leg in road_legs(p,q))

# a slot is entered from a neighbouring road cell; distance = road trip + 1 step into the slot
def best_entry(slot,vehicle):
    x=slot["x"]
    y=slot["y"]
    entries=[c for c in [(x,y-1),(x,y+1),(x-1,y),(x+1,y)] if is_road(c[0],c[1])]
    costs=[road_distance(vehicle,c)+1 for c in entries]
    i=argmin(costs)
    return entries[i],costs[i]

def find_best_slot(x,y,vehicle_type):
    vehicle=(x,y)
    rows=[]
    for s in candidate_slots(vehicle_type):
        d=subtract((s["x"],s["y"]),vehicle)
        entry,road_l1=best_entry(s,vehicle)
        rows.append({"id":s["id"],"x":s["x"],"y":s["y"],"diff":d,"entry":entry,
                     "direct_l1":l1_norm(d),"l1":road_l1,"l2":l2_norm(d)})
    if not rows:
        return None
    # s*=argmin road L1 distance, ties broken by straight-line ||S_i-V||_2
    keys=[(r["l1"],round(r["l2"],9)) for r in rows]
    best=rows[argmin(keys)]
    best["legs"]=road_legs(vehicle,best["entry"])
    nearest=rows[argmin([r["direct_l1"] for r in rows])]
    return {"vehicle":vehicle,"rows":rows,"best":best,"nearest":nearest}

def allocate(slot_id):
    for s in slots:
        if s["id"]==slot_id:
            s["status"]="Occupied"

reset()
