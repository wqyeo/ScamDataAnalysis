import json

class Database:
    def OpenJsonData(filePath):
        f = open(filePath, 'r', encoding='utf-8-sig')
        data = json.load(f);
        f.close()
        return data

    def SaveStringData(content: str, savePath: str) -> None:
        with open(savePath, 'w') as f:
            f.write(content)

    def SaveJsonData(data, savePath: str) -> None:
        with open(savePath, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
