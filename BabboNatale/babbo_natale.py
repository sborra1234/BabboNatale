import arcade
import random



"""
Compiti per casa: La scorpacciata di Babbo Natale
Dato questo giochino come partenza, aggiungere le seguenti modifiche:
1 - Scaricare, disegnare o generare con AI un'immagine di sfondo
     e mostrarla poi come background
2 - Premendo il tasto "M", il suono verrà mutato. Premendolo di nuovo
     il suono deve tornare. Avete due possibilità: o evitate proprio
     di far partire il suono, o vi guardate come funziona play_sound
     e vedete se c'è qualcosa che vi può essere utile
3 - Contate quanti biscotti vengono raccolti, salvatelo in una variabile
4 - Mostrate con draw_text il punteggio (numero di biscotti raccolti)
5 - Fate in modo che il nuovo biscotto venga sempre creato almeno a 100 pixel
    di distanza rispetto al giocatore

6 - Ogni volta che babbo natale mangia 5 biscotti, dalla prossima volta
    in  poi verranno creati 2 biscotti per volta. Dopo averne mangiati
    altri 5, vengono creati 3 biscotti per volta, poi 4, e via dicendo

7 - (Opzionale) Ogni volta che genero un biscotto, al 3% di possibilità potrebbe essere un
         "golden cookie". Il golden cookie rimane solo 3 secondi sullo schermo
        ma vale 100 punti. 

        - Crea una nuova immagine per il golden cookie
        - Gestisci la creazione, il timer, ecc
        - Gestisci il punteggio

Fate questo esercizio in una repository su git e mandate il link al vostro account sul form
"""

class BabboNatale(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.babbo = None
        self.lista_babbo = arcade.SpriteList()
        self.lista_cookie = arcade.SpriteList()

        self.sfondo = None
        self.suono_munch = arcade.load_sound("./assets/munch.mp3")
        self.audio_attivo = True

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.velocita = 4

        self.biscotti_raccolti = 0
        self.cookie_per_volta = 1

        self.setup()

    def setup(self):
        self.sfondo = arcade.load_texture("./assets/background.png")

        self.babbo = arcade.Sprite("./assets/babbo.png", scale=1.0)
        self.babbo.center_x = 300
        self.babbo.center_y = 100
        self.lista_babbo.append(self.babbo)

        self.crea_cookie()

    def distanza_da_babbo(self, x, y):
        return math.dist((x, y), (self.babbo.center_x, self.babbo.center_y))

    def crea_cookie(self):
        for _ in range(self.cookie_per_volta):
            cookie = arcade.Sprite("./assets/cookie.png", scale=0.2)

            while True:
                x = random.randint(50, 550)
                y = random.randint(50, 550)
                if self.distanza_da_babbo(x, y) >= 100:
                    break

            cookie.center_x = x
            cookie.center_y = y
            self.lista_cookie.append(cookie)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            self.width // 2,
            self.height // 2,
            self.width,
            self.height,
            self.sfondo
        )

        self.lista_cookie.draw()
        self.lista_babbo.draw()

        arcade.draw_text(
            f"Biscotti: {self.biscotti_raccolti}",
            10,
            self.height - 30,
            arcade.color.WHITE,
            20
        )

    def on_update(self, delta_time):
        change_x = 0
        change_y = 0

        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita

        self.babbo.center_x += change_x
        self.babbo.center_y += change_y

        if change_x < 0:
            self.babbo.scale = (-1, 1)
        elif change_x > 0:
            self.babbo.scale = (1, 1)

        self.babbo.center_x = max(0, min(self.width, self.babbo.center_x))
        self.babbo.center_y = max(0, min(self.height, self.babbo.center_y))

        collisioni = arcade.check_for_collision_with_list(
            self.babbo, self.lista_cookie
        )

        if collisioni:
            if self.audio_attivo:
                arcade.play_sound(self.suono_munch)

            for cookie in collisioni:
                cookie.remove_from_sprite_lists()
                self.biscotti_raccolti += 1

                if self.biscotti_raccolti % 5 == 0:
                    self.cookie_per_volta += 1

            self.crea_cookie()

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif tasto == arcade.key.M:
            self.audio_attivo = not self.audio_attivo

    def on_key_release(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False


def main():
    gioco = BabboNatale(600, 600, "Babbo Natale")
    arcade.run()


if __name__ == "__main__":
    main()

