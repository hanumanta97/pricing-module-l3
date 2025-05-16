# 🚕 Pricing Module - Django Based Assignment

## 📌 Objective

Design and build a web application with a **configurable pricing module** that supports **differential pricing**, using **Django Admin** as the UI.

---

## 📄 Description

The Pricing Module is intended to store and manage product/service pricing and calculate final invoices based on:

- Total ride time
- Distance traveled
- Waiting time
- Day of the week

> 💡 Think of this like a simplified billing system for services such as Uber/Ola.

---

## 🗃️ Models & Configurations

Pricing is broken down into the following components:

1. **Distance Base Price (DBP)**  
   Example:  
   - ₹80 up to 3 KMs (Tue, Wed, Thu)  
   - ₹90 up to 3.5 KMs (Sat, Mon)  
   - ₹95 up to 3.5 KMs (Sun)

2. **Distance Additional Price (DAP)**  
   Example:  
   - ₹30 per KM after 3 KMs  
   - ₹28 per KM after 3.5 KMs

3. **Time Multiplier Factor (TMF)**  
   Example:  
   - 1x under 1 hour  
   - 1.25x for 1–2 hours  
   - 2.2x for 2–3 hours

4. **Waiting Charges (WC)**  
   Example: ₹5 for every 3 minutes after initial 3 minutes

---

## 🧩 Features

- Admin interface to **create**, **update**, **enable/disable**, and **delete** pricing configurations.
- **Log table** to store configuration changes along with the **user** and **timestamp**.
- **Custom Django Form** with validation to manage pricing entries.
- REST API to calculate price dynamically.

---

## 🧮 Price Calculation Formula
-$Price = (DBP + (Dn * DAP)) + (Tn * TMF) + WC$) s
