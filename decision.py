def mod_decision(saef_val, curr_support, freq_support):
    """
    function that takes in our calculated monthly support, the user's current support,
    the frequency of the current support and returns whether the user is eligible for
    modification

    Inputs:
        saef_val: a float of our calculated support (monthly)
        curr_support: a float of the user's current support
        freq_support: a string which is "weekly", "biweekly", or "monthly"

    Returns:
        a string output that shows the original output (with user's original frequency), 
        our calculated amount (with user's original frequency), the percent difference, and 
        whether the user is eligible for modification.     
    """

    if freq_support == "weekly":
        curr_monthly = (curr_support * 52) / 12
        diff = percent_diff(curr_monthly, saef_val)
        saef_val = (saef_val * 12) / 52
       
        
    elif freq_support == "biweekly":
        curr_monthly = (curr_support * 26) / 12
        diff = percent_diff(curr_monthly, saef_val)
        saef_val = (saef_val * 12) / 26
    elif freq_support == "monthly":
        curr_monthly = curr_support
        diff = percent_diff(curr_monthly, saef_val)
        #saef_val will remain the same in output if freq_support == "monthly"
    else:
        return -1    
    
    if diff >= 20:
        place_text = ". You ARE eligible for modifications to your current child support"
    else:
        place_text = ". You are NOT eligible for modifications to your current child support" 

    ret = "User's inputted current support: " + curr_support + " " + freq_support + " SAEF's calculated support: " + saef_val + " " +  freq_support + " percent difference: " + diff + place_text

    return ret

def percent_diff (v1, v2):
    """
    helper to calculate percent difference 

    Inputs:
        v1,v2 : values to calculate, order does not matter

    Returns:
        diff : the percent difference

    """ 

    diff = abs((v1 - v2)/ ((v1 + v2) / 2)) * 100
    diff = round(diff, 2)

    return diff       
