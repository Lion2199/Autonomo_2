import tkinter as tk
import turtle
import threading

def iniciar_juego():
    # Oculta la ventana del menú
    root.withdraw()

    # Crear ventana del juego
    wn = turtle.Screen()
    wn.title("Atari Pong en Python")
    wn.bgcolor("black")
    wn.setup(width=800, height=600)
    wn.tracer(0)

    # Puntos
    score_a = 0
    score_b = 0

    # Paleta A
    paddle_a = turtle.Turtle()
    paddle_a.speed(0)
    paddle_a.shape("square")
    paddle_a.color("white")
    paddle_a.shapesize(stretch_wid=6, stretch_len=1)
    paddle_a.penup()
    paddle_a.goto(-350, 0)

    # Paleta B
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

        # Movimiento de la pelota
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Rebote superior e inferior
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1

        if ball.ycor() < -290:
            ball.sety(-290)
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

        # Rebote con paletas
        if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
            ball.setx(340)
            ball.dx *= -1

        if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
            ball.setx(-340)
            ball.dx *= -1

#Menú inicial con Tkinter
    root.destroy()

def ejecutar_juego():
    hilo_juego = threading.Thread(target=iniciar_juego)
    hilo_juego.start()

# Ventana del menú
root = tk.Tk()
root.title("Menú del Juego Pong")
root.geometry("300x200")

titulo = tk.Label(root, text="🎮 Atari Pong", font=("Arial", 16))
titulo.pack(pady=10)

btn_jugar = tk.Button(root, text="Iniciar Juego", font=("Arial", 14), command=ejecutar_juego)
btn_jugar.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", font=("Arial", 14), command=salir)
btn_salir.pack(pady=10)

root.mainloop()
