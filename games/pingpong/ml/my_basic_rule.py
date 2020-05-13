from mlgame.communication import ml as comm

def ml_loop(side: str):
    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    l_b_x=-1
    l_b_y=-1

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

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
            p_x=scene_info["platform_2P"][0]+20
            b_x=scene_info["ball"][0]
            b_y=scene_info["ball"][1]
            if l_b_x==-1 and l_b_y==-1:
                l_b_x=b_x
                l_b_y=b_y
            else:  
                if b_y-l_b_y<0:
                    if (b_x-l_b_x) == 0:
                        m=(b_y-l_b_y)/0.0001
                    else :
                        m=(b_y-l_b_y)/(b_x-l_b_x)
                    x=(80-l_b_y+m*l_b_x)/m
                    if x>200:
                        n_y=m*200-m*l_b_x+l_b_y
                        n_m=-m
                        x=(80-n_y+n_m*200)/n_m
                    elif x<0:
                        n_y=m*0-m*l_b_x+l_b_y
                        n_m=-m
                        x=(80-n_y+n_m*0)/n_m
                    if x>=p_x:
                        comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                    else:
                        comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
                l_b_y=b_y
                l_b_x=b_x
