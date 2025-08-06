import pygame
import random

# 初始化pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)    # 蛇身
RED = (255, 0, 0)      # 食物
BLUE = (0, 0, 255)     # 按钮
GRAY = (200, 200, 200) # 按钮点击效果

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 按钮类（封装按钮的绘制和点击检测）
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)  # 按钮位置和大小
        self.text = text                              # 按钮文字
        self.action = action                          # 点击后执行的动作

    def draw(self, surface):
        # 绘制按钮（未点击时蓝色，鼠标悬停时灰色）
        color = GRAY if self.is_hovered() else BLUE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)  # 白色边框

        # 绘制按钮文字
        font = pygame.font.SysFont("SimHei", 24)  # 支持中文显示
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self):
        # 检测鼠标是否悬停在按钮上
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        # 检测按钮是否被点击
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered()
        return False

# 游戏状态（start: 开始界面, playing: 游戏中, gameover: 结束界面）
game_state = "start"

# 创建按钮
start_button = Button(200, 300, 200, 50, "开始游戏", action="start_game")
restart_button = Button(200, 300, 200, 50, "重新开始", action="restart_game")
quit_button = Button(200, 380, 200, 50, "退出游戏", action="quit_game")

# 蛇、食物和分数初始化
def reset_game():
    global snake, direction, food, score
    snake = [(GRID_WIDTH//2 * GRID_SIZE, GRID_HEIGHT//2 * GRID_SIZE)]  # 蛇初始位置
    direction = (GRID_SIZE, 0)  # 初始向右移动
    food = (random.randint(0, GRID_WIDTH-1)*GRID_SIZE, 
            random.randint(0, GRID_HEIGHT-1)*GRID_SIZE)  # 食物随机位置
    score = 0  # 分数

reset_game()  # 初始化游戏

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)  # 清屏

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 开始界面的按钮交互
        if game_state == "start":
            if start_button.is_clicked(event):
                game_state = "playing"  # 进入游戏
            if quit_button.is_clicked(event):
                running = False  # 退出游戏

        # 游戏中的键盘控制
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                    direction = (0, -GRID_SIZE)  # 向上
                elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                    direction = (0, GRID_SIZE)   # 向下
                elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                    direction = (-GRID_SIZE, 0)  # 向左
                elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                    direction = (GRID_SIZE, 0)   # 向右

        # 结束界面的按钮交互
        elif game_state == "gameover":
            if restart_button.is_clicked(event):
                reset_game()
                game_state = "playing"  # 重新开始
            if quit_button.is_clicked(event):
                running = False  # 退出游戏

    # 游戏逻辑（仅在游戏中运行）
    if game_state == "playing":
        # 移动蛇（添加新头部，删除尾部）
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        snake.insert(0, new_head)

        # 检测是否吃到食物
        if new_head == food:
            score += 10
            # 重新生成食物（确保不在蛇身上）
            while food in snake:
                food = (random.randint(0, GRID_WIDTH-1)*GRID_SIZE,
                        random.randint(0, GRID_HEIGHT-1)*GRID_SIZE)
        else:
            snake.pop()  # 没吃到食物就删除尾部

        # 检测碰撞（撞墙或撞自己）
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake[1:]):
            game_state = "gameover"  # 游戏结束

        # 绘制蛇
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE-1, GRID_SIZE-1))

        # 绘制食物
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE-1, GRID_SIZE-1))

        # 显示分数
        font = pygame.font.SysFont("SimHei", 24)
        score_text = font.render(f"分数: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    # 绘制开始界面
    elif game_state == "start":
        font = pygame.font.SysFont("SimHei", 48)
        title_text = font.render("贪吃蛇游戏", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 200))
        start_button.draw(screen)
        quit_button.draw(screen)

    # 绘制结束界面
    elif game_state == "gameover":
        font = pygame.font.SysFont("SimHei", 48)
        over_text = font.render("游戏结束", True, WHITE)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, 150))

        score_font = pygame.font.SysFont("SimHei", 36)
        final_score = score_font.render(f"最终分数: {score}", True, WHITE)
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, 230))

        restart_button.draw(screen)
        quit_button.draw(screen)

    # 更新屏幕
    pygame.display.flip()
    clock.tick(10)  # 控制游戏速度（数值越大越快）

pygame.quit()
