import requests
import discord
import random
import asyncio
import time

from discord.ext import commands
from discord import app_commands



bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
token = 'MTI2NzA4ODQ4NzAzMTUwNDk4OA.GokdVl.i8Bn500DncUmBpOk_PL0__lTXhW2qwn2gvik6Y'

current_pokemon = None
current_guess_pokemon = None
guessed = False


user_inventory = {}

#ฟังก์ชั่นคำนวณสุ่มเวลาเป็นหน่วยนาที
def get_random_time(min_minutes,max_minutes):
    return random.randint(min_minutes,max_minutes) * 60
 
 
def get_count_time(start_time):
    second = time.time() - start_time
    return second


def random_all_pokemon():
    channel = bot.get_channel(1181615432512311357)#id ห้อง
    bot.loop.create_task(random_pokemon(channel))  # เริ่มทำงานสุ่ม Pokémon
    channel = bot.get_channel(1018888744390107179)
    bot.loop.create_task(random_guess_pokemon(channel))

def get_generation(pokemon_id):
    """ ฟังก์ชันในการคำนวณ generation โดยใช้ช่วงของ Pokémon ID """
    if 1 <= pokemon_id <= 151:
        return 1
    elif 152 <= pokemon_id <= 251:
        return 2
    elif 252 <= pokemon_id <= 386:
        return 3
    elif 387 <= pokemon_id <= 493:
        return 4
    elif 494 <= pokemon_id <= 649:
        return 5
    elif 650 <= pokemon_id <= 721:
        return 6
    elif 722 <= pokemon_id <= 809:
        return 7
    elif 810 <= pokemon_id <= 898:
        return 8
    else:
        return None  # สำหรับกรณี ID ที่ไม่ถูกต้อง


#แจ้งบอททำงาน
@bot.event
async def on_ready():
    global current_pokemon
    i = 1
    print("Bot online")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)") #บอกมีทั้งหมดกี่คำสั่ง
    print("")
    
    random_all_pokemon()
    
    for command in synced:  #วนรูปเอาชื่อคำสั้่ง
        print(f"{i}.{command}")
        i += 1
        
    start_time = time.time()
    while (True):
        time_count = get_count_time(start_time)
        time_check = int(time_count)
        format_time  = time.strftime("%H:%M:%S", time.gmtime(time_count)) # แปลงเวลาจากวินาทีไปเป็น ชั่วโมง:นาที:วินาที
        print(f"\r{format_time}", end="")
        await asyncio.sleep(1)  # หน่วงเวลา 1 วินาที (ใช้ await)
        #ถ้าหากเวลาที่เช็คเท่ากับ 60 วินาที จะทำการแสดงโปเกม่อนที่เกิดในปัจจุบัน
        if (time_check % 60 == 0):
            print()  
            print("----- Current Pokémon Info -----")
            print(f"Current Pokémon: {current_pokemon}")
            print(f"Current Pokémon Guess: {current_guess_pokemon}")
            print("-------------------------------")
            
            time_check = 0
        
        

#แจ้งคนเข้า 
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1019823883374821476)#id ห้อง
    text = f"Welcome to the server,{member.mention}"

    embed = discord.Embed(title = "Welcome to server",description = text ,color = 0xF5F925)
    embed.set_thumbnail(url=member.avatar.url)

    #await channel.send(text) #ส่งข้อความไปห้อง
    await channel.send(embed = embed)
    #await member.send(text) #ส่งส่วนตัว

#แจ้งคนออก
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1019823883374821476)
    text = f"Goodbye to this server,{member.mention}"

    embed = discord.Embed(title = "Goodbye to this server",description = text ,color = 0xF5F925)
    embed.set_thumbnail(url=member.avatar.url)

    await channel.send(embed=embed)
    #await channel.send(text)


#ข้อความตอบกลับ User ที่แท็ก bot
@bot.event
async def on_message(message):
    
    image_urls = [
        "https://images-ext-1.discordapp.net/external/iorUQXd6PXaPIaQRCuAHF3AVdAhndu9oIJCgKP-Riig/https/media.tenor.com/5PyqOsngA00AAAPo/boku-no-hero-academia-my-hero-academia.mp4",
        "https://images-ext-1.discordapp.net/external/U7v2_YCRngS2uGonTO7tMFnDBFh8fqITiliSmqXCre0/https/media.tenor.com/s52r3TzUGUIAAAPo/sigma-patrick-bateman.mp4",
        "https://images-ext-1.discordapp.net/external/-i4rrfeFqOgx5VesovqhaQFVVKJ-hRh2wdqxfUAoe8U/https/media.tenor.com/9dzu6DmPN-sAAAPo/me-when-piper.mp4"
    ]
    
    # ตรวจสอบว่าข้อความมาจากบอทหรือไม่
    if message.author == bot.user:
        return
    
    message_user = message.content
    
    if message_user == "hello":
        await message.channel.send("Hello kub "+str(message.author.name))
        
    if (bot.user in message.mentions and message_user):
        await message.channel.send(random.choice(image_urls))
        
    await bot.process_commands(message) #ทำคำสั่ง event แล้วไปทำคำสั่ง bot command ต่อ


#random pokemon เกิดในระยะเวลา
@bot.event 
async def random_pokemon(channel):
    
    global current_pokemon
    
    while True: 
        
        random_time = get_random_time(1,3)
        await asyncio.sleep(random_time) 
        
         # เรียก API ของ Pokémon เพื่อสุ่มข้อมูล
        pokemon_id = random.randint(1, 898) # Pokémon มีทั้งหมด 898 ตัวในปัจจุบัน
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url)
        
        
        if (response.status_code == 200):
            data = response.json()
            random_pokemon_name = data['name'].lower()
            element_pokemon = data['types'][0]['type']['name']
            image_pokemon = data['sprites']['other']['official-artwork']['front_default']
            
            # อัพเดทค่าโปเกม่อนที่สุ่มได้ล่าสุด
            current_pokemon = random_pokemon_name
            
            embed = discord.Embed(title=f"✨A {element_pokemon} {random_pokemon_name.capitalize()} Pokémon Has appeared✨",
                            description=f"Now You can catch this Pokémon before leave it!",
                            color = 0xF5F925,
                            timestamp=discord.utils.utcnow())
            
            embed.set_author(name="pokemon-bot",icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRszeXdQ_4pQX0tnIbBFWi8OSN0jtVLVmEDbw&s")
            embed.set_image(url=image_pokemon)
            
            
            # ส่งข้อความ Pokémon ปรากฏในแชท
            await channel.send(embed=embed)
        
        else :
            print("⚠️ Failed to fetch Pokémon data from the API.")
 
        
#randon pokemon ไว้สำหรับทาย
@bot.event
async def random_guess_pokemon(channel):
    
    global current_guess_pokemon
    global guessed
    while (True):
        
        random_time_guess = get_random_time(1,3)
        await asyncio.sleep(random_time_guess) 
        
        pokemon_id = random.randint(1,898)
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url)
        
        if(response.status_code == 200):
            data = response.json()
            random_guess_pokemon_name = data['name'].lower()
            element_pokemon = data['types'][0]['type']['name'].capitalize()
            weight_pokemon = data['weight']
            height_pokemon = data['height']
            ability_pokemon = data['abilities'][0]['ability']['name'].capitalize()
            
            current_guess_pokemon = random_guess_pokemon_name
            guessed = False
            
            # เพิ่มคำใบ้ง่ายๆ
            name_length = len(random_guess_pokemon_name)
            first_letter = random_guess_pokemon_name[0].upper()
            last_letter = random_guess_pokemon_name[-1].upper()

            # คำใบ้เพิ่มเติม: จำนวนตัวอักษร, ตัวแรก, ตัวสุดท้าย, Generation
            generation_hint = get_generation(pokemon_id)
            #generation_hint = pokemon_id // 151 + 1  # ตัวอย่างการคำนวณ generation (คร่าวๆ)
            
            embed = discord.Embed(
                title="Guess the Pokémon!", 
                description="Can you guess which Pokémon this is? /guess to guess Pokémon",
                color = 0xF5F925,
                timestamp=discord.utils.utcnow()
            )
            embed.set_author(name="pokemon-bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRszeXdQ_4pQX0tnIbBFWi8OSN0jtVLVmEDbw&s")
            
            # ข้อมูลคำใบ้เพิ่มเติม
            embed.add_field(name="Element", value=element_pokemon, inline=False)
            embed.add_field(name="Weight", value=f"{weight_pokemon / 10} kg", inline=True)
            embed.add_field(name="Height", value=f"{height_pokemon / 10} m", inline=True)
            embed.add_field(name="Ability", value=ability_pokemon, inline=True)
            
            # คำใบ้ที่ง่ายขึ้น
            embed.add_field(name="Hint 1", value=f"Name has {name_length} letters.", inline=False)
            embed.add_field(name="Hint 2", value=f"Starts with '{first_letter}' and ends with '{last_letter}'.", inline=False)
            embed.add_field(name="Hint 3", value=f"This Pokémon is from Generation {generation_hint}.", inline=False)

            await channel.send(embed=embed)
        else:
            print("⚠️ Failed to fetch Pokémon data from the API.")



#กำหนดคำสั่งให้บอท
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello{ctx.author.name}!")


#Slash command
@bot.tree.command(name='hellobot',description='for hello ambatron')
async def hellobot(interaction):
    #ส่งข้อความตอบกลับไปให้ ีuser
    await interaction.response.send_message("Hello I'm ambatron 🤖")


@bot.tree.command(name="ambraton_check")
@app_commands.describe(choice = "human or bot?")
async def namecommand(interaction,choice:str):
    if(choice == "human"):
        await interaction.response.send_message(f"You are not a {choice} welcome {interaction.user.name}")
    elif(choice == "bot"):
        await interaction.response.send_message(f"You are {choice} welcome {interaction.user.name}")


#Help command
@bot.tree.command(name="help",description="Bot command")
async def helpcommand(interaction):
    embed = discord.Embed(title="Help - bot command",
                          description="Bot commands",
                          color = 0xF5F925,
                          timestamp=discord.utils.utcnow())
    
    #ใส่ข้อมูลใน field 
    embed.add_field(name="/hellobot",value="Hello command",inline=False)
    embed.add_field(name="/ambraton_check",value="Check user command",inline=False)
    embed.add_field(name="/pokemon_check",value="Check Pokémon command",inline=False)
    embed.add_field(name="/inventory",value="Check your inventory",inline=False)
    
    embed.set_author(name=interaction.user.name,icon_url=interaction.user.avatar.url)
    #ใส่ข้อมูลส่วนท้าย
    embed.set_footer(text=interaction.user.name,icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed)


#Pokemon check
@bot.tree.command(name="pokémon_check",description="pokémon_check input name for search")
@app_commands.describe(character = "Name:")
async def check_pokemon(interaction,character:str):
    url = f"https://pokeapi.co/api/v2/pokemon/{character}"
    response = requests.get(url)
    
    print(f"\n{response.status_code}")
    print(" ")
    if (response.status_code == 200):
        data = response.json()
        pokemon_name = data['name'].capitalize()
        pokemon_image = data['sprites']['front_default']
        abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
        pokemon_type = ', '.join([t['type']['name'] for t in data['types']])


        embed = discord.Embed(title=f"Pokemon : {pokemon_name}",
                          description="Here are the details of the Pokémon:",
                          color = 0xF5F925,
                          timestamp=discord.utils.utcnow())
        
        #ใส่ข้อมูลใน field 
        embed.set_author(name="pokemon-bot",icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRszeXdQ_4pQX0tnIbBFWi8OSN0jtVLVmEDbw&s")
        embed.set_thumbnail(url=pokemon_image) 
        embed.add_field(name="Name", value=pokemon_name, inline=True)
        embed.add_field(name="Type", value=pokemon_type, inline=False)
        embed.add_field(name="Abilities", value=abilities, inline=False)

        
        #ใส่ข้อมูลส่วนท้าย
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)
    else :
        await interaction.response.send_message(f"Don't have this name **{character}** pls try again")
    
    
#เช็คกระเป๋าผู้ใช้งาน
@bot.tree.command(name="inventory",description="check you inventory")
async def check_inventory(interaction: discord.Interaction):
    user_name = interaction.user.name
    items = user_inventory.get(user_name, [])
    if items:
        item_list = ", ".join(items)
        embed = discord.Embed(title="Your inventory",
                            description=f"Your pokémon : {item_list}",
                            color = 0xF5F925,
                            timestamp=discord.utils.utcnow())
        
        embed.set_author(name=user_name,icon_url=interaction.user.avatar.url)

        embed.set_footer(text=user_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"{user_name} your inventory is **empty.**")


# คำสั่งจับโปเกม่อน
@bot.tree.command(name="catch", description="Catch Pokémon")
async def catch_pokemon(interaction: discord.Interaction):
    global current_pokemon  # เข้าถึงตัวแปรโปเกม่อนที่สุ่มได้ล่าสุด
    user_name = interaction.user.name

    if current_pokemon:
        # Add the caught Pokémon to the user's inventory
        if user_name not in user_inventory:
            user_inventory[user_name] = []  # Initialize inventory if user doesn't have one
        else:
            user_inventory[user_name].append(current_pokemon)  # Append Pokémon to user's inventory
            await interaction.response.send_message(f"{user_name} caught a {current_pokemon.capitalize()}!")
            # Reset the variable after the Pokémon is caught
            current_pokemon = None
    else:
        await interaction.response.send_message("No Pokémon available to catch right now!")

#@bot.tree.command(name="clear",description="clear chat")
#@app_commands.describe(time = "What Time want to clear?")
#async def clear_chat (interaction,time:str):
    
   # target_time = datetime.strptime(time, "%I:%M %p").time()
    
   # if (time == format_time):
    #    de


@bot.tree.command(name="guess", description="Guess Pokemon")
@app_commands.describe(characters="Name:")
async def guess_pokemon(interaction, characters: str):
    global current_guess_pokemon
    global guessed
    
    if current_guess_pokemon:
        if guessed:
            await interaction.response.send_message("🛑 It has already been guessed! Wait for the next Pokémon.")
            return

        if characters.lower() == current_guess_pokemon:
            url = f"https://pokeapi.co/api/v2/pokemon/{current_guess_pokemon}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                pokemon_image = data['sprites']['other']['official-artwork']['front_default']  
                
                embed = discord.Embed(
                    title=f"✅ Correct! It's **{current_guess_pokemon.capitalize()}**!",
                    description="You guessed the correct Pokémon!",
                    color=0xF5F925,
                    timestamp=discord.utils.utcnow()
                )
                embed.set_image(url=pokemon_image)
                
                await interaction.response.send_message(embed=embed)
                guessed = True
            else:
                await interaction.response.send_message("⚠️ Error fetching Pokémon data from the API.")
        else:
            await interaction.response.send_message("❌ Try again! Incorrect guess.")
    else:
        await interaction.response.send_message("🔍 No Pokémon to guess right now!")
        

bot.run(token)