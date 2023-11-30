from flask_app.nlu_pkg.services.utils.dependency_containers import Application

embedder_instance = Application().embedders.word2vec_embedder()
