EMBEDDING_FUNC_KWARGS = 'embedder'
VALIDITY_FUNC_KWARGS = 'contains'


class MetaEmbedder(type):
    def __init__(cls, name, bases, clsdict, **kwargs):
        super().__init__(cls)
        validity_func_name = kwargs[VALIDITY_FUNC_KWARGS]
        embedding_func_name = kwargs[EMBEDDING_FUNC_KWARGS]
        validity_func = clsdict[validity_func_name]
        embedding_func = clsdict[embedding_func_name]
        if embedding_func_name in clsdict:
            def func_wrapper(*args, **kwargs):
                if validity_func(*args, **kwargs):
                    return embedding_func(*args, **kwargs)
                else:
                    print("INVALID DETECTED")

            setattr(cls, embedding_func_name, func_wrapper)


