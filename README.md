# Morning Moon Pocket Tools

🌐 **Website:** [xtools.daobuddy.xyz](https://xtools.daobuddy.xyz/)

---

## ภาษาไทย

> ข้อมูลชุมชนสำหรับเกม **Morning Moon Pocket** รวบรวมจากกิจกรรมของผู้เล่นจริง เพื่อประกอบการพัฒนาเว็บไซต์เครื่องมือ

### เกี่ยวกับโปรเจกต์

Repository นี้เป็นคลังข้อมูลแบบ Markdown ที่รวบรวมสถิติในเกม Morning Moon Pocket โดยผู้เล่น ข้อมูลเหล่านี้ถูกนำไปใช้ในการพัฒนาเครื่องมือช่วยเล่นเกมที่เว็บไซต์ [xtools.daobuddy.xyz](https://xtools.daobuddy.xyz/) ซึ่งรวมถึงข้อมูลมอนสเตอร์ ค่า HP ของทรัพยากรในเกม และอื่น ๆ อีกมาก

### ไฟล์ข้อมูล

| ไฟล์ | คำอธิบาย |
|---|---|
| [monster-data_4.md](monster-data_4.md) | ข้อมูลมอนสเตอร์: HP, ความเสียหาย, debuff, และ item drop |
| [resource_hp_data.md](resource_hp_data.md) | ค่า HP ของทรัพยากรในโลก (ต้นไม้ หิน ฯลฯ) คำนวณจากการสังเกตของผู้เล่น |

### วิธีมีส่วนร่วม

ผู้เล่นสามารถช่วยกันเพิ่มหรือแก้ไขข้อมูลได้โดย:

1. **Fork** repository นี้
2. แก้ไขไฟล์ Markdown ที่เกี่ยวข้อง โดยใช้ template ที่มีอยู่ในไฟล์นั้น ๆ
3. เปิด **Pull Request** พร้อมอธิบายข้อมูลที่เพิ่ม/แก้ไข

สำหรับข้อมูล Resource HP สามารถใช้ template นี้:

```markdown
| D (your damage) | A (hits needed) | HP range         |
|-----------------|-----------------|------------------|
| ?               | ?               | (A-1)×D+1 – A×D |
```

### รางวัลสำหรับผู้ร่วมสนับสนุน

ผู้ที่ส่งข้อมูลที่มีประโยชน์และได้รับการยอมรับ จะได้รับ **Grant Permission Farming หรือ Pro Subscription ฟรี** โดยระยะเวลาขึ้นอยู่กับดุลพินิจของเจ้าของโครงการ

### ลิขสิทธิ์

ข้อมูลทั้งหมดรวบรวมโดยชุมชนผู้เล่น Morning Moon Pocket และมีไว้เพื่อประโยชน์ของชุมชนเท่านั้น

---

## English

> Community-sourced data for **Morning Moon Pocket**, collected from real player activity to support tool website development.

### About

This repository is a community Markdown database of in-game statistics for Morning Moon Pocket. The data is used to power tools at [xtools.daobuddy.xyz](https://xtools.daobuddy.xyz/), including monster stats, resource HP values, and more.

### Data Files

| File | Description |
|---|---|
| [monster-data_4.md](monster-data_4.md) | Monster stats: HP, damage, debuffs, and item drops |
| [resource_hp_data.md](resource_hp_data.md) | Wild resource HP (trees, rocks, etc.) estimated from player observations |

### How to Contribute

Players can contribute by:

1. **Fork** this repository
2. Edit the relevant Markdown file using the template provided inside
3. Open a **Pull Request** describing what data you added or corrected

For Resource HP data, use this contribution template:

```markdown
| D (your damage) | A (hits needed) | HP range         |
|-----------------|-----------------|------------------|
| ?               | ?               | (A-1)×D+1 – A×D |
```

### Contributor Rewards

Contributors who submit useful and accepted data will receive a complimentary **Farming Permission Grant or Pro Subscription**. Duration is at the discretion of the project owner.

### License

All data is collected by the Morning Moon Pocket player community and is intended for community use only.
