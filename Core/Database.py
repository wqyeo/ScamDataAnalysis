import json

class Database:

    def SaveStringData(content: str, savePath: str) -> None:
        with open(savePath, 'w') as f:
            f.write(content)

    def SaveJsonData(data, savePath: str) -> None:
        with open(savePath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
