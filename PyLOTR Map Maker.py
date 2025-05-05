import pygame
import sys

SCALE = 4
PAN_STEP = 50
OUTPUT_FILE = "waypoints.txt"

class Waypoint:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def format_code(self):
        return f"{self.name}(Region.PLACEHOLDER, WitcherFaction.PLACEHOLDER, {self.x}, {self.y}),"

    def save(self):
        with open(OUTPUT_FILE, "a") as f:
            f.write(self.format_code() + "\n")

class TextInputBox:
    def __init__(self, x, y, font):
        self.rect = pygame.Rect(x, y, 200, 32)
        self.color = pygame.Color("white")
        self.text = ''
        self.active = True
        self.font = font

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                name = self.text.strip().upper()
                self.text = ''
                self.active = False
                return name
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 30:
                    self.text += event.unicode
        return None

    def draw(self, screen):
        txt_surface = self.font.render(self.text or "Enter name and press Enter...", True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def main():
    pygame.init()
    image_path = input("Enter the path to the PNG map: ").strip()
    try:
        map_image = pygame.image.load(image_path)
    except:
        print("Failed to open the file.")
        sys.exit()

    map_image = pygame.transform.scale(map_image, (map_image.get_width() * SCALE, map_image.get_height() * SCALE))
    map_width, map_height = map_image.get_size()

    screen_width, screen_height = 1200, 1000
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PyLOTR Map Maker")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    offset_x = 0
    offset_y = 0
    waypoints = []
    input_box = None
    pending_click = None  # (x, y) in original image scale

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(map_image, (-offset_x, -offset_y))

        for wp in waypoints:
            render_x = wp.x * SCALE - offset_x
            render_y = wp.y * SCALE - offset_y
            if 0 <= render_x <= screen_width and 0 <= render_y <= screen_height:
                pygame.draw.circle(screen, (255, 0, 0), (render_x, render_y), 4)
                label = font.render(wp.name, True, (255, 255, 255))
                screen.blit(label, (render_x + 5, render_y - 5))

        if input_box:
            input_box.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not input_box:
                mouse_x, mouse_y = event.pos
                map_x = (mouse_x + offset_x) // SCALE
                map_y = (mouse_y + offset_y) // SCALE
                input_box = TextInputBox(mouse_x, mouse_y, font)
                pending_click = (map_x, map_y)

            elif input_box:
                result = input_box.handle_event(event)
                if result:
                    wp = Waypoint(result, pending_click[0], pending_click[1])
                    waypoints.append(wp)
                    wp.save()
                    print("Added:", wp.format_code())
                    input_box = None
                    pending_click = None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            offset_x = max(offset_x - PAN_STEP, 0)
        if keys[pygame.K_RIGHT]:
            offset_x = min(offset_x + PAN_STEP, map_width - screen_width)
        if keys[pygame.K_UP]:
            offset_y = max(offset_y - PAN_STEP, 0)
        if keys[pygame.K_DOWN]:
            offset_y = min(offset_y + PAN_STEP, map_height - screen_height)

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()











