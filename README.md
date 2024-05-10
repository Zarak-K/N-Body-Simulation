N-Body simulations are useful across a wide variety of areas in astronomy, from understanding the motion of planets in a star system to trajectories of stars within a galaxy and large scale motions of galaxies. As the equations of motion for N≥3 similarly massive objects have no analytical solutions, numerical integration techniques are implemented to approximate solutions.

These two programs simulate N-Body motion using the 4th order Runge-Kutta method. The masses, initial positions, initial velocities and duration of simulation can be adjusted freely to simulate a variety of interactions, with a few examples related to solar systems presented in the pdf document "Simulations.pdf".

The program "N-Body Simulation.py" will present the motion of objects for a specified duration as a static plot, whereas "N-Body Real-Time.py" will simulate real-time motion using the Pygame module. Some additional features do need to be added to the real-time simulation such as distance indicators and object labels to make the visualization more understandable, but the trajectories of objects are captured reasonably well.

