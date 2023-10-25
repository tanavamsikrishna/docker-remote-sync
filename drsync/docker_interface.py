import docker


def save_docker_image(image, file):
    client = docker.from_env()
    image = client.images.get(image)
    for chunk in image.save():
        file.write(chunk)