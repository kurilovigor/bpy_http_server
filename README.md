# Blender 2.8 HTTP Server

This is a simple addon that creates HTTP server on `http://localhost:8088` that allows to connect to Blender application and execute python scripts. This can be usefull for applications, that need simple Blender integration.

## Installing

Install `src/bpy_http_server.py` as an addon using *Edit > Preferences > Add-ons > Install from disk* and enable it.

## How to use addon

Addon creates following endpoints:

- GET http://localhost:8088/version - Get blender version.
- POST http://localhost:8088/exec - Execute python script in Blender context.
- POST http://localhost:8088/eval - Eval python script in Blender context and return result in JSON format.

This example HTTP request returns number of scene objects:

    POST http://localhost:8088/eval
    Content-Type: text/plain

    len(bpy.context.scene.objects)
