This requires the Nintaco emulator to run, as well as an original Pac-Man NES ROM.
The Nintaco software and library we included is available under the
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html license, and we have
modified it so that it can be used without necessarily invoking an infinite loop.

Start the Nintaco emulator, load the Pac-Man ROM, "Start Program Server"
in the Emulator, and run main.py.
It tends to get stuck in a local maxima solution most of the time.
The best way to avoid this is to use a large population size like 100.
I have had good results with a mutation rate of 0.15.