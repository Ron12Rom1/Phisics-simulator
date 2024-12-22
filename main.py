import pygame
import random
import math

# Initialize pygame
pygame.init()

colors = {
    # Soft Pastel Colors
    "Mint Green": (152, 251, 152),
    "Peach Puff": (255, 218, 185),
    "Lavender Blush": (255, 240, 245),
    "Sky Blue": (135, 206, 235),
    "Pale Yellow": (255, 255, 204),

    # Vibrant Colors
    "Crimson Red": (220, 20, 60),
    "Royal Blue": (65, 105, 225),
    "Amber Orange": (255, 191, 0),
    "Fuchsia": (255, 0, 255),
    "Electric Lime": (204, 255, 0),

    # Earthy Tones
    "Olive Green": (107, 142, 35),
    "Sandy Brown": (244, 164, 96),
    "Terracotta": (210, 105, 30),
    "Slate Gray": (112, 128, 144),
    "Deep Forest Green": (34, 139, 34),

    # Neutral Shades
    "Charcoal": (54, 69, 79),
    "Beige": (245, 245, 220),
    "Ivory": (255, 255, 240),
    "Taupe": (72, 60, 50),
    "Platinum": (229, 228, 226),
}


# Balls stuff
def create_ball(x, y, xv, yv, radius, color = None):
    if color == None:
        color = random.choice(list(colors.values()))
    ball = {'x': x, 'y': y, 'vector': {'x': xv, 'y': yv}, 'radius': radius, 'color': color, "original_color": color, "is_held": False}
    balls.append(ball)
    every_obj.append(ball)

def draw_all_balls():
    for ball in balls:
        pygame.draw.circle(window, ball['color'], (ball['x'], ball['y']), ball['radius'])

def simulate_physics():
    epsilon = 0.1  # Small threshold to prevent sinking
    # Update each ball's position and handle floor collision
    for ball in balls:
        
        if not (ball["is_held"]):
            # Apply gravity
            ball['vector']['y'] += 0.5

            # Update position
            ball['x'] += ball['vector']['x']
            ball['y'] += ball['vector']['y']

        # Update color based on velocity
        if is_make_ball_color_velocity:
            color = min(255, ((abs(ball["vector"]["x"] + ball['vector']['y'])/2) * 0.1) * 255)
            ball['color'] = (color, color, color)
        else:
            ball['color'] = ball["original_color"]

        # Check for collision with the floor
        if ball['y'] >= window_size[1] - ball['radius'] - 25:
            ball['y'] = window_size[1] - ball['radius'] - 25  # Correct position
            ball['vector']['y'] *= bounce_factor  # Reverse and dampen velocity

            # Stop very small bounces
            if abs(ball['vector']['y']) < epsilon:
                ball['vector']['y'] = 0

        # Check for collision with walls
        if ball['x'] <= ball['radius']:
            ball['vector']['x'] *= -1  # Reverse horizontal velocity
            ball["x"] = ball['radius'] + 1
        if ball['x'] >= window_size[0] - ball['radius']:
            ball['vector']['x'] *= -1  # Reverse horizontal velocity
            ball["x"] = window_size[0] - ball['radius'] - 1

    # Check for collisions between balls
    for i, ball1 in enumerate(balls):
        for j, ball2 in enumerate(balls):
            if i != j:
                dx = ball2['x'] - ball1['x']
                dy = ball2['y'] - ball1['y']
                dist = (dx**2 + dy**2)**0.5

                # Check if the balls are colliding
                if dist < ball1['radius'] + ball2['radius']:
                    # Resolve overlap
                    overlap = ball1['radius'] + ball2['radius'] - dist
                    if dist != 0:
                        dx_norm = dx / dist
                        dy_norm = dy / dist
                    else:
                        dx_norm = 0
                        dy_norm = 0
                    ball1['x'] -= dx_norm * overlap / 2
                    ball1['y'] -= dy_norm * overlap / 2
                    ball2['x'] += dx_norm * overlap / 2
                    ball2['y'] += dy_norm * overlap / 2

                    # Calculate velocity components along the collision normal
                    v1n = ball1['vector']['x'] * dx_norm + ball1['vector']['y'] * dy_norm
                    v2n = ball2['vector']['x'] * dx_norm + ball2['vector']['y'] * dy_norm

                    # Exchange the normal components of velocity
                    ball1['vector']['x'] += (v2n - v1n) * dx_norm
                    ball1['vector']['y'] += (v2n - v1n) * dy_norm
                    ball2['vector']['x'] += (v1n - v2n) * dx_norm
                    ball2['vector']['y'] += (v1n - v2n) * dy_norm

# Floor stuff
def create_floor():
    floor = {'x': 0, 'y': window_size[1] - 25, 'vector': {'x': 0, 'y': 0}, 'radius': 0, 'color': ( 200, 200, 200)}
    every_obj.append(floor)

def draw_floor():
    pygame.draw.rect(window, (200, 200, 200), (0, window_size[1] - 25, window_size[0], 25))


# Useful functions
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def check_colision(obj1, obj2) -> bool:
    return obj1['x'] < obj2['x'] + obj2['radius'] and obj1['x'] + obj1['radius'] > obj2['x'] and obj1['y'] < obj2['y'] + obj2['radius'] and obj1['y'] + obj1['radius'] > obj2['y']


# Change all globla ball values
def change_color_for_all_balls(color):
    for ball in balls:
        ball['color'] = color

def change_size_for_all_balls(offset = None):
    if offset == None:
        for ball in balls:
            ball['radius'] = 10
            return
    elif offset == default_ball_size:
        for ball in balls:
            ball['radius'] = default_ball_size
    else:    
        for ball in balls:
            ball['radius'] += offset
    
    max_ball_size = 100
    ball["radius"] = min(max_ball_size, ball["radius"])


# Calc vector
def calc_vector(x1, y1, x2, y2, flip = False):
    if flip:
        return [float(x1) - float(x2), float(y1) - float(y2)]
    return [float(x2) - float(x1), float(y2) - float(y1)]

# Catapulted ball stuff
def draw_start_point_for_catapuled_ball(original_x, original_y, color):
    if original_x == None or original_y == None:
        return
    pygame.draw.circle(window, color, (original_x, original_y), 5)

def draw_line_for_catapulted_ball(original_x, original_y, mouse_x, mouse_y, color):
    if original_x == None or original_y == None:
        return
    d = distance(original_x, original_y, mouse_x, mouse_y)
    size = 2 / d * 500
    color = balls[heled_ball]["color"]
    pygame.draw.line(window, (color[0] * 0.8, color[1] * 0.8, color[2] * 0.8), (original_x, original_y), (mouse_x, mouse_y), int(min(size, 10)))


# Reset all variables
def reset_all():
    balls.clear()
    every_obj.clear()
    create_floor()
    global bounce_factor
    bounce_factor = -0.8
    global default_ball_size
    default_ball_size = 20
    global is_make_ball_color_velocity
    is_make_ball_color_velocity = False

# Set up lists
balls = []
every_obj = []
mouse_pos = []

# Set up the display
window_size = (1200, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Black Window")

# Veriables
BACKGROUND_COLOR = (50, 50, 50)
times = 1
last_x, last_y = 0, 0
global bounce_factor
bounce_factor = -0.8  # Reduces velocity after a bounce
global is_make_ball_color_velocity
is_make_ball_color_velocity = False
shift_pressed = False
global default_ball_size
default_ball_size = 20
global heled_ball
heled_ball = None
original_x, original_y = None, None

# Create floor
create_floor()

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the window with black color
    window.fill(BACKGROUND_COLOR)
    
    # Get the current state of the keyboard
    keys = pygame.key.get_pressed()
    
    # Store last 5 mouse positions
    mouse_pos.append(pygame.mouse.get_pos())
    if len(mouse_pos) > 5:
        mouse_pos.pop(0)

    
    # Check for mouse click events
    if pygame.mouse.get_pressed()[0]:  # Left mouse button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if len(balls) == 0:
            create_ball(mouse_x, mouse_y, 0, 0, 20)
        if distance(balls[-1]["x"], balls[-1]["y"], mouse_x, mouse_y) > 35 and len(balls) < 200:
            last_x, last_y = mouse_x, mouse_y
            for i in range(times):
                create_ball(mouse_x, mouse_y, 0, 0, default_ball_size)
    # Catapult ball from its original position
    elif pygame.mouse.get_pressed()[2] and keys[pygame.K_LCTRL]:  # Right mouse button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if heled_ball == None:
            for ball in balls:
                if distance(ball["x"], ball["y"], mouse_x, mouse_y) < ball["radius"]:
                    original_x, original_y = ball["x"], ball["y"]
                    ball["is_held"] = True
                    heled_ball = balls.index(ball)
        else:
            balls[heled_ball]["x"] = mouse_x
            balls[heled_ball]["y"] = mouse_y

            # Draw the starting point for the catapulted ball
            color = balls[heled_ball]["color"]
            color = (color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
            draw_start_point_for_catapuled_ball(original_x, original_y, color)
            draw_line_for_catapulted_ball(original_x, original_y, mouse_x, mouse_y, color)
    elif not pygame.mouse.get_pressed()[2] and keys[pygame.K_LCTRL] and heled_ball != None and original_x and original_y:
        if len(balls) > 0 and heled_ball != None:
            new_vector_x, new_vector_y = calc_vector(original_x, original_y, mouse_x, mouse_y, flip = True)
            balls[heled_ball]["vector"]["x"], balls[heled_ball]["vector"]["y"] = new_vector_x*0.2, new_vector_y*0.2
            original_x, original_y = None, None
            balls[heled_ball]["is_held"] = False
            heled_ball = None
    # Drag and drop balls
    elif pygame.mouse.get_pressed()[2]:  # Right mouse button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if heled_ball == None:
            for ball in balls:
                if distance(ball["x"], ball["y"], mouse_x, mouse_y) < ball["radius"]:
                    ball["is_held"] = True
                    heled_ball = balls.index(ball)
        else:
            balls[heled_ball]["x"] = mouse_x
            balls[heled_ball]["y"] = mouse_y
    elif not pygame.mouse.get_pressed()[2]:
        if len(balls) > 0 and heled_ball != None:
            balls[heled_ball]["vector"]["x"], balls[heled_ball]["vector"]["y"] = calc_vector(mouse_pos[-3][0], mouse_pos[-3][1], mouse_x, mouse_y)
            balls[heled_ball]["is_held"] = False
            heled_ball = None

    # Keyboard events
    if keys[pygame.K_c]:
        balls.clear()
    if keys[pygame.K_r]:
        reset_all()        
    # Change the bounce factor
    if keys[pygame.K_UP]:
        bounce_factor -= 0.01
    if keys[pygame.K_DOWN]:
        bounce_factor += 0.01
    # Enable / disable physics
    space_pressed = True
    if keys[pygame.K_SPACE]:
        space_pressed = False
    if space_pressed:
        simulate_physics()
    # Toggle color velocity
    if keys[pygame.K_LSHIFT]:
        if not shift_pressed:
            is_make_ball_color_velocity = not is_make_ball_color_velocity
            shift_pressed = True
    else:
        shift_pressed = False
    # Change size of balls
    if keys[pygame.K_LCTRL]:
        if keys[pygame.K_k]:
            default_ball_size += 1
            change_size_for_all_balls(default_ball_size)
        if keys[pygame.K_l]:
            default_ball_size -= 1
            change_size_for_all_balls(default_ball_size)
    if keys[pygame.K_k]:
        change_size_for_all_balls(0.2)
    if keys[pygame.K_l]:
        change_size_for_all_balls(-0.2)
    
    # Draw gmae objects
    draw_all_balls()
    draw_floor()
    
    # Draw the number of balls
    font = pygame.font.Font(None, 24)
    text = font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
    window.blit(text, (5, 10))
    # Draw the FPS
    font = pygame.font.Font(None, 24)
    text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    window.blit(text, (5, 30))
    # Draw the bounce factor
    font = pygame.font.Font(None, 24)
    text = font.render(f"Bounce factor: {bounce_factor}", True, (255, 255, 255))
    window.blit(text, (5, 50))

    # Update the display
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Quit pygame
pygame.quit()


