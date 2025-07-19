import mysql.connector

from english_website.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# اتصال به پایگاه داده
mydb = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# تابع برای وارد کردن متن (پاساژ)
def insert_reading_passage(title, content):
    cursor = mydb.cursor()
    try:
        # کوئری برای وارد کردن متن (پاساژ)
        insert_query = "INSERT INTO reading_passage (title, content) VALUES (%s, %s)"
        values = (title, content)
        
        cursor.execute(insert_query, values)
        mydb.commit()  # اعمال تغییرات در پایگاه داده
        print("Passage added successfully.")
        
        # برگرداندن شناسه Passage جدید
        return cursor.lastrowid
    except Exception as e:
        print(f"The error '{e}' occurred while adding passage.")
        return None
    finally:
        cursor.close()

# تابع برای وارد کردن سوالات
def insert_reading_question(passage_id, question_text, options, correct_option, question_type):
    cursor = mydb.cursor()
    try:
        # کوئری برای وارد کردن سوال
        insert_query = """
        INSERT INTO reading_question (passage_id, question_text, option_1, option_2, option_3, option_4, correct_option, question_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (passage_id, question_text, options[0], options[1], options[2], options[3], correct_option, question_type)
        
        cursor.execute(insert_query, values)
        mydb.commit()  # اعمال تغییرات در پایگاه داده
        print("Question added successfully.")
        
    except Exception as e:
        print(f"The error '{e}' occurred while adding question.")
    finally:
        cursor.close()

# تابع برای دریافت متن چندخطی (پاساژ)
def get_passage_content():
    content = ""
    print("Enter your passage content (Type 'END' when you are done):")
    while True:
        line = input()
        if line.strip().lower() == 'end':  # اگر کاربر 'END' وارد کرد، وارد کردن متن تمام می‌شود
            break
        content += line + "\n"  # اضافه کردن هر خط به محتوای کل
    return content

# تابع اصلی برای وارد کردن داده‌ها
def add_reading_data():
    # وارد کردن متن (پاساژ)
    title = input("Enter the title of the passage: ")
    content = get_passage_content()  # فراخوانی تابع برای دریافت محتوای چندخطی
    
    passage_id = insert_reading_passage(title, content)
    
    if passage_id:
        # وارد کردن سوالات
        while True:
            try:
                num_questions = int(input("How many questions do you want to add? "))
                if num_questions > 0:
                    break  # اگر عدد معتبر وارد شد، حلقه متوقف می‌شود
                else:
                    print("Please enter a number greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        for i in range(num_questions):
            print(f"Enter details for Question {i+1}:")
            question_text = input("Enter the question text: ")
            options = []
            for i in range(4):
                options.append(input(f"Enter option {i+1}: "))
            correct_option = int(input("Enter the correct option number (1-4): "))
            question_type = input("Enter the question type (multiple_choice / true_false): ")

            insert_reading_question(
                passage_id,
                question_text,
                options,
                correct_option,
                question_type
            )
    else:
        print("Failed to add passage.")

# فراخوانی تابع برای اضافه کردن داده‌ها
add_reading_data()

# بستن اتصال به پایگاه داده
mydb.close()
