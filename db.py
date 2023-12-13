import sqlite3
import openai

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, username, first_name, last_name):
        self.cursor.execute("INSERT INTO `users` (`user_id`, `username`, `first_name`, `last_name`) VALUES (?,?,?,?)", (user_id,username,first_name,last_name))
        return self.conn.commit()
    
    def add_exercise(self, user_id, exercise_name, exercise_muscle, exercise_level, exercise_repetition):
        self.cursor.execute("INSERT INTO `exercises` (`user_id`, `exercise_name`, `exercise_muscle`, `exercise_level`, `exercise_repetition`) VALUES (?, ?, ?, ?, ?)",
            (user_id,
            exercise_name,
            exercise_muscle,
            exercise_level,
            exercise_repetition))
        return self.conn.commit()

    def get_exercises(self, user_id):
        result = self.cursor.execute("SELECT id, exercise_name, exercise_muscle, exercise_level, exercise_repetition FROM `exercises` WHERE `user_id` = ?", (user_id,))
        fetchall = result.fetchall()
        final_array = []

        for idx, (id, exercise_name, exercise_repetition, exercise_muscle, exercise_level) in enumerate(fetchall, start=1):
            exercise_repetition = int(exercise_repetition)

            formatted_item = f"<b>{idx}.</b> Exercise ID: {id}, Exercise Name: {exercise_name}, Exercise Muscle: {exercise_muscle}, Exercise level: {exercise_level}, Exercise repetition: {exercise_repetition}"
            final_array.append(formatted_item)

        result_string = '\n'.join(final_array)
        return result_string

    def update_exercise(self, id, user_id, exercise_name, exercise_muscle, exercise_level, exercise_repetition):
        self.cursor.execute("UPDATE `exercises` SET `exercise_name` = ?, `exercise_muscle` = ?, `exercise_level` = ?, `exercise_repetition` = ? WHERE `id` = ? AND `user_id` = ?",
            (exercise_name,
            exercise_muscle,
            exercise_level,
            exercise_repetition,
            id,
            user_id))
        return self.conn.commit()
    
    def exercise_choose(self, user_id):
        result = self.cursor.execute("SELECT id, exercise_name, exercise_muscle, exercise_level, exercise_repetition FROM `exercises` WHERE `user_id` = ?", (user_id,))
        fetchall = result.fetchall()

        openai.api_key = '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'

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Choose the best one exercise from fitness and workout and explain why",
            max_tokens=1024,
            stop=None,
        )

        return response.choices[0].text.strip()
    
    def fitness_ai(self, user_id):
        result = self.cursor.execute("SELECT id, exercise_name, exercise_muscle, exercise_level, exercise_repetition FROM `exercises` WHERE `user_id` = ?", (user_id,))
        fetchall = result.fetchall()

        openai.api_key = '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'

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"How to become fitter? based on the exercise data of user: {fetchall}? Explain how",
            max_tokens=1024,
            stop=None,
        )

        return response.choices[0].text.strip()
    
    def close(self):
        self.connection.close()