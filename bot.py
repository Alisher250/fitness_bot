from aiogram import executor
from dispatcher import dp
from aiogram import types
from dispatcher import dp
import config
import re
from db import Database
Database = Database('fitnessdb.db')
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

    
class AddExerciseStates(StatesGroup):
    EXERCISE_NAME = State()
    EXERCISE_MUSCLE = State()
    EXERCISE_LEVEL = State()
    EXERCISE_REPETITION = State()

class UpdateExerciseStates(StatesGroup):
    EXERCISE_ID = State()
    EXERCISE_NAME = State()
    EXERCISE_MUSCLE = State()
    EXERCISE_REPETITION = State()
    EXERCISE_LEVEL = State()


@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not Database.user_exists(message.from_user.id)):
        Database.add_user(message.from_user.id,message.from_user.username, message.from_user.first_name, message.from_user.last_name)

    photo = open('bot.png', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Add Exercise'),
               types.KeyboardButton('Select Exercises'),
               types.KeyboardButton('Update Exercise'),
               types.KeyboardButton('Get Nutrition Plan'),
               types.KeyboardButton('Which exercise to use?(AI)'),
               types.KeyboardButton('How to become fitter?(AI)'))
    
    await message.bot.send_photo(message.from_user.id, photo)
    await message.bot.send_message(message.from_user.id, f"Welcome {message.from_user.first_name}! This is the Fitness Bot, that will help you to get the best exercises for you and overall improve you health!", reply_markup=markup)

@dp.message_handler()
async def handle_buttons(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    if text == 'Add Exercise':
        photo = open('fitness.jpg', 'rb')
        await message.bot.send_photo(message.from_user.id, photo)
        await message.bot.send_message(user_id,"Please enter the exercise name:")
        await AddExerciseStates.EXERCISE_NAME.set()

    if text == 'Select Exercises':
        await message.bot.send_message(user_id, Database.get_exercises(user_id))
        
    if text == 'Update Exercise':
        await message.answer("Please provide the exercise ID:")
        await UpdateExerciseStates.EXERCISE_ID.set()

    if text == 'Get Nutrition Plan':
        photo = open('nutrition_plan.jpg', 'rb')
        await message.bot.send_photo(message.from_user.id, photo)

    if text == 'Which exercise to use?(AI)':
        photo = open('fitness2.jpg', 'rb')
        await message.bot.send_photo(message.from_user.id, photo)
        await message.bot.send_message(user_id, "One second please")
        await message.bot.send_message(user_id, Database.exercise_choose(user_id))

    if text == 'How to become fitter?(AI)':
        await message.bot.send_message(user_id, Database.fitness_ai(user_id))

@dp.message_handler(state=AddExerciseStates.EXERCISE_NAME)
async def add_exercise_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_name'] = message.text
    await message.answer("Enter the muscle to develop with this exercise :")
    await AddExerciseStates.next()

@dp.message_handler(state=AddExerciseStates.EXERCISE_MUSCLE)
async def add_exercise_muscle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_muscle'] = message.text
    await message.answer("Enter the level of difficulty of this exercise:")
    await AddExerciseStates.next()

@dp.message_handler(state=AddExerciseStates.EXERCISE_LEVEL)
async def add_exercise_level(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_level'] = message.text
    await message.answer("Enter the needed repetitions number for this exercise :")
    await AddExerciseStates.next()

@dp.message_handler(state=AddExerciseStates.EXERCISE_REPETITION)
async def add_exercise_repetition(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_repetition'] = message.text
        user_id = message.from_user.id
        if all(data.values()):
            Database.add_exercise(user_id, data['exercise_name'], data['exercise_muscle'], data['exercise_level'], data['exercise_repetition']) 
            await message.answer("Exercise data added successfully!")
            await state.finish()
        else:
            await message.answer("Some data is missing. Please try again.")



@dp.message_handler(state=UpdateExerciseStates.EXERCISE_ID)
async def update_exercise_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_id'] = message.text
    await message.answer("Enter updated exercise name:")
    await UpdateExerciseStates.EXERCISE_NAME.set()

@dp.message_handler(state=UpdateExerciseStates.EXERCISE_NAME)
async def update_exercise_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_name'] = message.text
    await message.answer("Enter updated exercise muscle:")
    await UpdateExerciseStates.EXERCISE_MUSCLE.set()

@dp.message_handler(state=UpdateExerciseStates.EXERCISE_MUSCLE)
async def update_exercise_muscle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_muscle'] = message.text
    await message.answer("Enter updated exercise repetition:")
    await UpdateExerciseStates.EXERCISE_REPETITION.set()

@dp.message_handler(state=UpdateExerciseStates.EXERCISE_REPETITION)
async def update_crop_expense(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_repetition'] = message.text
    await message.answer("Enter updated exercise level:")
    await UpdateExerciseStates.EXERCISE_LEVEL.set()

@dp.message_handler(state=UpdateExerciseStates.EXERCISE_LEVEL)
async def update_crop_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exercise_level'] = message.text
        if all(data.values()):
            Database.update_exercise(data['exercise_id'], message.from_user.id, data['exercise_name'], data['exercise_muscle'], data['exercise_level'], data['exercise_repetition']) 
            await message.answer("Exercise data added successfully!")
            await state.finish()
        else:
            await message.answer("Some data is missing. Please try again.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)