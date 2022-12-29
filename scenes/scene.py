import pygame

# Scene class
# Not meant to be used in its lonesome

class Scene:
    def __init__(self):
        self.canEscape = True
        self.next = self
        self.prev = None
        self.creation_time = pygame.time.get_ticks()
    
    # Process inputs
    def ProcessInput(self, events, pressed_keys):
        print("ProcessInput")

    # Update the scene based on input
    def Update(self):
        print("Update")

    # Draw the scene
    def Render(self, screen):
        print("Render")
    
    # Ensure that the scene closes without losing data, etc.
    def Terminate(self):
        pass