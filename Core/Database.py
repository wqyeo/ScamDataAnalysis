class Database:

    def SaveData(content: str, savePath: str) -> None:
        with open(savePath, 'w') as f:
            f.write(content)