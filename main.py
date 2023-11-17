import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from kubernetes import client, config
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def connection_test():
    return JSONResponse("Server Works!", status_code=200)


@app.delete("/delete_pod")
async def delete_pod(uid: str):
    config.load_incluster_config()
    api_instance = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()

    api_response = api_instance.delete_namespaced_deployment(
        name=f"deployment-{uid}",
        namespace=os.getenv("NAMESPACE"),
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
        )
    )
    print(f"Deployment '{deployment_name}' deleted. Status: {api_response.status}")

    api_response = core_v1_api.delete_namespaced_service(
        name=f"service-{uid}",
        namespace=os.getenv("NAMESPACE"),
        body=client.V1DeleteOptions()
    )
    print(f"Service '{service_name}' deleted. Status: {api_response.status}")

    return JSONResponse(content="Deleted Pod Successfully!", status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=49152)
