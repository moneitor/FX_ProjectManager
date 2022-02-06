

def fix_name(text):
    new_text = text.replace(" ", "_").lower()
    return new_text
    
    

    
if __name__ == "__main__":
    print (fix_name("Paco romola"))