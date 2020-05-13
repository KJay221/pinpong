import pickle
import numpy as np
import os.path as path
from mlgame.communication import ml as comm

def ml_loop(side: str):
    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    last_ball_x=-1
    last_ball_y=-1
    filename = path.join(path.dirname(__file__),"save/KNN_training_result.pickle")
    with open(filename, 'rb') as file:
        clf = pickle.load(file)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    '''def get_direction(ball_speed_x,ball_speed_y):
        if ball_speed_x>0 and ball_speed_y>0:
            return 1
        elif ball_speed_x<0 and ball_speed_y>0:
            return 2
        elif ball_speed_x<0 and ball_speed_y<0:
            return 3
        elif ball_speed_x>0 and ball_speed_y<0:
            return 4
        else :
            return 0'''

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        ball_x=scene_info["ball"][0]
        ball_y=scene_info["ball"][1]
        if last_ball_x==-1 and last_ball_y==-1:
            last_ball_x=ball_x
            last_ball_y=ball_y

        platform_1P=scene_info["platform_1P"][0]
        platform_2P=scene_info["platform_2P"][0]
        vector_x=ball_x-last_ball_x
        vector_y=ball_y-last_ball_y
        ball_speed_x=scene_info["ball_speed"][0]
        ball_speed_y=scene_info["ball_speed"][1]
        ##direction=get_direction(scene_info["ball_speed"][0],scene_info["ball_speed"][1])
        ## platform2P speedy speedx  y x platform_1P
        data=[platform_2P,ball_speed_y,ball_speed_x,vector_y,vector_x,platform_1P]
        data=np.array(data)
        last_ball_x=ball_x
        last_ball_y=ball_y

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            result=clf.predict([data])
            print(result)
            if result == 5 :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            elif result == -5 :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
