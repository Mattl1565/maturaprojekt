def are_cars_overtaking(car1X1, car1Y1, car1X2, car1Y2, car2X1, car2Y1, car2X2, car2Y2, threshold):
    """
     Determine if two cars are overlapping.

     Parameters:
     - car1Y1 (float): Y coordinate of car 1 at time 0.
     - car1X1 (float): X coordinate of car 1 at time 0.
     - car1Y2 (float): Y coordinate of car 1 at time 1.
     - car1X2 (float): X coordinate of car 1 at time 1.
     - car2X1 (float): X coordinate of car 2 at time 0.
     - car2Y1 (float): Y coordinate of car 2 at time 0.
     - car2X2 (float): X coordinate of car 2 at time 1.
     - car2Y2 (float): Y coordinate of car 2 at time 1.

     Returns:
     - bool: True if the cars are overlapping, False otherwise.
          - return(True) if car1X1 < car2X2 and car1X2 > car2X1 and car1Y1 > car2Y2 and car1Y2 < car2Y1
          - else return(False)
     """
    # if car1Y1 < car2Y2 and car1X2 > car2X2 and car1Y2 >= car2Y2 and (car1X1 <= (car2X1 + threshold) or car1X1 >= (car2X1 - threshold)):
    #     return True
    # elif car2Y1 < car1Y2 and car2X2 > car1X2 and car2Y2 >= car1Y2 and (car2X1 <= (car1X1 + threshold) or car2X1 >= (car1X1 - threshold)):
    #     return True
    # else:
    #     return False

    if car1Y1 > car2Y1 and car1X2 > car2X2 and car1Y2 >= car2Y2 and (car1X1 <= (car2X1 + threshold) or car1X1 >= (car2X1 - threshold)):
        return True
    elif car2Y1 < car1Y1 and car2X2 > car1X2 and car2Y2 >= car1Y2 and (car2X1 <= (car1X1 + threshold) or car2X1 >= (car1X1 - threshold)):
        return True
    else:
        return False
