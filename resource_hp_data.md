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

| Stat name in game    | Field    |
|----------------------|----------|
| Wood Chopping Damage | Chopping |
| Mineral Mining Damage | Mining  |
| Rock Breaking Damage | Breaking |
| — (no stat)          | Cutting  |

---

## Contribution template

Copy this block for each new observation:

```markdown
| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| ?               | ?               | (A-1)×D+1 – A×D |
```

---

## Resources

---

### Red Apple
- **Type:** Free drop — no action required, no HP

---

### Small Rock
- **Type:** Cutting

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5 | 1 | 1 – 5 |

**Estimated HP:** 1–5

---

### Log
- **Type:** Chopping

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5 | 1 | 1 – 5 |

**Estimated HP:** 1–5

---

### Primrose / Grass / Tulip / Red Herb
- **Type:** Cutting

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5 | 1 | 1 – 5 |

**Estimated HP:** 1–5

---

### Pine Cone
- **Type:** Breaking

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5 | 2 | 6 – 10 |

**Estimated HP:** 6–10


---

### Stump
- **Type:** Chopping
- **Reward:** 3 Wood

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5 | 3 | 11 – 15 |
| 6 | 3 | 12 – 15 |
| 12 | 2 | 13 – 24 |

**Estimated HP:** 13–24

---

### Rock
- **Type:** Breaking
- **Reward:** 3 Stone

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 6 | 3 | 13 – 18 |

**Estimated HP:** 13–18

---

### Large Rock
- **Type:** Breaking
- **Reward:** 12 Stone

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5               | 12              | 56 – 60  |
| 12              | 5               | 49 – 60  |

**Estimated HP:** 56–60 _(intersection of all ranges)_

---

### Beehive
- **Type:** Breaking
- **Reward:** 1 Honeycomb

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 6 | 2 | 7 – 12 |

**Estimated HP:** 7–12

---

### Beehive Tree
- **Type:** Chopping
- **Reward:** 9 Wood

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 12 | 2 | 13 – 24 |

**Estimated HP:** 13–24

---

### Red Apple Tree / Round Tree
- **Type:** Chopping
- **Reward:** 9 Wood

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
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
|-----------------|-----------------|----------|
| 5  | 12 | 56 – 60 |
| 6  | 10 | 56 – 60 |
| 10 | 6  | 51 – 60 |
| 12 | 5  | 49 – 60 |

**Estimated HP:** 56–60 _(intersection of all ranges)_

---

### Copper Ore
- **Type:** Mining
- **Reward:** 9 Copper

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5               | 6               | 26 – 30  |

**Estimated HP:** 26–30
