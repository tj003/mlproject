import sys
import logging
def error_message_details(error, error_details:sys):
    _,_,exc_tb = error_details.exc_info()#exc - execution info
    file_name = exc_tb.tb_frame.f_code.co_filename# to get a file name on which error is ocuring
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init(error_message)
        self.error_message = error_message_details(error_message, error_details=error_details)

    def __str__(self):
        return self.error_message
    


        