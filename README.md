# 🚗 Smart Parking Allocation System

> Mini project for **UE25MA242A** — Mathematical Foundation for AI & Data Science (MFAD)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Mathematical Concepts](#-mathematical-concepts)
- [Practical Application](#-practical-application)
- [Workflow](#-workflow)
- [Project Structure](#-project-structure)
- [Grid Layout](#-grid-layout)
- [Installation](#-installation)
- [Running the App](#-running-the-app)
- [Example](#-example)
- [Contributing](#-contributing)

---

## 🚨 Problem Statement

Finding a suitable parking slot manually can be inefficient when multiple slots are available. This system uses **vector-based distance calculations** to automatically select the nearest suitable slot for any vehicle type.

---

## 📐 Mathematical Concepts

### Vectors
The vehicle is $V = (x_v, y_v)$ and each parking slot is $S_i = (x_i, y_i)$.  
The relative vector from vehicle to slot is:

$$d_i = S_i - V = (x_i - x_v,\ y_i - y_v)$$

### L1 Norm — Manhattan Distance
$$\|d\|_1 = |d_x| + |d_y|$$

Models movement along the lanes of a parking grid. A car cannot drive through slots, so the trip is a sequence of straight road legs. The total trip length is the sum of the L1 norms of each leg (road L1 distance).

### L2 Norm — Euclidean Distance
$$\|d\|_2 = \sqrt{d_x^2 + d_y^2}$$

Straight-line distance used as a **tie-breaker** when multiple slots share the same road L1 distance.

### Argmin
$$s^* = \arg\min_i D_i$$

Selects the slot with the **smallest road L1 distance** $D_i$.  
Tie-break: smallest $\|S_i - V\|_2$.  
Tie-break again: first entry in `slots.csv`.

---

## 🧠 Practical Application

1. **Vectors** turn positions into coordinates so the offset to every slot can be computed.
2. The **L1 norm** of each road leg gives the driving distance to the slot's entry cell — the allocation metric. The road is column 0 and rows 0, 3, and 6; a leg never crosses a slot.
3. The **L2 norm** gives the straight-line distance (tie-break and display).
4. **Argmin** picks the single best slot from the candidates. The slot is only *recommended*; it becomes **Occupied** when the user clicks **Allocate**.

> **Compatibility rules:** A *Standard* vehicle uses Standard slots; an *EV* vehicle uses EV slots. Only available, compatible slots are candidates.

---

## 🔄 Workflow

```
Vehicle position
    → compute vectors (S_i − V)
    → compute L1 norms (road distance per leg)
    → distance comparison
    → argmin
    → recommended slot highlighted
    → user clicks [Allocate] or [Don't Allocate]
```

---

## 📁 Project Structure

```
Parking-Allocation/
├── app.py              # Flask app — single page, routes
├── parking.py          # Slots, compatibility, candidates, best slot, allocate, reset
├── linalg.py           # Vector subtraction, L1 norm, L2 norm, argmin
├── slots.csv           # 28 slots: ID, x, y, type, status (all start Available)
├── templates/
│   └── index.html      # Single-page UI (grid, controls, calculations panel)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🗺️ Grid Layout

Slot IDs use **row letter + column number**. `x` is the column (1–7, left to right) and `y` is the row (`A=1`, `B=2`, `D=4`, `E=5`, top to bottom). So `B3 = (3, 2)`.

```
     col 0  col 1  col 2  col 3  col 4  col 5  col 6  col 7
row 0  ROAD  ──────────────────────────────────────────────
row 1        A1     A2     A3     A4     A5     A6     A7
row 2        B1     B2     B3     B4     B5     B6     B7
row 3  ROAD  ──────────────────────────────────────────────
row 4        D1     D2     D3     D4     D5     D6     D7
row 5        E1     E2     E3     E4     E5     E6     E7
row 6  ROAD  ──────────────────────────────────────────────
```

- **Column 0** and **rows 0, 3, 6** are roads — no parking slots exist there.
- Every slot touches a road.
- **Vehicle position** is set by clicking a road cell → sets $V = (x, y)$ shown above the grid.

After clicking **Find Best Slot**, the recommended slot is highlighted and the Calculations section shows:
- Candidate table with distances
- Leg-by-leg route to the recommended slot
- (When relevant) the slot nearest in straight line but not directly reachable

---

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/HARIKRISHNA1321/Parking-Allocation.git
cd Parking-Allocation

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.  
**No internet connection required.**

---

## 💡 Example

All slots start **Available**. Vehicle type = *Standard*, $V = (6, 3)$ (click the road at row 3, column 6). Assume B5, B6, D5, D6, D7 are already occupied.

`A6 = (6,1)` is only $|0| + |-2| = 2$ away by direct L1, but the car cannot drive through B6. It must take the road: $(6,3) \to (0,3) \to (0,0) \to (6,0)$ — that is $6 + 3 + 6 = 15$, plus 1 step into the slot, giving a **road L1 distance of 16**.

`B4 = (4,2)` is entered from road cell `(4,3)` — 2 steps away + 1 into the slot:

| Slot | S      | S − V    | Entry cell | Direct L1 | Road L1 | L2   |
|------|--------|----------|------------|-----------|---------|------|
| B4   | (4, 2) | (−2, −1) | (4, 3)     | 3         | **3**   | 2.24 |
| D4   | (4, 4) | (−2,  1) | (4, 3)     | 3         | **3**   | 2.24 |
| B3   | (3, 2) | (−3, −1) | (3, 3)     | 4         | 4       | 3.16 |
| A6   | (6, 1) | ( 0, −2) | (6, 0)     | 2         | 16      | 2.00 |

B4 and D4 tie on both road L1 and L2 → first in `slots.csv` wins:

> **best slot = argmin(road L1, then L2) = B4** ✅

For an EV at $V = (0, 2)$, only EV slots A7, B7, E1, E2 are candidates.  
E1 (entered from `(0,5)`) has the smallest road L1 distance of **4**.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/Parking-Allocation.git
   ```
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "feat: describe your change"
   ```
5. **Push** to your fork and open a **Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

### 💡 Ideas for Contributions
- Add more vehicle/slot types (e.g., Handicap, Motorcycle)
- Add a real-time slot status refresh (WebSocket or polling)
- Improve the UI with better styling or animations
- Add unit tests for `linalg.py` and `parking.py`
- Support persistent storage (SQLite) instead of in-memory state
- Add a REST API layer for mobile app integration

---

*Built with ❤️ using Python & Flask*
