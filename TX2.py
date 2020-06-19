# coding: utf-8
import docker


class TX2(object):
    def __init__(self,IP):
        self.ip = IP
        self.client = docker.DockerClient(base_url="tcp://" + self.ip + ":2375")
    def Images(self):
        images = self.client.images.list()
        return images
    def Containers(self):
        containers = self.client.containers.list()
        container_dict = {}
        for con in containers:
            container_dict[str(con.name)] = con
        return container_dict

