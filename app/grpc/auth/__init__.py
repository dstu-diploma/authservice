import app.controllers.auth as auth_controller
from . import auth_pb2_grpc, auth_pb2
from os import environ
import logging
import grpc


GRPC_SERVER_PORT = environ.get("GRPC_SERVER_PORT", "50051")
LOGGER = logging.getLogger("uvicorn")


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    async def InitUser(self, request, context):
        LOGGER.info("Got InitUser message")

        tokens = await auth_controller.init_user(request.user_id, request.role)
        return auth_pb2.TokenPair(
            access_token=tokens.access_token, refresh_token=tokens.refresh_token
        )

    async def GenerateKeyPair(self, request, context):
        LOGGER.info("Got GenerateKeyPair message")

        access, refresh = await auth_controller.generate_key_pair(
            request.user_id, request.role
        )
        return auth_pb2.TokenPair(access_token=access, refresh_token=refresh)

    async def GenerateAccessToken(self, request, context):
        LOGGER.info("Got GenerateAccessToken message")

        token = await auth_controller.generate_access_token(
            request.user_id, request.refresh_token
        )
        return auth_pb2.TokenResponse(token=token)

    async def GenerateRefreshToken(self, request, context):
        LOGGER.info("Got GenerateRefreshToken message")

        token = await auth_controller.generate_refresh_token(
            request.user_id, request.role
        )
        return auth_pb2.TokenResponse(token=token)

    async def ValidateRefreshToken(self, request, context):
        LOGGER.info("Got ValidateRefreshToken message")

        is_valid, payload = await auth_controller.validate_refresh_token(
            request.token
        )
        return auth_pb2.TokenValidationResponse(
            is_valid=is_valid, user_id=payload.user_id, role=payload.role
        )


async def serve():
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port(f"[::]:{GRPC_SERVER_PORT}")
    await server.start()
    LOGGER.info(f"Started AuthService gRPC server on port {GRPC_SERVER_PORT}")

    return server
