import pygame,random,time
pygame.init()

# 屏幕 设定
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 960
game_display = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))

# 随机颜色的函数
def random_color():
    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    return color

# NPC 类设定
class NPC:
    def __init__(self, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.speed = random.randint(2,10)
        self.health = random.randint(20,200)
        self.view = random.randint(30,200)
        self.attack = random.randint(10,100)
        self.aggressive = random.randint(1,3)
        self.reproduction_time = random.randint(30,500)
        self.time_since_reproduction = 0
        self.killed = 0

    # 更新 NPC 的属性
    def update(self, npc_list):
        self.move(npc_list)
        if self.health <= 0:
            npc_list.remove(self)
        self.time_since_reproduction += 1
        if self.time_since_reproduction >= self.reproduction_time:
            self.reproduce(npc_list)
            self.time_since_reproduction = 0

    # NPC 撤回 以防止重叠
    def retreat(self, other_x, other_y):
        if self.x > other_x:
            self.x += self.speed
        else:
            self.x -= self.speed
        if self.y > other_y:
            self.y += self.speed
        else:
            self.y -= self.speed

    # NPC 繁殖
    def reproduce(self, npc_list):
        offspring = NPC(self.name, self.x, self.y, self.color)
        npc_list.append(offspring)

    # NPC 移动
    def move(self, npc_list):
        npc_in_view = self.npc_in_view(npc_list)
        if npc_in_view:
            nearest_npc = self.nearest_npc(npc_in_view)
            if self.check_colliding_npcs(nearest_npc) == True:
                self.attack_npc(nearest_npc)

            if self.aggressive == 1:
                self.retreat(nearest_npc.x, nearest_npc.y)
            elif self.aggressive == 2:
                if self.health > self.health / 2:
                    self.approach(nearest_npc.x, nearest_npc.y)
                else:
                    self.retreat(nearest_npc.x, nearest_npc.y)
            else:
                self.approach(nearest_npc.x, nearest_npc.y)
        else:
            self.stray()        
        # 如果超出了范围，NPC将出现在另一象限
        if self.x < 0:
            self.x = 1280
        if self.x > 1280:
            self.x = 0
        if self.y < 0:
            self.y = 960
        if self.y > 960:
            self.y = 0

    #检测NPC碰撞
    def check_colliding_npcs(self, nearest_npc):
        if abs(self.x - nearest_npc.x) <= self.radius*2 or abs(self.y - nearest_npc.y) <= self.radius*2:
            return True
        else:
            return False  

    # NPC 攻击
    def attack_npc(self, other_npc):
        if other_npc.name == self.name and other_npc.color == self.color: #自己繁殖的NPC不攻击
            return
        else:
            other_npc.health -= self.attack
        
        if other_npc.health <= 0:
            self.killed += 1

    # NPC 逃跑
    def retreat(self, other_x, other_y):
        if self.x > other_x:
            self.x += self.speed
        else:
            self.x -= self.speed
        if self.y > other_y:
            self.y += self.speed
        else:
            self.y -= self.speed

    # NPC 靠近攻击
    def approach(self, other_x, other_y):
        if self.x > other_x:
            self.x -= self.speed
        else:
            self.x += self.speed
        if self.y > other_y:
            self.y -= self.speed
        else:
            self.y += self.speed

    # NPC 游荡
    def stray(self):
        self.x += random.randint(-self.speed,self.speed)
        self.y += random.randint(-self.speed,self.speed)

    # NPC 的视野范围内其他的 NPC
    def npc_in_view(self, npc_list):
        npc_in_view = []
        for npc in npc_list:
            if npc != self:
                dist = ((npc.x - self.x)**2 + (npc.y - self.y)**2)**0.5
                if dist <= self.view:
                    npc_in_view.append(npc)
        return npc_in_view

    # 最近的 NPC
    def nearest_npc(self, npc_list):
        min_dist = 100000
        nearest_npc = None
        for npc in npc_list:
            if npc != self:
                dist = ((npc.x - self.x)**2 + (npc.y - self.y)**2)**0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest_npc = npc
        return nearest_npc

# 创建随机名称的函数
def random_name():
    name = ""
    for i in range(8):
        name += random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
    return name

# 创建NPC 列表
def create_npcs():
    npc_list = []
    for i in range(100):
        name = random_name()
        color = random_color()
        x = random.randint(0,DISPLAY_WIDTH)
        y = random.randint(0,DISPLAY_HEIGHT)
        npc = NPC(name, x, y, color)
        npc_list.append(npc)
    return npc_list

# 绘制 NPC
def draw_npc(npc):
    pygame.draw.circle(game_display, npc.color, (npc.x,npc.y), npc.radius)
    font = pygame.font.SysFont(None, 15)
    npc_name = font.render(npc.name, False, npc.color)
    game_display.blit(npc_name, (npc.x-15,npc.y-15))

# 显示用户信息框
def display_stat_window(npc_list):
    npc_counts = {}
    for npc in npc_list:
        if npc.name not in npc_counts:
            npc_counts[npc.name] = {
                "count": 0,
                "color": npc.color,
                "health": npc.health,
                "speed": npc.speed,
                "view": npc.view,
                "attack": npc.attack,
                "aggressive": npc.aggressive,
                "reproduction_time": npc.reproduction_time,
                "killed": npc.killed
                }
        npc_counts[npc.name]["count"] += 1
    message_display("Statistics", DISPLAY_WIDTH / 2-150, DISPLAY_HEIGHT / 2-150, 50)
    count = 0
    for name,attributes in npc_counts.items():
        count += 1
        message = f"Name: {name}  Count: {attributes['count']}"
        message += f"  Health: {attributes['health']}"
        message += f"  Speed: {attributes['speed']}"
        message += f"  View: {attributes['view']}"
        message += f"  Attack: {attributes['attack']}"
        message += f"  Aggressive: {attributes['aggressive']}"
        message += f"  Reproduction Time: {attributes['reproduction_time']}"
        message += f"  Killed: {attributes['killed']}"
        pygame.draw.rect(game_display,attributes['color'],(50,count*50,30,30))
        message_display(message,10,count*50,30)

# 消息函数
def message_display(text, x, y, font_size):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, False, (0, 0, 0))
    game_display.blit(text_surface, (x, y))

# 游戏 循环函数
def game_loop():
    clock = pygame.time.Clock()
    npc_list = create_npcs()
    game_exit = False
    game_paused = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = True

        game_display.fill((255,255,255))
        # 当游戏 paused（暂停） 需要显示统计信息
        if game_paused:
            display_stat_window(npc_list)
        else:
            for npc in npc_list:
                npc.update(npc_list)
                draw_npc(npc)

        message_display("Click 'p' button to Pause/Play", 5, 5, 20)
        message_display("Press Q to quit the game", 5, 30, 20)

        pygame.display.update()
        clock.tick(24)

    pygame.quit()
    quit()

# 开始游戏
game_loop()
