import sqlite3


def connect_db():
    """اتصال بقاعدة البيانات"""
    conn = sqlite3.connect('user_settings.db')  # يمكنك تغيير اسم قاعدة البيانات هنا
    return conn

# دالة لجلب اللغة من قاعدة البيانات
def get_language(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM user_language WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return 'English'  # قيمة افتراضية إذا لم يكن هناك لغة مفضلة للمستخدم

# دالة لتحديث اللغة في قاعدة البيانات
def update_language(user_id, language):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO user_language (user_id, language)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET language=?
    ''', (user_id, language, language))
    conn.commit()
    conn.close()

# دالة لتتحقق من وجود user _id في قاعدة البيانات
def user_exists(user_id):
    """التحقق من وجود user_id في قاعدة البيانات"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_language WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None  # إذا كان يوجد نتيجة فهذا يعني أن الـ user_id موجود

#لاضافة user _id إلى قاعدة البيانات
def add_user(user_id, language):
    """إضافة user_id واللغة إذا لم يكونا موجودين"""
    if not user_exists(user_id):  # إذا لم يكن موجودًا
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_language (user_id, language) VALUES (?, ?)", (user_id, language))
        conn.commit()
        conn.close()
