import psycopg2 as ps
from utils import *


conn = ps.connect( 
    host = "localhost",
    dbname = "AUT_Samad",
    user   = "postgres",
    port   = 5432
)

cur = conn.cursor()
conn.autocommit = True


while True :
    
    print('select operation from below list')
    print('1. add student')
    print('2. remove student')
    print('3. update student balance')
    print('4. add food')
    print('5. remove food')
    print('6. reserve food')
    print('7. change reservation')

    op = int(input('enter operation number : '))

    if op == 1 :
        print('Enter information')
        id = str(input('id : '))
        student_id = str(input('student id : '))
        major = str(input('major : '))
        birthdate = str(input('birthdate : '))
        first_name = str(input('first name : '))
        last_name = str(input('last name : '))
        balance = int(input('balance : '))

        add_student(
            cur, 
            id,
            student_id,
            major,
            birthdate,
            first_name,
            last_name,
            balance
        )

        if not continu():
            break

    if op == 2 :
        print('Enter information')
        id = str(input('id : '))
 
        remove_student(
            cur, 
            id,
        )

        if not continu():
            break

    if op == 3 :
        print('Enter information')
        id = str(input('id : '))
        balance = int(input('balance : '))

        update_balance(
            cur,
            id,
            balance
        )
    
        if not continu():
            break

    if op == 4 :
        print('Enter information')
        id = str(input('id : '))
        date = str(input('date : '))
        name = str(input('name : '))
        price = int(input('price : '))
        inventory = int(input('inventory : '))

        add_food(
            cur,
            id,
            date,
            name,
            price,
            inventory
        )

        if not continu():
            break

    if op == 5 :
        print('Enter information')
        id = str(input('id : '))

        remove_food(
            cur,
            id
        )

        if not continu():
            break

    if op == 6 :
        print('Enter information')
        id = str(input('id : '))
        food_id = str(input('food id : '))

        reserve_food(
            cur,
            id,
            food_id
        )

        if not continu():
            break

    if op == 7 :
        print('Enter information')
        type = str(input('type of change: '))
        if type == 'cancel' :
            id = str(input('id of reservation to cancel : '))
            change_reservation(
                cur,
                type,
                id
            )

        if type == 'change' :
            id = str(input('id of reservation to change : '))
            food_id = str(input('food id to reserve: '))
            change_reservation(
                cur,
                type,
                id,
                food_id
            )

    if not continu():
        break