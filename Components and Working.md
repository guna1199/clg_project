For Data Logging : We used color sensor to represent different PCBs and it detects the sticker placed on the corner of PCB and
                   Two color sensor one at the starting stage and one at the exit. After it exits, the time taken is automatically
                   noted and sent to the server.

For Solder tube : We have a laser and a detector setup, which is kept at a pre-defined level in the tube.So when the paste level goes
                  the detector detects and sends a signal to the raspberry pi, which sends it to the Adafruit IO server.
                  
For Exhaust fans : We have developed a tachometer like setup using arduino and IR sensor, this setup gives a RUNNING/ NOT RUNNING
                   update to the server depending on the speed of the fan continuously.
                   
                   
                   
