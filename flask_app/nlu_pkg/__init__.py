from .services.utils.dependency_containers import Application

embedder_instance = Application().embedders.word2vec_embedder()
