
import time
import math
import numpy as np
import vpython as vp


# dimensions of the 3d window
vp.scene.width = 1600
vp.scene.height = 900

# disable automatic camera scaling
vp.scene.autoscale = False

# adjust the visible depth of the camera
vp.scene.range = 2e11

fps_display = vp.wtext(text="FPS: Calculating")

last_time = time.time()
frame_count = 0

#  Start state: Simulation is running
running = True

# This function triggers every time a key is pressed
def key_input(evt):
    global running
    # If the spacebar is pressed, flip the running state
    if evt.key == ' ':
        running = not running
        # Optional: Print the state to the terminal
        if running:
            print("Simulation Resumed")
        else:
            print("Simulation Paused")

# Bind the function to the keyboard input of the 3D window
vp.scene.bind('keydown', key_input)

# universal Gravitational Constant (G)
G = 6.6743e-11

# create the Sun
sun = vp.sphere(
    pos=vp.vector(0,0,0),
    radius = 1.5e10,
    color = vp.color.yellow
)

# mass of the sun in kg
sun.m =  1.989e30

sun_text = vp.text(
    text="Sun", 
    pos=vp.vector(2.2e10, 0, 0,), 
    height=4e9,            # Die Schrifthöhe in echten Weltraum-Metern!
    align="center",        # Zentriert den Text über dem Punkt
    color=vp.color.white
)

# create Earth
earth = vp.sphere(
    pos=vp.vector(1.496e11,0,0)
    , radius = 4e9,
    color = vp.color.red,
    make_trail = True   
)
# initial velocity vector of the Earth
earth.v = vp.vector(0,29780,0)
# mass of Earth in kg
earth.m = 5.972e24

earth_text = vp.text(
    text="Earth", 
    pos=earth.pos, 
    height=4e9,            
    align="center",        
    color=vp.color.white
)

# the time step for each calculation cycle (3600 seconds = 1 hour of simulated time per loop iteration)
dt = 7200

moon = vp.sphere(
    pos= earth.pos + vp.vector(6.5e9,0,0),
    radius = 1.5e9,
    color = vp.vector(0.5,0.5,0.5),
    make_trail = True
)

moon.m = 7.342e22
moon.v = earth.v + vp.vector(0,7800,0)

mars = vp.sphere(
    pos= earth.pos + vp.vector(2.279e11,0,0),
    radius = 3e9,
    color = vp.vector(0.7,0.25,0.05),
    make_trail = True
)


mars.m = 6.4171e23
mars.v = vp.vector(0, 24007, 0)

mars_text = vp.text(
    text="Mars", 
    pos=mars.pos, 
    height=4e9,            
    align="center",       
    color=vp.color.white
)

venus = vp.sphere(
    pos= vp.vector(1.082e11, 0, 0),
    radius = 3.8e9,
    color = vp.vector(0.95, 0.75, 0.3),
    make_trail = True
)

venus.m = 4.8675e24
venus.v = vp.vector(0, 35020, 0)

venus_text = vp.text(
    text="Venus", 
    pos=venus.pos, 
    height=4e9,            
    align="center",        
    color=vp.color.white
)

mercury = vp.sphere(
    pos= vp.vector(5.791e10, 0, 0),
    radius = 2.5e9,
    color = vp.vector(0.6, 0.6, 0.6),
    make_trail = True
)

mercury.m = 3.3011e23
mercury.v = vp.vector(0, 47360, 0)

mercury_text = vp.text(
    text="Mercury", 
    pos=mercury.pos, 
    height=4e9,            
    align="center",        
    color=vp.color.white
)



while True:

    vp.rate(120)

    if running:

        #EARTH
        # Calculate the distance vector from earth to sun
        r_vector = sun.pos - earth.pos

        # Get the actual distance as a single scalar value (meters)
        r_mag = vp.mag(r_vector)

        #Calculate the magnitude of the gravitational force (Newton's formula)
        f_mag = (G * earth.m * sun.m) / r_mag**2

        # Compute acceleration vector using force magnitude, mass, time step, and direction
        a = (f_mag / earth.m) * dt * vp.norm(r_vector)

        # Update earth's velocity vector with the acceleration
        earth.v += a 

    

        #MOON physics
        m_r_vector = earth.pos - moon.pos
        m_r_mag = vp.mag(m_r_vector)
        m_f_mag = (G * moon.m * earth.m * 1000) / m_r_mag**2
        m_a = (m_f_mag / moon.m) * dt * vp.norm(m_r_vector)
    

        #MOON-SUN physics
        m_r_sun = sun.pos - moon.pos
        m_r_sun_mag = vp.mag(m_r_sun)
        m_f_sun = (G * moon.m * sun.m) / m_r_sun_mag**2
        m_a_sun = (m_f_sun / moon.m) * dt * vp.norm(m_r_sun)

        # add both forces (from Earth and Sun) to the Moon's velocity
        moon.v += (m_a + m_a_sun)


        #MARS
        r_vector_mars = sun.pos - mars.pos
        r_mag_mars = vp.mag(r_vector_mars)
        f_mag_mars = (G * mars.m * sun.m) / r_mag_mars**2
        a_mars = (f_mag_mars / mars.m) * dt * vp.norm(r_vector_mars)
        mars.v += a_mars 

        #VENUS
        r_vector_venus = sun.pos - venus.pos
        r_mag_venus = vp.mag(r_vector_venus)
        f_mag_venus = (G * venus.m * sun.m) / r_mag_venus**2
        a_venus = (f_mag_venus / venus.m) * dt * vp.norm(r_vector_venus)
        venus.v += a_venus


        #MERCURY
        r_vector_mercury = sun.pos - mercury.pos
        r_mag_mercury = vp.mag(r_vector_mercury)
        f_mag_mercury = (G * mercury.m * sun.m) / r_mag_mercury**2
        a_mercury = (f_mag_mercury / mercury.m) * dt * vp.norm(r_vector_mercury)
        mercury.v += a_mercury


        # Update earth's position vector based on the new velocity and time step
        earth.pos += earth.v * dt

        moon.pos += moon.v * dt

        mars.pos += mars.v * dt

        venus.pos += venus.v * dt

        mercury.pos += mercury.v * dt


        # Count this frame
        frame_count += 1
        current_time = time.time()
    
        # If 1 full second has passed, update the display
        if current_time - last_time >= 1.0:
            fps_display.text = "FPS: " + str(frame_count)
            frame_count = 0          # Reset the counter for the next second
            last_time = current_time # Reset the timer
