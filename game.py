from random import randint
import time

WIDTH = 800
HEIGHT = 600

game_over = False
end_done = False
raining = False
happy = True
hit_fang = False

cow = Actor("cow")
cow.pos = (WIDTH / 2), (HEIGHT / 2)

zap = Actor("zap")

watering = False

flowers = []
flower_status = []
flower_game_text = []

_time = 0
start_time = time.time()

def draw():
    global game_over, _time, start_time, end_done
    if not game_over:
        screen.clear()
        if raining:
            screen.blit("garden-rain", (0,0))
        else:
            screen.blit("garden", (0,0))
        cow.draw()
        index = 0 
        for flower in flowers:
            flower.draw()
            screen.draw.text(flower_game_text[index], (flower.x, flower.y - 30), color="black")
            index += 1
        _time = int(time.time() - start_time)
        screen.draw.text("Garden happy for " + str(_time) + " seconds!!!", (10,10), color="black")
    else:
        if not end_done:
            if not happy:
                screen.draw.text("GARDEN UNHAPPY!!!", (10,50), color="red")
            elif hit_fang:
                screen.draw.text("FANGFLOWER ATTACK!!!", (10,50), color="red")
            else:
                screen.draw.text("GAME OVER!!!", (10,50), color="red")
            end_done = True
        if hit_fang:
            zap.draw()

def update():
    draw()
    check_keyboard()
    check_if_unhappy()
    update_game_text()
    update_fang_pos()
    check_fang_hit()

def add_flower():
    new_flower = Actor("flower")
    new_flower.pos = randint(0, WIDTH), randint(150, HEIGHT)
    flowers.append(new_flower)
    flower_status.append("happy")
    flower_game_text.append("")
    clock.schedule(add_flower, 4)

def wilt_flower():
    if not game_over:
        index = randint(0, len(flowers) - 1)
        if flower_status[index] == "happy" and not raining:
            flowers[index].image = "flower-wilt"
            flower_status[index] = 10
        clock.schedule(wilt_flower, 3)

def update_wilt():
    global flower_status
    if not game_over:
        index = 0
        for flower in flowers:
            if (not flower_status[index] == "happy") and (not flower_status[index] == "fangflower"):
                if raining:
                    flower_status[index] = "happy"
                    flower.image = "flower"
                else:
                    flower_status[index] -= 1
            index += 1
        clock.schedule(update_wilt, 1)

def update_fang_pos():
    global flower_status, flowers
    if not game_over:
        index = 0
        for flower in flowers:
            if flower_status[index] == "fangflower":
                dx = cow.x - flower.x
                dy = cow.y - flower.y
                stepx = dx / 50
                stepy = dy / 50
                flower.x += stepx
                flower.y += stepy
            index += 1

def fangflower_mutate():
    global flowers, flower_status
    if not game_over:
        index = randint(0, len(flowers) - 1)
        if not flower_status[index] == "fangflower":
            flowers[index].image = "fangflower"
            flower_status[index] = "fangflower"
        if raining:
            clock.schedule(fangflower_mutate, 5)
        else:
            clock.schedule(fangflower_mutate, 15)

def check_if_unhappy():
    global happy, game_over
    index = 0
    for flower in flowers:
        if (not flower_status[index] == "happy") and (not flower_status[index] == "fangflower"):
            if int(flower_status[index]) < 1:
                happy = False
                game_over = True
        index += 1

def check_fang_hit():
    global hit_fang, game_over
    index = 0
    for flower in flowers:
        if flower_status[index] == "fangflower":
            if flower.colliderect(cow):
                zap.pos = cow.x, cow.y
                hit_fang = True
                game_over = True
        index += 1

add_flower()
clock.schedule(wilt_flower, 3)
clock.schedule(fangflower_mutate, 15)
update_wilt()

def check_keyboard():
    global game_over, watering
    if not game_over:
        if keyboard.space:
            cow.image = "cow-water"
            watering = True
            clock.schedule(water_flower, 0.5)
        if watering:
            if keyboard.left and cow.x > 0:
                cow.x -= 2
            if keyboard.right and cow.x < WIDTH:
                cow.x += 2
            if keyboard.up and cow.y > 150:
                cow.y -= 2
            if keyboard.down and cow.y < HEIGHT:
                cow.y += 2
        else:
            if keyboard.left and cow.x > 0:
                cow.x -= 5
            if keyboard.right and cow.x < WIDTH:
                cow.x += 5
            if keyboard.up and cow.y > 150:
                cow.y -= 5
            if keyboard.down and cow.y < HEIGHT:
                cow.y += 5

def water_flower():
    global watering
    if not game_over:
        cow.image = "cow"
        watering = False
        index = 0
        for flower in flowers:
            if (flower.colliderect(cow) and flower.image == "flower-wilt"):
                flower.image = "flower"
                flower_status[index] = "happy"
                break
            index += 1

def update_game_text():
    index = 0
    for flower in flowers:
        if not flower_status[index] == "happy" and not flower_status[index] == "fangflower":
            flower_game_text[index] = str(flower_status[index])
        else:
            flower_game_text[index] = ""
        index += 1

def weather_rain():
    global raining
    raining = True
    clock.schedule(weather_sun, 20)

def weather_sun():
    global raining
    raining = False
    clock.schedule(weather_rain, 50)

weather_sun()