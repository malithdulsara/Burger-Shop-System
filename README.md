# 🍔 iHungry Burger Shop Management System

A robust, console-based Point of Sale (POS) system designed for a Burger Shop. This system efficiently manages customer orders, tracks sales, and identifies top-performing customers on a monthly basis.

## 🚀 Key Features

* **Secure Authentication:** Access restricted to authorized personnel using masked password entry.
* **Order Management:** Seamless process to place, search, and view orders by status (Preparing, Delivered, Cancelled).
* **Dynamic Updates:** Ability to modify order quantities and statuses in real-time.
* **Monthly Analytics:** Automatically identifies the 'Best Customer' based on delivered orders for the current month.
* **Persistent Storage:** Data is securely saved to and loaded from a local text file database (`orders.txt`).
* **Colorful Interface:** Professional terminal UI using Colorama for better user experience.

## 🛠️ Built With

* **Python 3.x**
* **Colorama** - For terminal styling and colors.
* **Maskpass** - For secure password handling.

## 📦 How to Run

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install colorama maskpass
3. Run Application
   ```bash
   python Burger_Shop.py
