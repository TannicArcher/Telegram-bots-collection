import aiosqlite


# ========================USERS========================
async def add_user(user_id, ref=None):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO users (user_id, ref) VALUES(?,?)", (user_id, ref))
    await conn.commit()
    await conn.close()


async def check_user_id(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def update_bonus(user_id, value):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET bonus=? WHERE user_id=?", (value, user_id))
    await conn.commit()
    await conn.close()


async def select_all_users():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM users")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_all_refs(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM users WHERE ref=?", (user_id,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_user(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM users WHERE user_id=?", (user_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def update_bal(user_id, bal):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET balance= balance + ? WHERE user_id=?", (bal, user_id))
    await conn.commit()
    await conn.close()


async def update_ref_bal(user_id, bal):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET ref_bal= ref_bal + ? WHERE user_id=?", (bal, user_id))
    await conn.commit()
    await conn.close()


async def add_bought(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET bought=bought + 1 WHERE user_id=?", (user_id,))
    await conn.commit()
    await conn.close()


async def update_full_added_bal(user_id, bal):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET added_to_bal= added_to_bal + ? WHERE user_id=?", (bal, user_id))
    await conn.commit()
    await conn.close()


# ========================ORDERS========================
async def insert_order(user_id, item_name, count, url, order_id, payed, order_type):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO orders (user_id, item, count, url, order_id, payed, order_type)"
                       " VALUES(?,?,?,?,?,?,?)",
                       (user_id, item_name, count, url, order_id, payed, order_type))
    await conn.commit()
    await conn.close()


async def select_all_orders():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM orders")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_user_orders(user_id, order_type):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM orders WHERE user_id=? AND order_type=?", (user_id, order_type))
    h = await cursor.fetchall()
    await conn.close()
    return h


# ======================== STAT ========================
async def select_stat():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM stat")
    h = await cursor.fetchone()
    await conn.close()
    return h


async def add_smm_bought():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE stat SET smm_bought=smm_bought + 1")
    await conn.commit()
    await conn.close()


async def update_order_count():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE stat SET item_bought=item_bought + 1")
    await conn.commit()
    await conn.close()


async def add_wasted(wasted):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE stat SET all_wasted=all_wasted + ?", (wasted,))
    await conn.commit()
    await conn.close()


# ========================BUTTONS========================
# ITEMS
async def add_item(name, sub_category, category, cost, minimum, maximum, service_id, item_desc, item_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO smm_item_buttons "
                       "(name, sub_category, category, cost, min, max, service_id, item_desc, item_id)"
                       " VALUES(?,?,?,?,?,?,?,?,?)",
                       (name, sub_category, category, cost, minimum, maximum, service_id, item_desc, item_id))
    await conn.commit()
    await conn.close()


async def add_product_item(cat_id, sub_id, product, product_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO product_items "
                       "(cat_id, sub_id, product, product_id)"
                       " VALUES(?,?,?,?)",
                       (cat_id, sub_id, product, product_id))
    await conn.commit()
    await conn.close()


async def select_product_items(sub_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM product_items WHERE sub_id=?", (sub_id,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_product_item(product_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM product_items WHERE product_id=?", (product_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def del_product_item(product_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM product_items WHERE product_id=?", (product_id,))
    await conn.commit()
    await conn.close()


async def select_item(item_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM smm_item_buttons WHERE item_id=?", (item_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def select_items(sub_category):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM smm_item_buttons WHERE sub_category=?", (sub_category,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_all_items():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM smm_item_buttons")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def update_cost(item_id, cost):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE smm_item_buttons SET cost=? WHERE item_id=?", (cost, item_id,))
    await conn.commit()
    await conn.close()


async def update_item_name(item_id, name):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE smm_item_buttons SET name=? WHERE item_id=?", (name, item_id,))
    await conn.commit()
    await conn.close()


async def update_item_desc(item_id, desc):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE smm_item_buttons SET item_desc=? WHERE item_id=?", (desc, item_id,))
    await conn.commit()
    await conn.close()


async def update_service_id(item_id, service_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE smm_item_buttons SET service_id=? WHERE item_id=?", (service_id, item_id,))
    await conn.commit()
    await conn.close()


async def update_min(item_id, min_count):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE smm_item_buttons SET min=? WHERE item_id=?", (min_count, item_id,))
    await conn.commit()
    await conn.close()


async def update_max(item_id, max_count):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE smm_item_buttons SET max=? WHERE item_id=?", (max_count, item_id,))
    await conn.commit()
    await conn.close()


async def del_item(item_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM smm_item_buttons WHERE item_id=?", (item_id,))
    await conn.commit()
    await conn.close()


async def del_product(product_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM product_items WHERE product_id=?", (product_id,))
    await conn.commit()
    await conn.close()


async def del_item_from_category(category):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM smm_item_buttons WHERE category=?", (category,))
    await conn.commit()
    await conn.close()


async def del_product_from_category(cat_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM product_items WHERE cat_id=?", (cat_id,))
    await conn.commit()
    await conn.close()


async def del_item_from_sub_category(sub_category):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM smm_item_buttons WHERE sub_category=?", (sub_category,))
    await conn.commit()
    await conn.close()


async def del_product_from_subcategory(sub_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM product_items WHERE sub_id=?", (sub_id,))
    await conn.commit()
    await conn.close()


# SUB CATEGORY
async def add_subcategory(category, sub_id, name):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO smm_sub_category_buttons (category, sub_id, name) VALUES(?,?,?)",
                       (category, sub_id, name))
    await conn.commit()
    await conn.close()


async def update_sub_name_smm(sub_id, name):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE smm_sub_category_buttons SET name=? WHERE sub_id=?",
                       (name, sub_id))
    await conn.commit()
    await conn.close()


async def update_sub_name_product(sub_id, name):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE product_sub_categories SET name=? WHERE sub_id=?",
                       (name, sub_id))
    await conn.commit()
    await conn.close()


async def update_cost_product(sub_id, cost):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE product_sub_categories SET cost=? WHERE sub_id=?",
                       (cost, sub_id))
    await conn.commit()
    await conn.close()


async def update_sub_desc(sub_id, desc):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE product_sub_categories SET description=? WHERE sub_id=?",
                       (desc, sub_id))
    await conn.commit()
    await conn.close()


async def update_file_type(sub_id, item_type):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE product_sub_categories SET item_type=? WHERE sub_id=?",
                       (item_type, sub_id))
    await conn.commit()
    await conn.close()


async def add_product_subcategory(cat_id, sub_id, name, description, cost, item_type):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO product_sub_categories (cat_id, sub_id, name, description, cost, item_type) "
                       "VALUES(?,?,?,?,?,?)",
                       (cat_id, sub_id, name, description, cost, item_type))
    await conn.commit()
    await conn.close()


async def select_sub_category(sub_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM smm_sub_category_buttons WHERE sub_id=?", (sub_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def select_smm_subcategories(category):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM smm_sub_category_buttons WHERE category=?", (category,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_product_subcategory(sub_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM product_sub_categories WHERE sub_id=?", (sub_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def select_product_subcategories(cat_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM product_sub_categories WHERE cat_id=?", (cat_id,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def del_sub_category(sub_id):
    await del_item_from_sub_category(sub_id)
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM smm_sub_category_buttons WHERE sub_id=?", (sub_id,))
    await conn.commit()
    await conn.close()


async def del_product_subcategory(sub_id):
    await del_product_from_subcategory(sub_id)
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM product_sub_categories WHERE sub_id=?", (sub_id,))
    await conn.commit()
    await conn.close()


async def del_sub_from_category(category):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM smm_sub_category_buttons WHERE category=?", (category,))
    await conn.commit()
    await conn.close()


async def del_product_sub_from_category(cat_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM product_sub_categories WHERE cat_id=?", (cat_id,))
    await conn.commit()
    await conn.close()


# CATEGORY
async def add_category(name, cat_id, category_type):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO category_buttons (name, cat_id, type) VALUES(?,?,?)",
                       (name, cat_id, category_type))
    await conn.commit()
    await conn.close()


async def update_category_name(cat_id, name):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE category_buttons SET name=? WHERE cat_id=?",
                       (name, cat_id))
    await conn.commit()
    await conn.close()


async def select_categories(category_type):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM category_buttons WHERE type=?", (category_type,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_category(cat_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM category_buttons WHERE cat_id=?", (cat_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def del_category(cat_id, cat_type):
    if cat_type == "smm":
        await del_item_from_category(cat_id)
        await del_sub_from_category(cat_id)
    else:
        await del_product_from_category(cat_id)
        await del_product_sub_from_category(cat_id)
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM category_buttons WHERE cat_id=?", (cat_id,))
    await conn.commit()
    await conn.close()


async def select_settings():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM settings")
    h = await cursor.fetchone()
    await conn.close()
    return h


async def update_qiwi_secret(qiwi_secret):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE settings SET qiwi_secret=?", (qiwi_secret,))
    await conn.commit()
    await conn.close()


async def update_settings_num(new):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE settings SET qiwi_num=?", (new,))
    await conn.commit()
    await conn.close()


async def update_settings_log_channel(new):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE settings SET log_channel=?", (new,))
    await conn.commit()
    await conn.close()


async def update_settings_token(new):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE settings SET qiwi_token=?", (new,))
    await conn.commit()
    await conn.close()


async def update_settings_p2p(new):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE settings SET qiwi_key=?", (new,))
    await conn.commit()
    await conn.close()


# SUPPORT MAILS
async def add_mail(user_id, mail_type, text):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO support_mails (user_id, mail_type, text)"
                       " VALUES(?,?,?)",
                       (user_id, mail_type, text))
    await conn.commit()
    await conn.close()


async def select_mail(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM support_mails WHERE user_id=?", (user_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def select_all_mails():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute("SELECT * FROM support_mails")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def del_mail(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM support_mails WHERE user_id=?",
                       (user_id,))
    await conn.commit()
    await conn.close()
