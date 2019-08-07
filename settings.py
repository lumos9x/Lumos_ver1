import os, json

class Secrets:

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    secret_file = os.path.join(BASE_DIR,'secrets.json') # secrets.json 파일 위치를 명시
    secrets = {}

    def __init__(self):
        # 파일읽기
        with open(self.secret_file) as f:
            self.secrets = json.loads(f.read())

    def get_secret(self, k):
        """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
        try:
            return self.secrets[k]

        except KeyError:
            error_msg = "Set the {} environment variable".format(k)



if __name__ == '__main__':
    sec = Secrets()
    print(sec.get_secret("GOOGLE_MAP_KEY"))
