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

| Stat name in game | Field |
|-------------------|-------|
| Wood Chopping Damage | Chopping |
| Mineral Mining Damage | Breaking |
| — (no stat) | Cutting |

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

### Primrose / Grass / Tulip
- **Type:** Cutting

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 5 | 1 | 1 – 5 |

**Estimated HP:** 1–5

---

### Stump
- **Type:** Chopping
- **Reward:** 3 Wood

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 12 | 2 | 13 – 24 |

**Estimated HP:** 13–24

---

### Rock
- **Type:** Breaking
- **Reward:** 3 Rock

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 6 | 3 | 13 – 18 |

**Estimated HP:** 13–18

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

### Red Apple Tree
- **Type:** Chopping
- **Reward:** 9 Wood

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 12 | 4 | 37 – 48 |
| 5  | 9 | 41 – 45 |

**Estimated HP:** 41–45 _(intersection of both ranges)_

---

### Pine Tree
- **Type:** Chopping
- **Reward:** 12 Wood

| D (your damage) | A (hits needed) | HP range |
|-----------------|-----------------|----------|
| 12 | 5 | 49 – 60 |
| 5  | 12 | 56 – 60 |

**Estimated HP:** 56–60 _(intersection of both ranges)_
