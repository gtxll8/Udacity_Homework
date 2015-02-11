__author__ = 'g'
import turtle

def draw_square(color,shape,speed,angle,size):
    #(1) get the values
    brad = turtle.Turtle()
    brad.color(color)
    brad.shape(shape)
    brad.speed(speed)
    brad.right(angle)
    #(2) initialize loop counter
    counter = 0
    while counter < 4:
        brad.forward(size)
        brad.right(90)
        counter += 1

def draw_triangle(color,shape,speed,angle,size,x,y):
    #(1) get the values
    brad = turtle.Turtle()
    brad.color(color)
    brad.shape(shape)
    brad.speed(speed)
    brad.right(angle)
    brad.goto(x,y)
    #(2) initialize loop counter
    counter = 0
    while counter < 3:
        brad.forward(size)
        brad.right(120)
        counter += 1

def draw_circle(color,shape,speed,radius):
    #(1) get the values
    angie = turtle.Turtle()
    angie.color(color)
    angie.shape(shape)
    angie.speed(speed)
    # draw a circle
    angie.circle(radius)

# Get the canvas up
window = turtle.Screen()
window.bgcolor("blue")

# call the functions to draw a circle out of squares

for angle in range(1, 360,5):
    draw_triangle("yellow","classic",25,angle,100,0,0)
    draw_square("purple","arrow",150,angle,30)
draw_triangle("red","classic",0,0,0,0,-300)
# exit click the window


window.exitonclick()