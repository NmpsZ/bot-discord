### Pokémon Bot

บอทนี้พัฒนาด้วยภาษา Python โดยใช้ไลบรารี `discord.py` และดึงข้อมูลโปเกม่อนจาก **PokeAPI** เพื่อให้ข้อมูลต่างๆ เกี่ยวกับโปเกม่อน

---

### คุณสมบัติของบอท

1. **สุ่มโปเกม่อน**:  
   - บอทสุ่มโปเกม่อนและส่งข้อความในช่องที่กำหนดพร้อมรายละเอียดต่างๆ เช่น ประเภท, ความสามารถ, น้ำหนัก, และความสูงของโปเกม่อนนั้น
2. **จับโปเกม่อน**:  
   - ผู้ใช้สามารถจับโปเกม่อนที่สุ่มมาและเพิ่มลงใน inventory ของตัวเองได้
3. **ทายโปเกม่อน**:  
   - ผู้ใช้สามารถทายชื่อของโปเกม่อนที่สุ่มขึ้นมา โดยมีการให้คำใบ้
4. **อินเวนทอรี่ของผู้ใช้**:  
   - ผู้ใช้สามารถดูโปเกม่อนที่จับได้ใน inventory ของตัวเอง
5. **ข้อความต้อนรับและลาก่อน**:  
   - บอทจะส่งข้อความต้อนรับเมื่อมีผู้เข้าร่วมเซิร์ฟเวอร์ และส่งข้อความลาก่อนเมื่อมีผู้ออกจากเซิร์ฟเวอร์

---

### คำสั่งของบอท
   -/hellobot: บอทจะทักทายผู้ใช้
   -/ambraton_check: ตรวจสอบว่าผู้ใช้เป็นมนุษย์หรือบอท
   -/help: แสดงรายการคำสั่งของบอท
   -/pokémon_check <name>: ค้นหารายละเอียดของโปเกม่อนโดยใช้ชื่อ
   -/inventory: แสดงอินเวนทอรี่ของโปเกม่อนของผู้ใช้
