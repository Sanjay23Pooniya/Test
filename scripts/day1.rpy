label game_start:
    menu lap_or_taxi:
        "{b}{color=#000000}Yes \n{size=-4}{color=#2bb8ff}[KoGa3ChoiceView4_1]":
                        $ dylan_lap = True
                        $ dylan += 1
                        jump mama_lap
        "{b}{color=#000000}No \n{size=-4}{color=#1fdb51}[KoGa3ChoiceView2_1] [KoGa3ChoiceView1]":
                        $ good_wife += 1
                        $ dylan_lap = False
                        jump taxi
    label mama_lap:
    menu embrace_hip_or_not:
        "{b}{color=#000000}Hold on to son's hip \n{size=-4}{color=#2bb8ff}[KoGa3ChoiceView4_1]":
                        $ dylan += 1
                        jump embrace_hip
        "{b}{color=#000000}Don’t hold on to son's hip[KoGa3ChoiceView1]":
                        jump not_embrace_hip
    label embrace_hip:
    jump drive_continues
    label not_embrace_hip:
    jump drive_continues
    label drive_continues:
    jump day1_in_house
    label taxi:
    jump day1_in_house
    label day1_in_house:
    jump day2
