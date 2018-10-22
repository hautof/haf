from pylib.Http.HttpController import HttpController



for x in range(10):
    result = HttpController.get(url="http://192.168.41.106:8093/publicclass/getlatestactivity", data={"activitycategory":x})
    print(result)