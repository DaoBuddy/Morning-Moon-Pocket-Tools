# Wild Resource Data

Goal: find the **real HP** of each resource by collecting observations.

## How HP is calculated

Each observation gives a HP range:

```
If damage = D and you need A hits to harvest:
  HP range = [ (A-1)×D + 1  ,  A×D ]
```

The more observations with different damage values, the narrower the intersection → real HP.

**Energy cost:** 1 Action = 4 Energy

| Stat name in game     | Field    |
| --------------------- | -------- |
| Wood Chopping Damage  | Chopping |
| Mineral Mining Damage | Mining   |
| Rock Breaking Damage  | Breaking |
| — (no stat)           | Cutting  |

---

## Contribution template

Copy this block for each new observation:

```markdown
| D (your damage) | A (hits needed) | HP range        |
| --------------- | --------------- | --------------- |
| ?               | ?               | (A-1)×D+1 – A×D |
```

---

## Resources

---

### Red Apple
- **Type:** Free drop — no action required, no HP
- **Reward:** 1 Red Apple

---

### Small Rock
- **Type:** Breaking
- **Reward:** 1 Rock

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 1               | ≤5       |

**Estimated HP:** ≤5

---

### Log
- **Type:** Chopping
- **Reward:** 1 Wood

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 1               | ≤5       |

**Estimated HP:** ≤5

---

### King Trumpet Mushroom
- **Type:** Cutting
- **Reward:** 1 King Trumpet Mushroom

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 1               | ≤5       |

**Estimated HP:** ≤5

---

### Primrose / Grass / Tulip / Red Herb / Green Herb
- **Type:** Cutting
- **Reward:** 1 Primrose / Grass / Tulip / Red Herb / Green Herb

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 1               | ≤5       |

**Estimated HP:** ≤5

---

### Shiitake Mushroom
- **Type:** Cutting
- **Reward:** 1 Shiitake Mushroom

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 1               | ≤5       |

**Estimated HP:** ≤5

---

### White Button Mushroom
- **Type:** Cutting

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 1               | ≤5       |

**Estimated HP:** ≤5

---

### Pine Cone
- **Type:** Breaking
- **Reward:** 1 Pine Cone

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 2               | 6 – 10   |
| 12              | 1               | 1 – 12   |

**Estimated HP:** 6–10 _(intersection of all ranges)_

---

### Stump
- **Type:** Chopping
- **Reward:** 3 Wood

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 3               | 11 – 15  |
| 6               | 3               | 12 – 15  |
| 12              | 2               | 13 – 24  |

**Estimated HP:** 13–24

---

### Rock
- **Type:** Breaking
- **Reward:** 3 Stone

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 6               | 3               | 13 – 18  |
| 12              | 2               | 13 – 24  |

**Estimated HP:** 13–18 _(intersection of all ranges)_

---

### Large Rock
- **Type:** Breaking
- **Reward:** 12 Stone

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 12              | 56 – 60  |
| 12              | 5               | 49 – 60  |

**Estimated HP:** 56–60 _(intersection of all ranges)_

---

### Barrel
- **Type:** Breaking
- **Reward:** 1 Red Apple

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 12              | 3               | 25 – 36  |

**Estimated HP:** 25–36

---

### Beehive
- **Type:** Breaking
- **Reward:** 1 Honeycomb

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 6               | 2               | 7 – 12   |
| 14              | 1               | 1 – 14   |

**Estimated HP:** 7–12 _(intersection of all ranges)_

---

### Beehive Tree
- **Type:** Chopping
- **Reward:** 9 Wood

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 12              | 2               | 13 – 24  |

**Estimated HP:** 13–24

---

### Red Apple Tree / Round Tree
- **Type:** Chopping
- **Reward:** 9 Wood

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 12              | 4               | 37 – 48  |
| 5               | 9               | 41 – 45  |
| 6               | 8               | 43 – 48  |
| 10              | 5               | 41 – 50  |

**Estimated HP:** 43–45 _(intersection of all ranges)_

---

### Pine Tree
- **Type:** Chopping
- **Reward:** 12 Wood

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 12              | 56 – 60  |
| 6               | 10              | 56 – 60  |
| 10              | 6               | 51 – 60  |
| 12              | 5               | 49 – 60  |

**Estimated HP:** 56–60 _(intersection of all ranges)_

---

### Copper Ore (small)
- **Type:** Mining
- **Reward:** 3 Copper

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 2               | 6 - 10   |
| 19              | 1               | 1 – 19   |

**Estimated HP:** 6-10


---

### Copper Ore
- **Type:** Mining
- **Reward:** 9 Copper

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 5               | 6               | 26 – 30  |
| 19              | 2               | 20 – 38  |

**Estimated HP:** 26–30 _(intersection of all ranges)_

---

### Silver Ore (small)
- **Type:** Mining
- **Reward:** 3 Silver

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 19              | 2               | 20 – 38  |

**Estimated HP:** 20–38

---

### Silver Ore
- **Type:** Mining
- **Reward:** 9 Silver

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 19              | 6               | 96 – 114 |

**Estimated HP:** 96–114

---


### Metal Wood Crate
- **Type:** Breaking
- **Reward:** 7 Stone, 7 Wood, 10 Grass, 1 Red Apple

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 12              | 1               | 1 – 12   |

**Estimated HP:** 1–12

---

### Wood Crate
- **Type:** Breaking
- **Reward:** 3 Stone, 3 Wood, 5 Grass, 1 Red Apple

| D (your damage) | A (hits needed) | HP range |
| --------------- | --------------- | -------- |
| 12              | 1               | 1 – 12   |
| 5               | 2               | 6 – 10   |

**Estimated HP:** 6–10 _(intersection of all ranges)_

---

### Chest
- **Type:** Free drop — no action required, no HP
- **Reward:** 10 Wood, 10 Stone, Forest Loot Box (2%), 1 Banana

---
