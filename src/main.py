from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.exceptions.custom_exception import RecordNotFoundException, InternalServerException, \
    AuthenticationFailException, UnsupportedFileFormatException, APIAuthenticationFailException
from src.exceptions.custom_exception_handler import ExceptionHandlers, AppException
from src.controllers import therapy


app = FastAPI(title="Mentalyc Service", version="0.0.1", root_path="/v1")

origin = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(APIAuthenticationFailException, ExceptionHandlers.handle_authentication_fail_exception)
app.add_exception_handler(RecordNotFoundException, ExceptionHandlers.handle_record_not_found_exception)
app.add_exception_handler(InternalServerException, ExceptionHandlers.handle_internal_server_exception)
app.add_exception_handler(UnsupportedFileFormatException, ExceptionHandlers.handle_unsupported_file_format_exception)
app.add_exception_handler(Exception, ExceptionHandlers.handle_generic_exception)
app.add_exception_handler(AppException, ExceptionHandlers.handle_app_exception)

@app.get("/")
async def root():
    return "Mentalyc Service API is RUNNING!"

app.include_router(therapy.therapy_router)