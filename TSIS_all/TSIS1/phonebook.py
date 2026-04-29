import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    database="phonebook",
    user="postgres",
    password="0708"
)
cur = conn.cursor()


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING", (group,))
    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    gid = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO contacts(username,email,birthday,group_id) VALUES (%s,%s,%s,%s) RETURNING id",
        (name, email, birthday, gid)
    )
    cid = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones(contact_id,phone,type) VALUES (%s,%s,%s)",
        (cid, phone, ptype)
    )

    conn.commit()
    print("Added!")


def search():
    q = input("Search: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No results")


def filter_group():
    g = input("Group: ")
    cur.execute("""
        SELECT c.username, c.email, p.phone
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name = %s
    """, (g,))

    for row in cur.fetchall():
        print(row)


def sort_contacts():
    field = input("Sort by (name/birthday): ")

    if field == "name":
        order = "username"
    else:
        order = "birthday"

    cur.execute(f"SELECT username, email FROM contacts ORDER BY {order}")

    for row in cur.fetchall():
        print(row)


def pagination():
    limit = 3
    offset = 0

    while True:
        cur.execute(
            "SELECT username, email FROM contacts LIMIT %s OFFSET %s",
            (limit, offset)
        )

        rows = cur.fetchall()
        if not rows:
            print("No more data")
        else:
            for row in rows:
                print(row)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break
        else:
            print("Invalid command")


def export_json():
    cur.execute("""
        SELECT c.username, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    rows = cur.fetchall()

    result = []

    for r in rows:
        result.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]) if r[2] else None,
            "group": r[3],
            "phone": r[4],
            "type": r[5]
        })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("Exported!")

def import_json():
    with open("contacts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for row in data:
        name = row["name"]
        email = row["email"]
        birthday = row["birthday"]
        group = row["group"]
        phone = row["phone"]
        ptype = row["type"]

        if birthday == "birthday":
            continue  # защита от мусора

        cur.execute("SELECT id FROM contacts WHERE username=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE username=%s", (name,))

        cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING", (group,))
        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        gid = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts(username,email,birthday,group_id)
            VALUES (%s,%s,%s,%s)
            RETURNING id
        """, (name, email, birthday, gid))

        cid = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO phones(contact_id,phone,type)
            VALUES (%s,%s,%s)
        """, (cid, phone, ptype))

    conn.commit()
    print("Imported!")


def menu():
    print("""
1 Add contact
2 Search
3 Filter by group
4 Sort
5 Pagination
6 Export JSON
7 Import JSON
0 Exit
""")


# ОСНОВНОЙ ЦИКЛ (без ошибок!)
while True:
    menu()
    c = input("Choose: ")

    if c == "1":
        add_contact()
    elif c == "2":
        search()
    elif c == "3":
        filter_group()
    elif c == "4":
        sort_contacts()
    elif c == "5":
        pagination()
    elif c == "6":
        export_json()
    elif c == "7":
        import_json()
    elif c == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")


# ВАЖНО: закрытие после цикла
cur.close()
conn.close()