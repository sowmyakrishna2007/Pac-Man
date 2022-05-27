f = open("grid.txt","r")
import random, time
import string
upper = string.ascii_uppercase
grid = []
grid_combined = []
for i in f.readlines():
    new = []
    for j in i:
        if j == "." or j == '=' or j == '-' or j == "p" or j == "*" or j in upper:
            new.append(j)
    grid.append(new)
    grid_combined.extend(new)
orig_p = grid_combined.index("p")
a = grid_combined.index("A")
b = grid_combined.index("B")
c = grid_combined.index("C")
d = grid_combined.index("D")
import pygame as p
def setup():
    global screen, clock
    p.init()
    screen = p.display.set_mode((800, 800))
    clock = p.time.Clock()
def set_board(current,red_ghost,pink,blue,yellow,pacman_right,tries,score,powered,scared,power_dict):
    global coordinates
    coordinates = []
    y = 100
    x_p = 120
    p.draw.rect(screen,"black",(50,710,200,50))
    for i in range(tries-1):
        screen.blit(pacman_right,(x_p,720))
        x_p += 45
    font = p.font.SysFont("Courier", 20)

    score_display = font.render(f"Score: {score}", True, 'white',100)
    screen.blit(score_display, (100,30))
    for i in range(20):
        x = 100
        for j in range(20):
            coordinates.append((x, y))
            if grid_combined[len(coordinates)-1] == '=':
                p.draw.rect(screen, "medium blue", (x, y, 30, 30),2)
                obstacle = p.image.load("obstacle.png")
                screen.blit(obstacle, (x,y))
            elif grid_combined[len(coordinates) - 1] == 'p':

                    screen.blit(current,(x+1,y+1))
            elif grid_combined[len(coordinates) - 1] == "C":
                if power_dict["C"] == True:
                    screen.blit(scared,(x,y))
                else:
                    screen.blit(red_ghost, (x+2, y))
            elif "A" in grid_combined[len(coordinates) - 1]:
                if power_dict["A"] == True:
                    screen.blit(scared,(x,y))
                else:
                    screen.blit(pink, (x+2, y))
            elif "B" in grid_combined[len(coordinates) - 1]:
                if power_dict["B"] == True:
                    screen.blit(scared,(x,y))
                else:
                    screen.blit(blue, (x+2, y))

            elif "D" in grid_combined[len(coordinates) - 1]:
                if power_dict["D"] == True:
                    screen.blit(scared,(x,y))
                else:
                    screen.blit(yellow, (x+2, y))
            elif grid_combined[len(coordinates)-1] == '.':
                p.draw.rect(screen, "black", (x+1, y+1, 28, 28))
                p.draw.circle(screen, "white", (x+15,y+15),4)
            elif grid_combined[len(coordinates)-1] == '*':
                p.draw.rect(screen, "black", (x+1, y+1, 28, 28))
                p.draw.circle(screen, "red", (x+15,y+15),8)
            else:
                p.draw.rect(screen, "black", (x+1, y+1, 28, 28))
            x += 30
        y += 30
def main():
    count = 0
    setup()
    global grid_combined
    global score
    global coordinates
    score = 0
    pacman_right = p.image.load('pacman_right.jpg')
    pacman_right = p.transform.scale(pacman_right, (27,27))
    pacman_left = p.image.load('pacman_left.jpg')
    pacman_left = p.transform.scale(pacman_left, (27, 27))
    pacman_down = p.image.load('pacman_down.jpg')
    pacman_down = p.transform.scale(pacman_down, (27, 27))
    pacman_up = p.image.load('pacman_up.jpg')
    pacman_up = p.transform.scale(pacman_up, (27, 27))
    red = p.image.load('red_ghost.png')
    red = p.transform.scale(red, (25,25))
    green = p.image.load('Green_ghost.png')
    green = p.transform.scale(green,(25,25))
    blue = p.image.load('blue_ghost.png')
    blue = p.transform.scale(blue, (25, 25))
    yellow = p.image.load('yellow_ghost.png')
    yellow = p.transform.scale(yellow, (25, 25))
    scared = p.image.load('scared_ghost.png')
    scared = p.transform.scale(scared, (25, 25))
    tries = 3
    powered = False
    power_dict = {"A": False, "B": False, "C": False, "D": False}
    set_board(pacman_right,red,green,blue,yellow,pacman_right,tries,score,powered,scared,power_dict)
    x = None
    current = pacman_right
    g = None
    is_moving = False

    while tries >= 1:
        copies = []
        copies_all = []
        done = False
        power_dict = {"A":False,"B":False,"C":False,"D":False}
        while not done:
            screen.fill(p.Color("black"))
            set_board(current,red,green,blue,yellow,pacman_right,tries,score,powered,scared,power_dict)
            for event in p.event.get():
                if event.type == p.QUIT:
                    done = True
                    tries = 0
                if event.type == p.KEYDOWN:
                    if event.key == p.K_RIGHT:
                        x = "Right"
                        current = pacman_right
                    if event.key == p.K_UP:
                        x = "Up"
                        current = pacman_up
                    if event.key == p.K_LEFT:
                        x = "Left"
                        current = pacman_left
                    if event.key == p.K_DOWN:
                        x = "Down"
                        current = pacman_down
                    is_moving = True
            ghost_indices = []
            ghosts = []

            for i in range(len(coordinates)):
                    if grid_combined[i] in upper:
                        ghost_indices.append(i)
                        ghosts.append(grid_combined[i])

            for i in ghost_indices:
                    pacman_index = grid_combined.index("p")
                    if power_dict[grid_combined[i]] == False:
                        if i + 1 == pacman_index or i - 1 == pacman_index or i == pacman_index-20 or i == pacman_index+20:
                            done = True
            if powered:
                count += 1
                if count == 100:
                    powered = False
                    power_dict = {"A":False,"B":False,"C":False,"D":False}
                    count = 0
            score_up = False
            y = grid_combined.index("p")
            try:
                f = copies_all[-2]
            except:
                pass
            try:
                j = copies[-2]

                k = j[y]
                if k in upper:
                    score += 200
                    while True:
                        q = random.randint(0,len(grid_combined)-1)
                        if grid_combined[q] != "=" and grid_combined[q] != "p":
                            grid_combined[q] = k
                            power_dict[k] = False
                            break
                if f[y] == ".":
                    score_up = True
                if score_up:
                    score += 10
            except:
                pass
            if x == "Right":
                y = grid_combined.index("p")+1
                z = grid_combined.index("p")

                if grid_combined[y] == "=":
                    x = None
                else:
                    if grid_combined[y] in upper and powered == False:
                        done = True
                    if grid_combined[y] == "*":
                        powered = True
                        power_dict = {"A":True,"B":True,"C":True,"D":True}

                    grid_combined[z] = "-"
                    grid_combined[y] = "p"

            elif x == "Up":
                y = grid_combined.index("p") - 20
                z = grid_combined.index("p")

                if grid_combined[y] == "=":
                    x = None
                else:
                    if grid_combined[y] in upper and powered == False:
                        done = True
                    if grid_combined[y] == "*":
                        powered = True
                        power_dict = {"A": True, "B": True, "C": True, "D": True}

                    grid_combined[z] = "-"
                    grid_combined[y] = "p"

            elif x == "Down":
                y = grid_combined.index("p") + 20
                z = grid_combined.index("p")

                if grid_combined[y] == "=":
                    x = None
                else:
                    if grid_combined[y] in upper and powered == False:
                        done = True
                    if grid_combined[y] == "*":
                        powered = True
                        power_dict = {"A": True, "B": True, "C": True, "D": True}

                    grid_combined[z] = "-"
                    grid_combined[y] = "p"
            elif x == "Left":
                y = grid_combined.index("p") - 1
                z = grid_combined.index("p")

                if grid_combined[y] == "=":
                    x = None
                else:
                    if grid_combined[y] in upper and powered == False:
                        done = True
                    if grid_combined[y] == "*":
                        powered = True
                        power_dict = {"A": True, "B": True, "C": True, "D": True}

                    grid_combined[z] = "-"
                    grid_combined[y] = "p"
            if is_moving:
                ghost_indices = []
                for i in range(len(coordinates)):
                    if grid_combined[i] in upper:
                        ghost_indices.append(i)
                for i in ghost_indices:
                    pacman_loc = coordinates[grid_combined.index("p")]
                    ghost_loc = coordinates[i]
                    y_diff = ghost_loc[1] - pacman_loc[1]
                    x_diff = ghost_loc[0] - pacman_loc[0]
                    try:
                        j = copies[-6]
                        if power_dict[grid_combined[i]] == False:
                            if y_diff < 0:
                                g1 = "Down"
                                # if (grid_combined[i+20] == "=" or grid_combined[i+40] == "=" or grid_combined[i+60] == "=" or grid_combined[i+80] == "=") and j[i+20] == "=":
                                #     g1 = "Up"
                            elif y_diff > 0:
                                g1 = "Up"
                                # if (grid_combined[i-20] == "=" or grid_combined[i-40] == "=" or grid_combined[i-60] or grid_combined[i-80] == "=") == "=" and j[i-20] == "=":
                                #
                                #     g1 = "Down"
                            if x_diff < 0:
                                g2 = "Right"
                                # if (grid_combined[i+1] == "=" or grid_combined[i+2] == "=" or grid_combined[i+3] == "=" or grid_combined[i+4] == "=") and j[i+1] == "=":
                                #     g2 = "Left"
                            elif x_diff > 0:
                                g2 = "Left"
                                # if (grid_combined[i-1] == "=" or grid_combined[i-2] == "=" or grid_combined[i-3] == "=" or grid_combined[i-4] == "=") and j[i-1] == "=":
                                #     g2 = "Right"

                        else:
                            if y_diff < 0:
                                g1 = "Up"

                            elif y_diff > 0:
                                g1 = "Down"
                                if grid_combined[i+20] == "=":
                                    g1 = "Up"

                            if x_diff < 0:
                                g2 = "Left"
                                if grid_combined[i-1] == "=":
                                    g2 = "Right"

                            elif x_diff > 0:
                                g2 = "Right"

                        g = random.choice([g1, g2])
                        lst = []
                        for j in copies[::-1]:
                            k = j[i]
                            if k == "-" or k == "." or k == "*":
                                lst.append(k)
                                break
                        if len(lst) == 0:
                            final = "."
                        else:
                            final = lst[0]
                        if g == "Down":
                            y = i + 20
                            z = i
                            orig_s = grid_combined[y]

                            orig = grid_combined[z]
                            if grid_combined[y] == "=" or grid_combined[y] in upper or grid_combined[y] == "p":
                                pass
                            else:
                                grid_combined[z] = final

                                grid_combined[y] = orig
                        if g == "Up":
                            y = i - 20
                            z = i
                            orig_s = grid_combined[y]
                            orig = grid_combined[z]
                            if grid_combined[y] == "=" or grid_combined[y] in upper or grid_combined[y] == "p":
                                g = g2
                            else:
                                grid_combined[z] = final
                                grid_combined[y] = orig
                        if g == "Right":
                            y = i + 1
                            z = i
                            orig_s = grid_combined[y]
                            orig = grid_combined[z]
                            if grid_combined[y] == "=" or grid_combined[y] in upper or grid_combined[y] == "p":
                                g = g1
                            else:
                                grid_combined[z] = final
                                grid_combined[y] = orig
                        if g == "Left":
                            y = i - 1
                            z = i
                            orig_s = grid_combined[y]
                            orig = grid_combined[z]
                            if grid_combined[y] == "=" or grid_combined[y] in upper or grid_combined[y] == "p":
                                g = g2
                            else:
                                grid_combined[z] = final
                                grid_combined[y] = orig

                    except:
                        pass
            if done == True:
                    p.display.flip()
                    time.sleep(0.7)
                    tries -= 1
                    y = orig_p
                    z = grid_combined.index("p")
                    grid_combined[z] = "-"
                    grid_combined[y] = "p"
                    is_moving=False
                    x = None
                    current = pacman_right
                    ghost_indices = []
                    for i in range(len(coordinates)):
                        if grid_combined[i] in upper:
                            ghost_indices.append(i)

                    for i in ghost_indices:
                        for j in copies[::-1]:
                            orig = j[i]
                            if orig not in upper and orig != "p":
                                break
                        if grid_combined[i] == "A":
                            grid_combined[i] = orig

                        if grid_combined[i] == "B":
                            grid_combined[i] = orig

                        if grid_combined[i] == "C":
                            grid_combined[i] = orig

                        if grid_combined[i] == "D":
                            grid_combined[i] = orig
                    grid_combined[c] = "C"
                    grid_combined[a] = "A"
                    grid_combined[b] = "B"
                    grid_combined[d] = "D"

            copy = grid_combined[:]
            copies.append(copy)
            try:
                if copies[-1] == copies[-2]:
                    copies.remove(copy)

            except:
                pass
            copies_all.append(copy)


            p.display.flip()
            if done == True and tries == 0:
                font = p.font.SysFont("Courier", 50)

                game_over = font.render("GAME OVER", True, 'red')
                screen.blit(game_over, (250, 50))
                p.display.flip()
                time.sleep(3)
            clock.tick(6)

    p.quit()

if __name__ == "__main__":
    main()