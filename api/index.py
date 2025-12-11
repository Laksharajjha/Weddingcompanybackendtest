try:
    from app.main import app
except Exception as e:
    # DEBUG MODE: Catch startup errors (like missing Env Vars) and show them in browser
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()

    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(path: str):
        return JSONResponse(
            status_code=500, 
            content={
                "error": "Application Startup Failed", 
                "detail": str(e), 
                "trace": traceback.format_exc()
            }
        )
