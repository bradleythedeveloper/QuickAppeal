import discord
from discord.ext import commands
from discord.utils import find
import mysql.connector
from mysql.connector import Error
from secret.config import get_sql_root_pw, get_api_token, get_service_key_path
import random
import time

pw = get_sql_root_pw()

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_db_connection("localhost", "root", pw, "quickappeal")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

client = commands.Bot(command_prefix='qa!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for appeals'))

@client.event
async def on_guild_join(guild):
    general = find(lambda x: 'general' in x.name,  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        message = await general.send('Hello {}!'.format(guild.name))
        serverID = message.guild.id

#@client.event
#async def on_message(message):

