import psycopg2 as ps


conn = ps.connect( 
    host = "localhost",
    dbname = "AUT_Samad",
    user   = "postgres",
    port   = 5432
)

cur = conn.cursor()
conn.autocommit = True

cur.execute(
    """
    -- beginsql
    create table if not exists students(
    id         varchar(10) primary key,
    studentID  varchar(10),
    major      varchar(20),
    birthdate  varchar(10),
    first_name varchar(25),
    last_name  varchar(25),
    balance    int 
    )
    -- endsql

"""
)

cur.execute(
    """
    -- beginsql
    create table if not exists foods(
    id        varchar(10),
    date      varchar(10),
    name      varchar(25),
    price     int,
    inventory int
    )
    -- endsql

"""
)

cur.execute(
    """
    -- beginsql
    create table if not exists reservations(
    id             serial primary key,
    studentID      varchar(10),
    foodID         varchar(10)
    )
    -- endsql

"""
)

cur.execute(
    """
    -- beginsql
    create table if not exists transactions(
    SRCID      varchar(10),
    DSTID      varchar(10),
    date       varchar(10)
    )
    -- endsql

"""
)

cur.close()
conn.close()
