#Import ua-parser.
from ua_parser import user_agent_parser as uap

#Function for parsing incoming lists of UAs and throwing them into another list
def ua_parse(user_agents):
    
    #Check type
    if not(isinstance(user_agents,list)):
        user_agents = [user_agents]
        
    #Construct output list
    output_list = []
    
    #For each entry in the input list, 
    for entry in user_agents:
        
        #Retrieve the UA results
        output_list.append(uap.Parse(entry))
    
    #And return
    return output_list
