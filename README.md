# Smart Parking Allocation System

Mini project for UE25MA242A - Mathematical Foundation for AI & Data Science (MFAD).

## Problem Statement

Finding a suitable parking slot manually can be inefficient when multiple slots are available. The system uses vector-based distance calculations to automatically select a nearby suitable slot.

## Mathematical Concepts

**Vectors.** The vehicle is V = (x_v, y_v) and each slot is S_i = (x_i, y_i). The relative vector is d_i = S_i - V = (x_i - x_v, y_i - y_v).

**L1 norm (Manhattan distance).** ||d||_1 = |d_x| + |d_y|. It models movement along lanes of a grid, which suits a parking lot. A car cannot drive through parking slots, so its trip is a sequence of straight road legs, and the trip length is the sum of the L1 norms of the legs (the road L1 distance).

**L2 norm (Euclidean distance).** ||d||_2 = sqrt(d_x^2 + d_y^2). It is the straight-line distance S_i - V and is used as the tie-breaker.

**Argmin.** s* = argmin_i D_i selects the slot with the smallest road L1 distance D_i (the car drives to a road cell next to the slot, then 1 step into it). If several slots share the minimum, the one with the smallest ||S_i - V||_2 is chosen.

## Practical Application

1. Vectors turn positions into coordinates, so the offset to every slot can be computed.
2. The L1 norm of each road leg gives the driving distance to the slot's entry cell (the allocation metric). The road is column 0 and rows 0, 3 and 6; a leg never crosses a slot.
3. The L2 norm gives the straight-line distance (tie-break and display).
4. Argmin picks the single best slot from the candidates. The slot is only recommended; it becomes Occupied when the user clicks Allocate.

Compatibility rules: a Standard vehicle uses Standard slots, an EV vehicle uses EV slots. Only available, compatible slots are candidates.

## Workflow

Vehicle position -> vectors -> norms -> distance comparison -> argmin -> recommended slot -> user chooses Allocate or Don't Allocate

## Files

- `app.py` - Flask app, one page
- `parking.py` - slots, compatibility, candidates, best slot, allocate, reset
- `linalg.py` - vector subtraction, L1 norm, L2 norm, argmin
- `slots.csv` - 28 slots with ID, x, y, type, status (all start Available)
- `templates/index.html` - the single page

## Installation

```
cd parking-allocation
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```
python app.py
```

Open http://127.0.0.1:5000 in a browser. No internet is needed.

## Grid Layout

Slot IDs are row letter + column number. x is the column (1-7, left to right) and y is the row (A=1, B=2, D=4, E=5, top to bottom). So B3 = (3,2).

Column 0 and rows 0, 3 and 6 are the road (there are no slots in those rows), so every slot touches a road. The vehicle position is chosen by clicking a road cell, which sets V = (x,y) and shows it above the grid as a pair (x,y).

After Find Best Slot, the recommended slot is highlighted and the Calculations section shows the candidate table, the leg-by-leg route to the recommended slot, and (when relevant) the slot that looked nearest in a straight line but is not reachable directly. Click Allocate to make it Occupied (grey) or Don't Allocate to leave it Available.

## Example

All slots start Available. Vehicle type Standard, V = (6,3) (click the road at row 3, column 6). Suppose B5, B6, D5, D6 and D7 are already occupied.

A6 = (6,1) is only |0| + |-2| = 2 away by direct L1, but the car cannot drive through B6 or any other slot. It must drive along the road: (6,3) -> (0,3) -> (0,0) -> (6,0), which is 6 + 3 + 6 = 15, plus 1 step into the slot, so its road L1 distance is 16.

B4 = (4,2) is entered from the road cell (4,3), which is 2 steps away, plus 1 step into the slot:

| Slot | S | S - V | Entry cell | Direct L1 | Road L1 | L2 |
|------|-------|---------|--------|---|----|------|
| B4 | (4,2) | (-2,-1) | (4,3) | 3 | 3 | 2.24 |
| D4 | (4,4) | (-2,1) | (4,3) | 3 | 3 | 2.24 |
| B3 | (3,2) | (-3,-1) | (3,3) | 4 | 4 | 3.16 |
| A6 | (6,1) | (0,-2) | (6,0) | 2 | 16 | 2.00 |

B4 and D4 tie on both road L1 and L2, so the first one in `slots.csv` wins:

best slot = argmin(road L1, then L2) = **B4**

For an EV at V = (0,2), only the EV slots A7, B7, E1 and E2 are candidates, and E1 (entered from (0,5)) has the smallest road L1 distance (4).

If the user clicks Don't Allocate, the recommended slot stays Available.
