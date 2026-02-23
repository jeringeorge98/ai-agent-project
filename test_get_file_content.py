from fuctions.get_files_content import get_file_content
def test():
    # result = get_file_content("calculator","lerm_ipsum.txt")
    # if len(result) > 1000:
    #     message = result[1000:]
    #     print(("truncated at 1000 characters" in message))
    print(get_file_content("calculator","main.py"))    
    print(get_file_content("calculator","pkg/calculator.py"))
    print(get_file_content("calculator","/bin/cat"))
    print(get_file_content("calculator","pkg/does_not_exist.py"))      
        

if __name__ == "__main__":
    test()
