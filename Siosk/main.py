from package.model import API
from auto.delete import delete_dot_underscore_files

# To get your own API Key for Siosk, Please visit to https://anoask.site and register
api = API(
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2Fub2Fzay5zaXRlIiwiZXhwIjoxNzE3NDcwMDc5LCJzdWIiOiIzOCJ9._1iLHXYqP5ht71-NUKGlmJYJuDR9m3uoIVGywJSDoa0",
    url = "http://127.0.0.1"
)

if __name__ == "__main__":
    delete_dot_underscore_files() 
    api.preparing()
    api.detecting()  