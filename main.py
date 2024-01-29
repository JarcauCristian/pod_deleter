import os
import logging
import uvicorn
from kubernetes import client, config
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    try:
        config.load_incluster_config()
        apps_v1_api = client.AppsV1Api()
        core_v1_api = client.CoreV1Api()
        networking_v1_api = client.NetworkingV1Api()
        namespace = os.getenv("NAMESPACE")

        # Delete Deployment
        deployment_response = apps_v1_api.delete_namespaced_deployment(
            name=f"deployment-{uid}",
            namespace=namespace,
            body=client.V1DeleteOptions(propagation_policy='Foreground')
        )
        logging.info(f"Deployment '{uid}' deleted. Status: {deployment_response.status}")

        # Delete Service
        service_response = core_v1_api.delete_namespaced_service(
            name=f"service-{uid}",
            namespace=namespace,
            body=client.V1DeleteOptions()
        )
        logging.info(f"Service '{uid}' deleted. Status: {service_response.status}")

        # Delete Secret
        secret_response = core_v1_api.delete_namespaced_secret(
            name=f"secret-{uid}",
            namespace=namespace,
            body=client.V1DeleteOptions()
        )
        logging.info(f"Secret '{uid}' deleted. Status: {secret_response.status}")

        # Delete Ingress
        ingress_response = networking_v1_api.delete_namespaced_ingress(
            name=f"ingress-{uid}",
            namespace=namespace,
            body=client.V1DeleteOptions()
        )
        logging.info(f"Ingress '{uid}' deleted. Status: {ingress_response.status}")

    except client.exceptions.ApiException as e:
        logging.error(f"Error deleting Kubernetes resources: {e}")
        raise HTTPException(status_code=500, detail=f"Error occurred while deleting Kubernetes resources for uid: {uid}")

    return JSONResponse(content=f"Deleted pod and associated resources for '{uid}' successfully", status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
