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
    def __init__(self, name, x, y, color, radius, speed, health, view, attack, aggressive, reproduction_time, killed, life):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = speed
        self.health = health
        self.max_health = health
        self.view = view
        self.attack = attack
        self.aggressive = aggressive
        self.reproduction_time = reproduction_time
        self.time_since_reproduction = 0
        self.killed = killed
        self.life = life
        self.max_life = life

    # 更新 NPC 的属性
    def update(self, npc_list):
        self.move(npc_list)
        self.time_since_reproduction += 1
        self.life -= 1
        if self.time_since_reproduction >= self.reproduction_time:
            self.reproduce(npc_list)
            self.time_since_reproduction = 0
        if self.life <= 0:
            npc_list.remove(self)

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

    # NPC 繁殖
    def reproduce(self, npc_list):
        offspring = NPC(self.name, self.x, self.y, self.color, self.radius, self.speed, self.max_health, self.view, self.attack, self.aggressive, self.reproduction_time, self.killed, self.max_life)
        npc_list.append(offspring)

    # NPC 移动
    def move(self, npc_list):
        npc_in_view = self.npc_in_view(npc_list)
        if npc_in_view:
            nearest_npc = self.nearest_npc(npc_in_view)
            if nearest_npc:
                if self.check_colliding_npcs(nearest_npc) == True:
                    self.attack_npc(nearest_npc, npc_list)
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
        else:
            self.stray()        
        # 如果超出了范围，NPC将出现在另一象限
        
        if self.x < 0:
            self.x = DISPLAY_WIDTH + self.x - self.radius
        if self.x > DISPLAY_WIDTH:
            self.x = self.x - DISPLAY_WIDTH + self.radius
        if self.y < 0:
            self.y = DISPLAY_HEIGHT + self.y - self.radius
        if self.y > DISPLAY_HEIGHT:
            self.y = self.y - DISPLAY_HEIGHT + self.radius
        

    #检测NPC碰撞
    def check_colliding_npcs(self, nearest_npc):
        if abs(self.x - nearest_npc.x) <= self.radius and abs(self.y - nearest_npc.y) <= self.radius:
            return True
        else:
            return False  

    # NPC 攻击
    def attack_npc(self, other_npc, npc_list):
        if other_npc.name == self.name: #自己繁殖的NPC不攻击
            return
        else:
            other_npc.health -= self.attack
        
        if other_npc.health <= 0:
            self.killed += 1
            npc_list.remove(other_npc)

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
        random.seed()
        self.x = random.randint(-self.speed,self.speed)
        random.seed()
        self.y = random.randint(-self.speed,self.speed)
        
        '''
        random.seed()
        if self.x > DISPLAY_WIDTH/2:
            self.x += random.randint(-self.speed,int(self.speed/2))
        else:
            self.x += random.randint(-int(self.speed/2),self.speed)
        random.seed()
        if self.y > DISPLAY_HEIGHT/2:
            self.y += random.randint(-self.speed,int(self.speed/2))
        else:
            self.y += random.randint(-int(self.speed/2),self.speed)
        '''
        

    # NPC 的视野范围内其他的 NPC
    def npc_in_view(self, npc_list):
        npc_in_view = []
        for npc in npc_list:
            if npc.name != self.name:
                if abs(npc.x - self.x) <= self.view and abs(npc.y - self.y) <= self.view: #减少计算量简单计算，实际应该计算圆形面积内的NPC
                    npc_in_view.append(npc)
        return npc_in_view

    # 最近的敌对 NPC
    
    def nearest_npc(self, npc_list):
        min_dist = self.view * 2
        nearest_npc = None
        for npc in npc_list:
            if npc.name != self.name:
                dist = abs(npc.x - self.x) + abs(npc.y - self.y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_npc = npc
        return nearest_npc
    '''
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
    '''

# 创建随机名称的函数
def random_name():
    name = ""
    for i in range(8):
        name += random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
    return name

# 创建NPC 列表
def create_npcs():
    npc_list = []
    row = 1
    column = 1
    x = 1 
    y = 1
    npc_number = 300
    for i in range(npc_number):
        name = random_name()
        color = random_color()
        x = int(row * DISPLAY_WIDTH/(npc_number**0.5))
        row += 1
        if x >= DISPLAY_WIDTH:
            y = int(column * DISPLAY_HEIGHT/(npc_number**0.5))
            row = 1
            column += 1
        if y > DISPLAY_WIDTH:
            message_display('Too much NPC !! Please reduce the NPC number!!',DISPLAY_WIDTH/2-100,DISPLAY_WIDTH/2-100,50)
            time.sleep(3)
            pygame.quit()
            quit()
        
        radius = random.randint(2,10)
        speed = random.randint(5,30)
        health = random.randint(50,500)
        view = random.randint(30,300)
        attack = random.randint(10,300)
        aggressive = random.randint(1,3)
        reproduction_time = random.randint(20,300)
        killed = 0
        life = random.randint(reproduction_time*2+1,reproduction_time*4+1)
        
        npc = NPC(name, x, y, color, radius, speed, health, view, attack, aggressive, reproduction_time, killed, life)
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
                "max_health": npc.max_health,
                "speed": npc.speed,
                "view": npc.view,
                "attack": npc.attack,
                "aggressive": npc.aggressive,
                "reproduction_time": npc.reproduction_time,
                "killed": npc.killed,
                "max_life": npc.max_life
                }
        npc_counts[npc.name]["count"] += 1
    message_display("Statistics", DISPLAY_WIDTH / 2-150, 5, 40)
    count = 0
    for name,attributes in npc_counts.items():
        count += 1
        message = f"Name: {name}  Count: {attributes['count']}"
        message += f"  max_health: {attributes['max_health']}"
        message += f"  Speed: {attributes['speed']}"
        message += f"  View: {attributes['view']}"
        message += f"  Attack: {attributes['attack']}"
        message += f"  Aggressive: {attributes['aggressive']}"
        message += f"  Reproduction Time: {attributes['reproduction_time']}"
        message += f"  Killed: {attributes['killed']}"
        message += f"  max_life: {attributes['max_life']}"
        pygame.draw.rect(game_display,attributes['color'],(0,count*35,50,15))
        message_display(message,10,count*35,20)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_exit = True
                if event.key == pygame.K_p:
                    if game_paused == False:
                        game_paused = True
                    else:
                        game_paused = False

        game_display.fill((255,255,255))
        # 当游戏 paused（暂停） 需要显示统计信息
        if game_paused:
            display_stat_window(npc_list)
        else:
            for npc in npc_list:
                npc.update(npc_list)
                draw_npc(npc)

        message_display("Click 'p' button to Pause/Play", 150, 5, 20)
        message_display("Press 'q' to quit ", 5, 5, 20)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    quit()

# 开始游戏
game_loop()
