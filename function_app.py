"""
function_app.py
Entry point for the application.
"""
from src.functions.main_function import main

import logging
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="*/5 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def PP_DatabaseUpdater(myTimer: func.TimerRequest) -> None:
    
    main()
    logging.info('Python timer trigger function executed.')