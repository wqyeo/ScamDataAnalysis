class WebContent:
    def __init__(self, tag: str, jsonName: str, class_:str = None, innerContents: list = None) -> None:
        """
        Represents a web content data.

        # Params
        --------------------------
        **tag**
        The HTML tag this content was under.

        **class_** *Optional*
        The class tag this content was under.

        **jsonName**
        The name to be classified under when this gets parsed to JSON.

        **innerContents** *Optional*
        The inner contents of this content.
        """
        self.tag = tag
        self.class_ = class_
        self.jsonName = jsonName
        self.innerContents = innerContents
        pass