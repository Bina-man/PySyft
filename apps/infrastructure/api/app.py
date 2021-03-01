import json
import os
from pathlib import Path

from flask import Flask, Response, jsonify, request
from loguru import logger

from apps.infrastructure.providers import AWS_Serverfull, AWS_Serverless
from apps.infrastructure.utils import Config

app = Flask(__name__)


@app.route("/")
def index():
    response = {
        "message": "Welcome to OpenMined PyGrid Infrastructure Deployment Suite"
    }
    return Response(json.dumps(response), status=200, mimetype="application/json")


@app.route("/deploy", methods=["POST"])
def deploy():
    """Deploys the resources."""

    data = json.loads(request.json)
    config = Config(**data)

    deployment = None
    deployed = False
    output = None

    config.app.id = 0

    if config.provider == "aws":
        deployment = (
            AWS_Serverless(config)
            if config.serverless
            else AWS_Serverfull(config=config)
        )
    elif config.provider == "azure":
        pass
    elif config.provider == "gcp":
        pass

    if deployment.validate():
        # deployed = True
        # output = {}
        deployed, output = deployment.deploy()

    response = {
        "message": f"Your PyGrid {config.app.name} was deployed successfully"
        if deployed
        else f"Your attempt to deploy PyGrid {config.app.name} failed",
        "output": output,
    }
    return Response(json.dumps(response), status=200, mimetype="application/json")