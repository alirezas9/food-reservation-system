from datetime import datetime


def isValid_student(
        id,
        student_id,
        major,
        birthdate,
        first_name,
        last_name,
        balance
):
    majors = ['CS', 'EE', 'ME', 'CE']
    valid = True

    if not isinstance(id, str) or len(id) != 10:
        valid = False

    if not isinstance(student_id, str) or len(student_id) != 10:
        valid = False

    if not isinstance(major, str) or major not in majors:
        valid = False

    if not isinstance(birthdate, str) or len(birthdate) != 10:
        valid = False
    y, m, d = birthdate.split('-')
    if len(y) != 4 or len(m) != 2 or len(d) != 2:
        valid = False

    if not isinstance(first_name, str) or len(first_name) > 25:
        valid = False

    if not isinstance(last_name, str) or len(last_name) > 25:
        valid = False

    if not isinstance(balance, int) or balance < 0:
        valid = False

    return valid

def add_student(
        cur,
        id,
        student_id,
        major,
        birthdate,
        first_name,
        last_name,
        balance
):    
    if isValid_student(
            id,
            student_id,
            major,
            birthdate,
            first_name,
            last_name,
            balance) :
        
        cur.execute(
            """
            -- beginsql
            insert into students values (
            %s, %s, %s,%s, %s, %s, %s)
            -- endsql
            """,
            (id,
            student_id,
            major,
            birthdate,
            first_name,
            last_name,
            balance)
        ) 
    else:
        print('Invalid information')

def remove_student(
        cur,
        id) :
    
    cur.execute(
        """
        -- beginsql
        delete from students 
        where id = %s 
        -- endsql
        """,
        (id,)
    )

def update_balance(
        
        cur,
        id,
        balance) :

    if balance < 0 :
        assert False, "balance cannot be negative"
    else:
        cur.execute(
            """
            -- beginsql
            update students
            set balance = %s
            where id = %s 
            -- endsql
            """,
            (balance, id)
        )

def add_food(
        cur,
        id,
        date,
        name,
        price,
        inventory
):
    cur.execute(
        """
        -- beginsql
        insert into foods values (
        %s, %s, %s, %s, %s)
        -- endsql
        """,
        (
        id,
        date,
        name,
        price,
        inventory
        )
    )

def remove_food(
        cur,
        id
):
    cur.execute(
        """
        -- beginsql
        delete from foods
        where id = %s 
        -- endsql
        """,
        (id,)
    )

def reserve_food(
        cur,
        id,
        foodID
):
    cur.execute(
        """
        -- beginsql
            select balance 
            from students
            where id = %s 
        -- endsql
        """,
        (id,)
    )

    student_balance = cur.fetchall()[0][0]

    cur.execute(
        """
        -- beginsql
            select price, inventory
            from foods
            where id = %s
        -- endsql
        """,
        (foodID,)
    )
    temp = cur.fetchall()[0]
    food_price = temp[0]
    inventory  = temp[1]

    if food_price > student_balance:
        assert False, "student balance is not enough"
    elif inventory == 0:
        assert False, "food inventory is 0"
    else :
        update_balance(cur, id, student_balance - food_price)
        cur.execute(
            """
            -- beginsql
            update foods
            set inventory = inventory - 1
            where id = %s 
            -- endsql
            """,
            (foodID,)
        )
        cur.execute(
            """
            -- beginsql
            insert into reservations(studentID, foodID) values (
            %s, %s)
            -- endsql
            """,
            (
            id,
            foodID)
        )

        cur.execute(
            """
            -- beginsql
            insert into transactions values (
            %s,
            %s,
            %s
            )
            -- endsql
            """,
            (id,'',datetime.now().strftime("%Y-%m-%d"))
        )

def change_reservation(
        cur,
        type,
        id,
        dst_id = None
):

    if type == 'cancel':
        cur.execute(
            """
            -- beginsql
            select foodID, studentID
            from reservations
            where ID = %s
            -- endsql
            """,
            (id,)
        )
        temp = cur.fetchall()[0]
        food_id = temp[0]
        studentID = temp[1]

        cur.execute(
            """
            -- beginsql
            delete from reservations
            where id = %s
            -- endsql
            """,
            (id,)
        )

        cur.execute(
            """
            -- beginsql
            select price 
            from foods 
            where ID = %s
            -- endsql
            """,
            (food_id, )
        )
        food_price = cur.fetchall()[0][0]
        cur.execute(
            """
            -- beginsql
            select balance
            from students
            where ID = %s
            -- endsql
            """,
            (studentID,)
        )
        balance = cur.fetchall()[0][0]
        update_balance(cur, studentID, balance + food_price)
        cur.execute(
            """
            -- beginsql
            update foods
            set inventory = inventory + 1
            where ID = %s
            -- endsql
            """,
            (food_id,)
        )
        cur.execute(
            """
            -- beginsql
            insert into transactions values (
            %s,
            %s,
            %s
            )
            -- endsql
            """,
            (id, '', datetime.now().strftime("%Y-%m-%d"))
        )

    if type == 'change':
        cur.execute(
            """
            -- beginsql
            select studentID
            from reservations
            where ID = %s
            -- endsql
            """,
            (id,)
        )
        studentID = cur.fetchall()[0][0]
        change_reservation(cur, 'cancel', id)
        reserve_food(cur, studentID, dst_id)


def continu():
    return input('continue? (y/n) : ') == 'y'