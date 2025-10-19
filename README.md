# Sports_Kit_Management_Dashboard



# 🏏 Sports Kits Management Dashboard

A simple and efficient **Sports Kits Management System** built using **Streamlit** and **SQLite** to manage sports equipment inventory, issue/return logs, and analytics.

---

## 🚀 Features

✅ **Add Kits** – Add new sports kits and track their total quantity.  
✅ **Issue Kits** – Issue kits to users while automatically updating availability.  
✅ **Return Kits** – Record returns and handle conditions (good, worn-out, or lost).  
✅ **Track Transactions** – Maintain a detailed history of all kit movements.  
✅ **Data Visualization** – Get a quick overview of inventory through bar charts.  
✅ **Fine Calculation** – Automatically calculate fines for lost or worn-out kits.

---

## 🧩 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** SQLite  
- **Data Handling:** Pandas  
- **Visualization:** Matplotlib  

---

## 🗂️ Database Schema

### Table: `kits`
| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary Key |
| name | TEXT | Kit name |
| total | INT | Total quantity |
| available | INT | Currently available |
| lost | INT | Lost count |
| wornout | INT | Worn-out count |

### Table: `transactions`
| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary Key |
| user | TEXT | User name |
| kit_name | TEXT | Name of kit |
| action | TEXT | Issued/Returned |
| fine | INT | Fine amount |
| date | TIMESTAMP | Auto-generated timestamp |

---
                                    

Team:
N Sai Venkata Pavan
K Yagna Sri Keerthi
