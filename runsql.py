import sqlite3

# الاتصال بقاعدة البيانات أو إنشائها إذا كانت غير موجودة
conn = sqlite3.connect('user_settings.db')
cursor = conn.cursor()

# إنشاء جدول لتخزين إعدادات اللغة
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_language (
    user_id INTEGER PRIMARY KEY,
    language TEXT
)
''')

# حفظ التغييرات وإغلاق الاتصال
conn.commit()
conn.close()
