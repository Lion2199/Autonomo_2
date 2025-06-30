import tkinter as tk
from tkinter import messagebox
import turtle
import threading

# Historial global para guardar hasta 5 partidas
historial_estadisticas = []

def iniciar_juego():
    root.withdraw()  # Oculta la ventana del menú
    MAX_SCORE = 10
    score_a = 0
    score_b = 0

    wn = turtle.Screen()
    wn.title("Atari Pong en Python")
    wn.bgcolor("black")
    wn.setup(width=800, height=600)
    wn.tracer(0)

    # Paletas
    paddle_a = turtle.Turtle()
    paddle_a.speed(0)
    paddle_a.shape("square")
    paddle_a.color("white")
    paddle_a.shapesize(stretch_wid=6, stretch_len=1)
    paddle_a.penup()
    paddle_a.goto(-350, 0)

    paddle_b = turtle.Turtle()
    paddle_b.speed(0)
    paddle_b.shape("square")
    paddle_b.color("white")
    paddle_b.shapesize(stretch_wid=6, stretch_len=1)
    paddle_b.penup()
    paddle_b.goto(350, 0)

    # Pelota
    ball = turtle.Turtle()
    ball.speed(1)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 0.2
    ball.dy = 0.2

    # Marcador
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Jugador A: 0  Jugador B: 0", align="center", font=("Courier", 24, "normal"))

    # Movimiento de paletas
    def paddle_a_up():
        y = paddle_a.ycor()
        if y < 250:
            paddle_a.sety(y + 20)

    def paddle_a_down():
        y = paddle_a.ycor()
        if y > -240:
            paddle_a.sety(y - 20)

    def paddle_b_up():
        y = paddle_b.ycor()
        if y < 250:
            paddle_b.sety(y + 20)

    def paddle_b_down():
        y = paddle_b.ycor()
        if y > -240:
            paddle_b.sety(y - 20)

    # Teclado
    wn.listen()
    wn.onkeypress(paddle_a_up, "w")
    wn.onkeypress(paddle_a_down, "s")
    wn.onkeypress(paddle_b_up, "Up")
    wn.onkeypress(paddle_b_down, "Down")

    # Bucle principal del juego
    while True:
        wn.update()
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Rebotes
        if ball.ycor() > 290 or ball.ycor() < -290:
            ball.sety(max(min(ball.ycor(), 290), -290))
            ball.dy *= -1

        # Gol por derecha
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear()
            pen.write(f"Jugador A: {score_a}  Jugador B: {score_b}", align="center", font=("Courier", 24, "normal"))

        # Gol por izquierda
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write(f"Jugador A: {score_a}  Jugador B: {score_b}", align="center", font=("Courier", 24, "normal"))

        # Verificar ganador
        if score_a == MAX_SCORE or score_b == MAX_SCORE:
            ganador = "Jugador A" if score_a == MAX_SCORE else "Jugador B"
            pen.clear()
            pen.goto(0, 0)
            pen.write(f"🏆 {ganador} gana!", align="center", font=("Courier", 28, "bold"))
            wn.update()

            # Guardar estadísticas (máximo 5 partidas)
            historial_estadisticas.append({
                "ganador": ganador,
                "score_a": score_a,
                "score_b": score_b
            })
            if len(historial_estadisticas) > 5:
                historial_estadisticas.pop(0)

            turtle.delay(2000)
            wn.bye()
            root.deiconify()
            break

        # Rebote con paletas
        if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
            ball.setx(340)
            ball.dx *= -1
        if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
            ball.setx(-340)
            ball.dx *= -1

def mostrar_reglas():
    reglas = (
        "🎮 Reglas del Juego Pong:\n\n"
        "1. Jugador A usa las teclas 'W' (subir) y 'S' (bajar).\n"
        "2. Jugador B usa las flechas ↑ (subir) y ↓ (bajar).\n"
        "3. Evita que la pelota pase tu lado.\n"
        "4. Cada fallo del oponente es un punto para ti.\n"
        "5. El primer jugador en llegar a 10 puntos gana.\n"
    )
    messagebox.showinfo("Reglas del Juego", reglas)

def mostrar_estadisticas():
    if not historial_estadisticas:
        messagebox.showinfo("Estadísticas", "No hay partidas registradas todavía.")
        return

    texto = "📊 Últimos 5 juegos:\n\n"
    for i, partida in enumerate(reversed(historial_estadisticas), 1):
        texto += (f"{i}. Ganador: {partida['ganador']} | "
                  f"Puntos A: {partida['score_a']} | "
                  f"Puntos B: {partida['score_b']}\n")

    messagebox.showinfo("Estadísticas", texto)

def abrir_submenu():
    submenu = tk.Toplevel(root)
    submenu.title("Opciones de Juego")
    submenu.geometry("300x220")

    tk.Label(submenu, text="Selecciona una opción:", font=("Arial", 14)).pack(pady=10)

    tk.Button(submenu, text="🎮 Multijugador", font=("Arial", 12), command=lambda: [submenu.destroy(), ejecutar_juego()]).pack(pady=5)
    tk.Button(submenu, text="📊 Últimas estadísticas", font=("Arial", 12), command=mostrar_estadisticas).pack(pady=5)
    tk.Button(submenu, text="🔙 Regresar al menú", font=("Arial", 12), command=submenu.destroy).pack(pady=10)

def ejecutar_juego():
    hilo_juego = threading.Thread(target=iniciar_juego)
    hilo_juego.daemon = True
    hilo_juego.start()

def salir():
    root.destroy()

# Ventana principal
root = tk.Tk()
root.title("Menú del Juego Pong")
root.geometry("300x300")

tk.Label(root, text="🎮 Atari Pong", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Iniciar Juego", font=("Arial", 14), command=abrir_submenu).pack(pady=10)
tk.Button(root, text="Reglas del Juego", font=("Arial", 14), command=mostrar_reglas).pack(pady=10)
tk.Button(root, text="Salir", font=("Arial", 14), command=salir).pack(pady=10)

root.mainloop()
