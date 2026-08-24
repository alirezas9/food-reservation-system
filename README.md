# Food Reservation System

A basic simulation of a university food reservation system, built in Python on top of a **PostgreSQL** database. Students can be registered with a balance, food items can be listed for reservation, and students can reserve, cancel, or change their food reservations through a simple command-line menu.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)

## Overview

This is a small, from-scratch CLI application demonstrating CRUD operations and simple business logic (balance checks, inventory checks) against a PostgreSQL database using `psycopg2`, without an ORM. It was built as a university database-systems exercise (originally connecting to a database named `AUT_Samad`).

## Repository Structure

```
food-reservation-system/
├── create.py     # Creates the database tables (students, foods, reservations, transactions)
├── main.py       # Interactive CLI menu — the entry point of the application
├── utils.py      # All database operations: validation, add/remove/update/reserve logic
└── README.md
```

## Database Schema

`create.py` sets up four tables:

| Table | Columns | Purpose |
|---|---|---|
| `students` | `id` (PK), `studentID`, `major`, `birthdate`, `first_name`, `last_name`, `balance` | Registered students and their account balance. |
| `foods` | `id`, `date`, `name`, `price`, `inventory` | Food items available for reservation on a given date, with remaining inventory. |
| `reservations` | `id` (serial PK), `studentID`, `foodID` | Active reservations linking a student to a reserved food item. |
| `transactions` | `SRCID`, `DSTID`, `date` | A log of balance-affecting transactions (reservation, cancellation, change). |

## Installation

**Prerequisites:** Python 3, a running PostgreSQL server, and the `psycopg2` driver.

```bash
git clone https://github.com/alirezas9/food-reservation-system.git
cd food-reservation-system
pip install psycopg2-binary
```

Update the connection parameters (`host`, `dbname`, `user`, `port`) at the top of `create.py` and `main.py` to match your local PostgreSQL setup — by default they point to a local database named `AUT_Samad` with user `postgres`.

## Usage

1. Create the database tables:

```bash
python create.py
```

2. Run the interactive CLI:

```bash
python main.py
```

You'll be prompted to choose from a numbered list of operations, then enter the required fields for that operation:

```
select operation from below list
1. add student
2. remove student
3. update student balance
4. add food
5. remove food
6. reserve food
7. change reservation
```

After each operation the program asks `continue? (y/n)` to either loop back to the menu or exit.

## Features

- **Student management** — add a student (with validation on ID length, major, birthdate format, name length, and non-negative balance), remove a student, and update a student's balance.
- **Food management** — add a food item (with date, price, and inventory) and remove a food item.
- **Reservations** — reserve a food item for a student, which:
  - checks the student has sufficient balance and the food has inventory remaining,
  - deducts the price from the student's balance,
  - decrements the food's inventory,
  - records the reservation and logs a transaction.
- **Reservation changes** — `cancel` a reservation (refunds the student and restores inventory) or `change` a reservation (cancels the old one and reserves a new food item in its place).

### Validation rules (`isValid_student`)

- `id` and `studentID` must be strings of exactly 10 characters.
- `major` must be one of `CS`, `EE`, `ME`, `CE`.
- `birthdate` must be a `YYYY-MM-DD` formatted 10-character string.
- `first_name` / `last_name` must be strings up to 25 characters.
- `balance` must be a non-negative integer.

## License

No license file is currently included in this repository.
