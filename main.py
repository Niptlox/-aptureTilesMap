import pygame as pg

count_players = 3
map_size = (6, 4)


def get_points_img(n, size):
    w, h = size
    img = pg.Surface(size).convert_alpha()
    img.fill((0, 0, 0, 0))
    r = 3
    if n == 1:
        pg.draw.circle(img, "white", (w // 2, h // 2), r)
    elif n == 2:
        pg.draw.circle(img, "white", (w // 3, h // 2), r)
        pg.draw.circle(img, "white", (w // 3 * 2, h // 2), r)
    elif n == 3:
        pg.draw.circle(img, "white", (w // 3, h // 3), r)
        pg.draw.circle(img, "white", (w // 3 * 2, h // 3), r)
        pg.draw.circle(img, "white", (w // 2, h // 3 * 2), r)
    elif n == 4:
        pg.draw.circle(img, "white", (w // 3, h // 3), r)
        pg.draw.circle(img, "white", (w // 3 * 2, h // 3), r)
        pg.draw.circle(img, "white", (w // 3, h // 3 * 2), r)
        pg.draw.circle(img, "white", (w // 3 * 2, h // 3 * 2), r)
    elif n == 5:
        pg.draw.circle(img, "white", (w // 3, h // 3), r)
        pg.draw.circle(img, "white", (w // 3 * 2, h // 3), r)
        pg.draw.circle(img, "white", (w // 3, h // 3 * 2), r)
        pg.draw.circle(img, "white", (w // 3 * 2, h // 3 * 2), r)
        pg.draw.circle(img, "white", (w // 2, h // 2), r)
    return img


def get_img_of_color(color, size):
    img = pg.Surface(size)
    img.fill(color, (1, 1, size[0] - 2, size[1] - 2))
    return img

pg.font.init()

WSIZE = (720, 480)
screen = pg.display.set_mode(WSIZE)
TSIZE = (48, 48)

points_imgs = [get_points_img(i, TSIZE) for i in range(0, 5 + 1)]
map_array = [[[None, 0] for j in range(map_size[0])] for i in range(map_size[1])]
running = True
color_players = {
    0: "red",
    1: "green",
    2: "blue",
    3: "yellow",
}


def add_point_to_tile(pos, player, settplayer=False):
    x, y = pos
    if 0 <= pos[0] < map_size[0] and 0 <= pos[1] < map_size[1]:
        # map_array[pos[1]][pos[0]][0] is None or
        if map_array[pos[1]][pos[0]][0] == player or settplayer:
            map_array[pos[1]][pos[0]][0] = player
            map_array[pos[1]][pos[0]][1] += 1
            if map_array[pos[1]][pos[0]][1] == max_points_tile:
                map_array[pos[1]][pos[0]] = [None, 0]
                add_point_to_tile((x - 1, y), player, settplayer=True)
                add_point_to_tile((x + 1, y), player, settplayer=True)
                add_point_to_tile((x, y - 1), player, settplayer=True)
                add_point_to_tile((x, y + 1), player, settplayer=True)
            return True
    return False


def restart_game():
    global map_array, now_player, win_player
    map_array = [[[None, 0] for j in range(map_size[0])] for i in range(map_size[1])]
    now_player = 0
    win_player = None
    set_players(count_players)
    check_players()


def set_players(count, sett=3):
    w, h = map_size
    poses = [(1, 1), (w - 2, h - 2), (w - 2, 1), (1, h - 2)]
    for i in range(count):
        map_array[poses[i][1]][poses[i][0]] = [i, sett]


def check_players():
    global player_lives, win_player
    player_lives = [0] * count_players
    for iy in range(map_size[1]):
        for ix in range(map_size[0]):
            p = map_array[iy][ix][0]
            if p is not None:
                player_lives[p] = 1
    if sum(player_lives) == 1:
        win_player = player_lives.index(1)


def next_player():
    global now_player
    now_player = (now_player + 1) % count_players
    if not player_lives[now_player]:
        next_player()

win_surface = pg.Surface(WSIZE).convert_alpha()
win_surface.fill((0, 0, 0, 0))
font = pg.font.SysFont("", 40)


win_player = None
max_points_tile = 4
player_lives = [1] * count_players
now_player = 0
colors_imgs = {i: get_img_of_color(color_players[i], TSIZE) for i in color_players}
colors_imgs[None] = get_img_of_color("gray", TSIZE)
map_offset_surface = (50, 50)
set_players(count_players)
while running:
    screen.fill("black")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if win_player is None:
                if event.button == pg.BUTTON_LEFT:
                    map_pos = (event.pos[0] - map_offset_surface[0]) // TSIZE[0], \
                              (event.pos[1] - map_offset_surface[1]) // TSIZE[1]
                    if 0 <= map_pos[0] < map_size[0] and 0 <= map_pos[1] < map_size[1]:
                        if add_point_to_tile(map_pos, now_player):
                            check_players()
                            next_player()
        if event.type == pg.KEYDOWN:
            if win_player is not None and event.key == pg.K_SPACE:
                restart_game()

    for iy in range(map_size[1]):
        for ix in range(map_size[0]):
            img = colors_imgs[map_array[iy][ix][0]]
            screen.blit(img, (map_offset_surface[0] + ix * TSIZE[0], map_offset_surface[1] + iy * TSIZE[1]))
            img_c = points_imgs[map_array[iy][ix][1]]
            screen.blit(img_c, (map_offset_surface[0] + ix * TSIZE[0], map_offset_surface[1] + iy * TSIZE[1]))
    if win_player is not None:
        screen.fill("black", rect=(WSIZE[0]//4, WSIZE[1]//3, WSIZE[0]//2, WSIZE[1]//3))
        text = font.render("WIN PLAYER " + color_players[win_player], True, color_players[win_player])
        screen.blit(text, (WSIZE[0] // 2 - text.get_width() // 2, WSIZE[1] // 2 - 20))
        text2 = font.render("press SPACE for restart", True, "white")
        screen.blit(text2, (WSIZE[0] // 2 - text2.get_width()//2, WSIZE[1] // 2 + 20))
    screen.blit(colors_imgs[now_player], (0, 0))
    pg.display.flip()
