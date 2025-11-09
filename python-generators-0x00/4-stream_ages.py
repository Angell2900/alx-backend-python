import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    cursor.close()
    connection.close()

def calculate_average_age():
    total, count = 0, 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    calculate_average_age()
