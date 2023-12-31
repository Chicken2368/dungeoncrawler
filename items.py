import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, can_be_killed):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type  # index 0 is coin, index 1 is health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.can_be_killed = can_be_killed

    def update(self, screen_scroll, player):
        if self.can_be_killed:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

        if self.rect.colliderect(player.rect) and self.can_be_killed:
            if self.item_type == 0:
                player.score += 1
            elif self.item_type == 1:
                player.health += 10
                if player.health > 100:
                    player.health = 100
            self.kill()
        animation_cooldown = 150
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
