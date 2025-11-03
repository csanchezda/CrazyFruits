import os
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.base_path = os.path.join(os.path.dirname(__file__), "../asserts/music")

        # Rutas de sonido
        self.musica_fondo_path = os.path.join(self.base_path, "musica.mp3")
        self.perder_vida_path = os.path.join(self.base_path, "vida_perdida.mp3")
        self.comer_sonidos_paths = [
            os.path.join(self.base_path, f"Comer_fruta{i}.mp3") for i in range(1, 5)
        ]
        self.game_over_path = os.path.join(self.base_path, "game_over.mp3")

        # Cargar sonidos
        self.sonido_perder = pygame.mixer.Sound(self.perder_vida_path)
        self.sonidos_comer = [pygame.mixer.Sound(p) for p in self.comer_sonidos_paths]
        self.sonido_game_over = pygame.mixer.Sound(self.game_over_path)

        # Volúmenes balanceados
        self.sonido_perder.set_volume(0.4)
        for s in self.sonidos_comer:
            s.set_volume(0.35)
        self.sonido_game_over.set_volume(0.5)

        self.muted = False
        self.idx_comer = 0

        # Reproducir música en loop
        pygame.mixer.music.load(self.musica_fondo_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    # Silenciar o activar
    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    # Detener música de fondo
    def detener_musica(self):
        pygame.mixer.music.stop()

    # Reanudar música (reiniciar)
    def reanudar_musica(self):
        if not self.muted:
            pygame.mixer.music.load(self.musica_fondo_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)

    # Sonido al perder vida
    def play_perder(self):
        if not self.muted:
            self.sonido_perder.play()

    # Sonido al comer fruta
    def play_comer(self):
        if not self.muted:
            sonido = self.sonidos_comer[self.idx_comer]
            sonido.play()
            self.idx_comer = (self.idx_comer + 1) % len(self.sonidos_comer)

    # Música de game over
    def play_game_over(self):
        self.detener_musica()
        if not self.muted:
            self.sonido_game_over.play()
